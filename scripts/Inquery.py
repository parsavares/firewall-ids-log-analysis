# Inquery.py

# Import necessary libraries
import dask.dataframe as dd  # Dask for parallel DataFrame operations
import os                    # For handling file paths
import logging               # For logging outputs to a file
import sys                   # For system-specific parameters and functions
from pathlib import Path     # For intuitive path handling

def setup_logging(log_file):
    """
    Sets up logging to output to both console and a file.
    """
    try:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        # Formatter for log messages
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Ensure the directory for log_file exists
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # File handler to write logs to a file
        file_handler = logging.FileHandler(log_file, mode='w')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Stream handler to output logs to the console
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        logging.info(f"Logging initialized. Logs will be saved to {log_file}")
    except Exception as e:
        print(f"Failed to set up logging: {e}")
        sys.exit(1)  # Exit the script if logging cannot be set up

def standardize_column_names(df):
    """
    Standardizes column names by converting to lowercase and replacing spaces with underscores.
    """
    new_columns = {col: col.strip().lower().replace(' ', '_') for col in df.columns}
    df = df.rename(columns=new_columns)
    return df

def load_csv_files(file_paths):
    """
    Loads CSV files into a dictionary of Dask DataFrames with specified data types.
    """
    dataframes = {}
    for name, path in file_paths.items():
        try:
            logging.info(f"Loading {name} from {path}...")

            # Define data types for problematic columns
            # Adjust these based on your actual data
            dtype = {
                'destination_port': 'object',
                'source_port': 'object'
            }

            # Read CSV with specified dtypes and handle missing values
            df = dd.read_csv(
                path,
                dtype=dtype,
                assume_missing=True,          # Allows integer columns to have NaNs by treating them as floats
                low_memory=False,            # Processes the file in chunks to infer dtypes more accurately
                na_values=['(empty)', ''],   # Define additional strings to recognize as NaN
                keep_default_na=True
            )

            # Standardize column names
            df = standardize_column_names(df)

            # Store the DataFrame in the dictionary
            dataframes[name] = df

            # Log successful load message
            logging.info(f"Successfully loaded {name} with {df.npartitions} partitions.\n")
        except Exception as e:
            logging.error(f"Error loading {name} from {path}: {e}\n")
    return dataframes

def explore_dataframes(dataframes):
    """
    Explores each DataFrame by printing its columns and data types.
    """
    for name, df in dataframes.items():
        logging.info(f"Exploring {name}:")

        try:
            # Compute the number of rows
            num_rows = df.shape[0].compute()
            logging.info(f"Number of Rows: {num_rows}")
        except Exception as e:
            logging.error(f"Error computing number of rows: {e}")

        # Number of columns is accessible directly
        num_cols = df.shape[1]
        logging.info(f"Number of Columns: {num_cols}")

        # Print column names and data types
        logging.info("Column Names and Data Types:")
        logging.info(df.dtypes)
        logging.info("\n")

def find_common_columns(dataframes):
    """
    Finds common columns across all DataFrames.
    """
    column_sets = [set(df.columns) for df in dataframes.values()]
    common_cols = set.intersection(*column_sets)
    return common_cols

def additional_analysis(dataframes):
    """
    Performs additional analyses on the loaded DataFrames.
    """
    for name, df in dataframes.items():
        logging.info(f"Additional Analysis for {name}:")

        try:
            # Descriptive Statistics
            desc = df.describe().compute()
            logging.info("Descriptive Statistics:")
            logging.info(desc)
        except Exception as e:
            logging.error(f"Error computing descriptive statistics for {name}: {e}")

        try:
            # Unique Value Counts for Categorical Columns
            categorical_cols = df.select_dtypes(include=['object', 'string']).columns
            for col in categorical_cols:
                unique_counts = df[col].nunique().compute()
                logging.info(f"Unique values in '{col}': {unique_counts}")
        except Exception as e:
            logging.error(f"Error computing unique value counts for {name}: {e}")

        logging.info("\n")

def main():
    # Setup logging
    user_documents = Path.home() / "Documents"
    log_file = user_documents / "inquery.txt"  # Change to desired directory
    setup_logging(log_file)

    # Define the base directory (adjust if your script is located elsewhere)
    base_dir = os.path.join(os.getcwd(), '..', 'data', 'MC2-CSVFirewallandIDSlogs')

    # Define file paths
    file_paths = {
        'Firewall_04062012': os.path.join(base_dir, 'Firewall-04062012.csv'),
        'Firewall_04072012': os.path.join(base_dir, 'Firewall-04072012.csv'),
        'IDS_0406': os.path.join(base_dir, 'IDS-0406.csv'),
        'IDS_0407': os.path.join(base_dir, 'IDS-0407.csv')
    }

    # Load CSV files into Dask DataFrames
    dataframes = load_csv_files(file_paths)

    # Explore each DataFrame
    explore_dataframes(dataframes)

    # Perform additional analyses
    additional_analysis(dataframes)

    # Identify common columns across all datasets
    common_columns = find_common_columns(dataframes)
    if common_columns:
        logging.info(f"Common Columns Across All Datasets ({len(common_columns)} columns):")
        for col in common_columns:
            logging.info(f"- {col}")
    else:
        logging.info("No common columns found across all datasets.")

    logging.info("\n")

    # Attempt to find subsets with common columns for potential merging
    # For example, Firewalls might have similar columns that can be merged
    firewall_datasets = {name: df for name, df in dataframes.items() if 'firewall' in name.lower()}
    ids_datasets = {name: df for name, df in dataframes.items() if 'ids' in name.lower()}

    # Identify common columns within Firewall datasets
    if len(firewall_datasets) > 1:
        fw_common_cols = set.intersection(*(set(df.columns) for df in firewall_datasets.values()))
        if fw_common_cols:
            logging.info(f"Common Columns Across Firewall Datasets ({len(fw_common_cols)} columns):")
            for col in fw_common_cols:
                logging.info(f"- {col}")

            # Example: Merge Firewall_04062012 and Firewall_04072012 on common columns
            fw_names = list(firewall_datasets.keys())
            df1 = firewall_datasets[fw_names[0]]
            df2 = firewall_datasets[fw_names[1]]
            common_fw_cols = list(fw_common_cols)

            logging.info(f"\nMerging {fw_names[0]} and {fw_names[1]} on columns: {common_fw_cols}")
            try:
                merged_fw = dd.merge(
                    df1,
                    df2,
                    on=common_fw_cols,
                    how='inner'  # Change to 'outer', 'left', or 'right' as needed
                )
                merged_fw_shape = merged_fw.shape.compute()
                logging.info(f"Resulting Merged Firewall DataFrame has {merged_fw_shape[0]} rows and {merged_fw_shape[1]} columns.\n")
                logging.info("Sample of Merged Firewall DataFrame:")
                logging.info(merged_fw.head().compute())
            except Exception as e:
                logging.error(f"Error during merging Firewall datasets: {e}\n")
        else:
            logging.info("No common columns found within Firewall datasets for merging.\n")

    # Similarly, identify and merge within IDS datasets
    if len(ids_datasets) > 1:
        ids_common_cols = set.intersection(*(set(df.columns) for df in ids_datasets.values()))
        if ids_common_cols:
            logging.info(f"Common Columns Across IDS Datasets ({len(ids_common_cols)} columns):")
            for col in ids_common_cols:
                logging.info(f"- {col}")

            # Example: Merge IDS_0406 and IDS_0407 on common columns
            ids_names = list(ids_datasets.keys())
            df3 = ids_datasets[ids_names[0]]
            df4 = ids_datasets[ids_names[1]]
            common_ids_cols = list(ids_common_cols)

            logging.info(f"\nMerging {ids_names[0]} and {ids_names[1]} on columns: {common_ids_cols}")
            try:
                merged_ids = dd.merge(
                    df3,
                    df4,
                    on=common_ids_cols,
                    how='inner'  # Change to 'outer', 'left', or 'right' as needed
                )
                merged_ids_shape = merged_ids.shape.compute()
                logging.info(f"Resulting Merged IDS DataFrame has {merged_ids_shape[0]} rows and {merged_ids_shape[1]} columns.\n")
                logging.info("Sample of Merged IDS DataFrame:")
                logging.info(merged_ids.head().compute())
            except Exception as e:
                logging.error(f"Error during merging IDS datasets: {e}\n")
        else:
            logging.info("No common columns found within IDS datasets for merging.\n")

    # Potential cross-dataset merging (Firewall and IDS) based on IPs and Ports
    # First, identify similar columns with different naming conventions
    # Mapping similar columns
    column_mapping = {
        'firewall_source_ip': 'ids_sourceip',
        'firewall_destination_ip': 'ids_destip',
        'firewall_source_port': 'ids_sourceport',
        'firewall_destination_port': 'ids_destport'
    }

    # Create a copy of dataframes with standardized names for easier mapping
    standardized_dfs = {}
    for name, df in dataframes.items():
        standardized_dfs[name] = df.copy()
        # Prefix firewall and ids for clarity
        if 'firewall' in name.lower():
            standardized_dfs[name] = df.rename(columns={
                'source_ip': 'firewall_source_ip',
                'destination_ip': 'firewall_destination_ip',
                'source_port': 'firewall_source_port',
                'destination_port': 'firewall_destination_port'
            })
        elif 'ids' in name.lower():
            standardized_dfs[name] = df.rename(columns={
                'sourceip': 'ids_sourceip',
                'destip': 'ids_destip',
                'sourceport': 'ids_sourceport',
                'destport': 'ids_destport'
            })

    # Attempt to merge Firewall and IDS datasets on Source IP and Destination IP
    # Note: Given the size of Firewall datasets, merging directly might be resource-intensive
    # Consider sampling or filtering data before merging

    # Example: Merge Firewall_04062012 with IDS_0406
    fw_name = 'Firewall_04062012'
    ids_name = 'IDS_0406'
    fw_df = standardized_dfs.get(fw_name)
    ids_df = standardized_dfs.get(ids_name)

    if fw_df is not None and ids_df is not None:
        merge_on = ['firewall_source_ip', 'firewall_destination_ip']

        logging.info(f"\nAttempting to merge {fw_name} and {ids_name} on columns: {merge_on}")
        try:
            merged_cross = dd.merge(
                fw_df,
                ids_df,
                left_on=['firewall_source_ip', 'firewall_destination_ip'],
                right_on=['ids_sourceip', 'ids_destip'],
                how='inner'  # Change to 'outer', 'left', or 'right' as needed
            )
            merged_cross_shape = merged_cross.shape.compute()
            logging.info(f"Resulting Cross-Dataset Merged DataFrame has {merged_cross_shape[0]} rows and {merged_cross_shape[1]} columns.\n")
            logging.info("Sample of Cross-Dataset Merged DataFrame:")
            logging.info(merged_cross.head().compute())
        except Exception as e:
            logging.error(f"Error during cross-dataset merging: {e}\n")
    else:
        logging.error(f"One of the datasets '{fw_name}' or '{ids_name}' is missing for cross-dataset merging.\n")

    # Additional analyses can be added here

if __name__ == "__main__":
    main()
