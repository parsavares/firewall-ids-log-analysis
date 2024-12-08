import os
import dask.dataframe as dd

# --------------------------- Configuration ---------------------------

# Define the relative path to the data directory from the 'scripts' folder
DATA_DIR = os.path.join('..', 'data', 'MC2-CSVFirewallandIDSlogs')

# Define the paths to each dataset
FIREWALL_FILE_1 = os.path.join(DATA_DIR, 'Firewall-04062012.csv')
FIREWALL_FILE_2 = os.path.join(DATA_DIR, 'Firewall-04072012.csv')
IDS_FILE_1 = os.path.join(DATA_DIR, 'IDS-0406.csv')
IDS_FILE_2 = os.path.join(DATA_DIR, 'IDS-0407.csv')

# List of datasets to analyze with their descriptive names
DATASETS = {
    'Firewall-04062012.csv': FIREWALL_FILE_1,
    'Firewall-04072012.csv': FIREWALL_FILE_2,
    'IDS-0406.csv': IDS_FILE_1,
    'IDS-0407.csv': IDS_FILE_2
}

# Define the output file path (saved in the same 'scripts' folder)
OUTPUT_FILE = 'dataset_summary.txt'

# --------------------------- Helper Functions ---------------------------

def analyze_dataset(name, path):
    """
    Analyzes a single dataset and returns its summary.

    Parameters:
    - name: str, name of the dataset file
    - path: str, relative path to the dataset file

    Returns:
    - summary: str, formatted summary of the dataset
    """
    summary = f"Dataset: {name}\n"
    summary += f"Path: {path}\n"

    try:
        # Read the dataset using Dask
        df = dd.read_csv(path, assume_missing=True, dtype=str)  # Read all columns as string to handle mixed types

        # Compute the number of rows
        num_rows = df.shape[0].compute()
        summary += f"Number of Rows: {num_rows}\n"

        # Compute the number of columns
        num_columns = len(df.columns)
        summary += f"Number of Columns: {num_columns}\n"

        # List the column names
        columns = df.columns.tolist()
        summary += f"Columns: {', '.join(columns)}\n"

        # Get data types of each column (No compute() needed as df.dtypes is a Pandas Series)
        dtypes = df.dtypes
        dtype_info = ', '.join([f"{col}: {dtype}" for col, dtype in dtypes.items()])
        summary += f"Data Types: {dtype_info}\n"

    except Exception as e:
        summary += f"Error processing dataset: {e}\n"

    summary += "-" * 50 + "\n"
    return summary

# --------------------------- Main Execution ---------------------------

def main():
    """
    Main function to analyze all datasets and save the summary to a text file.
    """
    # Initialize an empty string to hold all summaries
    all_summaries = "Dataset Analysis Summary\n"
    all_summaries += "=" * 50 + "\n\n"

    # Iterate over each dataset and analyze
    for name, path in DATASETS.items():
        # Check if the file exists
        if not os.path.exists(path):
            all_summaries += f"Dataset: {name}\nPath: {path}\nError: File does not exist.\n"
            all_summaries += "-" * 50 + "\n"
            continue

        # Analyze the dataset and append the summary
        summary = analyze_dataset(name, path)
        all_summaries += summary

    # Define the full path for the output file
    output_path = os.path.join(os.path.dirname(__file__), OUTPUT_FILE)

    # Write all summaries to the output file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(all_summaries)
        print(f"Dataset analysis complete. Summary saved to '{OUTPUT_FILE}'.")
    except Exception as e:
        print(f"Failed to write summary to '{OUTPUT_FILE}': {e}")

# --------------------------- Entry Point ---------------------------

if __name__ == "__main__":
    main()
