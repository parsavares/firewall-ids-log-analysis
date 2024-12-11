import os
import dask.dataframe as dd
import pandas as pd
import numpy as np
import re

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
CLEANED_PREFIX = 'cleaned_'

# --------------------------- Helper Functions ---------------------------

def trim_column_names(df):
    """
    Trims leading and trailing whitespace from column names.
    
    Parameters:
    - df: Dask DataFrame
    
    Returns:
    - df: Dask DataFrame with trimmed column names
    """
    df.columns = df.columns.str.strip()
    return df

def trim_data_whitespace(df):
    """
    Trims leading and trailing whitespace from string columns in the DataFrame.
    
    Parameters:
    - df: Dask DataFrame
    
    Returns:
    - df: Dask DataFrame with trimmed string data
    """
    # Identify object (string) columns
    obj_columns = df.select_dtypes(['object']).columns
    for col in obj_columns:
        df[col] = df[col].str.strip()
    return df

def handle_missing_values(df, strategy='inspect', fill_value='Unknown'):
    """
    Handles missing values in the dataset based on the specified strategy.
    
    Parameters:
    - df: Dask DataFrame
    - strategy: str, options include 'drop', 'fill', 'inspect'
    - fill_value: str, value to replace missing entries if strategy is 'fill'
    
    Returns:
    - df: Dask DataFrame with missing values handled (if 'drop' or 'fill')
    - missing_summary: Pandas DataFrame summarizing missing values before any imputation
    """
    # Compute missing values
    missing_counts = df.isnull().sum().compute()
    total_rows = df.shape[0].compute()
    missing_percent = (missing_counts / total_rows) * 100
    missing_summary = pd.DataFrame({
        'Missing Count': missing_counts,
        'Missing Percentage': missing_percent
    })
    
    # Handle according to strategy
    if strategy == 'drop':
        df = df.dropna()
    elif strategy == 'fill':
        df = df.fillna(fill_value)
    # If strategy is 'inspect', do not modify the DataFrame
    
    return df, missing_summary

def remove_duplicates(df):
    """
    Removes duplicate rows from the dataset.
    
    Parameters:
    - df: Dask DataFrame
    
    Returns:
    - df: Dask DataFrame without duplicates
    """
    df = df.drop_duplicates()
    return df

def standardize_column_names(name, df):
    """
    Standardizes column names to ensure consistency across datasets.
    
    Parameters:
    - name: str, name of the dataset
    - df: Dask DataFrame
    
    Returns:
    - df: Dask DataFrame with standardized column names
    """
    if 'Firewall' in name:
        # For Firewall datasets, ensure consistent casing and spacing
        df = trim_column_names(df)
    elif 'IDS' in name:
        # For IDS datasets, rename columns to match Firewall datasets
        rename_dict = {
            'sourceIP': 'Source IP',
            'sourcePort': 'Source Port',
            'destIP': 'Destination IP',
            'destPort': 'Destination Port',
            'time': 'Date/time'
        }
        df = trim_column_names(df)
        df = df.rename(columns=rename_dict)
    return df

def inspect_extra_spaces(df):
    """
    Inspects and counts extra spaces within string columns.
    
    Parameters:
    - df: Dask DataFrame
    
    Returns:
    - extra_space_summary: Pandas DataFrame summarizing extra spaces per column
    """
    obj_columns = df.select_dtypes(['object']).columns
    extra_space_counts = {}
    
    for col in obj_columns:
        # Count entries where leading or trailing spaces exist
        has_extra_spaces = df[col].str.contains(r'^\s+|\s+$', regex=True, na=False)
        count = has_extra_spaces.sum().compute()
        if count > 0:
            extra_space_counts[col] = count
    
    extra_space_summary = pd.DataFrame.from_dict(extra_space_counts, orient='index', columns=['Extra Spaces Count'])
    return extra_space_summary

def impute_missing_values(df):
    """
    Imputes missing values in the dataset using the behavior of Source IP / Destination IP for previous entries.
    For numerical columns, fill with previous values from the same Source IP or Destination IP.
    For categorical columns, fill with most frequent value from the same Source IP or Destination IP.
    
    Parameters:
    - df: Dask DataFrame
    
    Returns:
    - df: Dask DataFrame with imputed values
    """
    # Identify numerical and categorical columns
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
    categorical_cols = df.select_dtypes(include=['object']).columns

    # For large datasets, imputation can be expensive. This is a conceptual example.
    # Impute numerical columns using forward fill grouped by IPs
    for col in numerical_cols:
        df[col] = df.groupby('Source IP')[col].fillna(method='ffill')
        df[col] = df.groupby('Destination IP')[col].fillna(method='ffill')
    
    # Impute categorical columns. Forward fill first, then mode if still missing.
    for col in categorical_cols:
        df[col] = df.groupby('Source IP')[col].fillna(method='ffill')
        df[col] = df.groupby('Destination IP')[col].fillna(method='ffill')
        # If still missing, fill with mode per Source IP group
        mode_value = df.groupby('Source IP')[col].agg(lambda x: x.mode()[0] if not x.mode().empty else 'Unknown')
        df[col] = df[col].fillna(mode_value)
    
    return df

def analyze_and_clean_dataset(name, path, strategy='inspect', impute=False):
    """
    Analyzes and cleans a single dataset, then returns its summary.
    
    Parameters:
    - name: str, name of the dataset file
    - path: str, relative path to the dataset file
    - strategy: str, strategy to handle missing values ('inspect', 'drop', 'fill')
    - impute: bool, whether to perform imputation after inspection
    
    Returns:
    - summary: str, formatted summary of the dataset
    - cleaned_path: str, path to the cleaned dataset
    """
    summary = f"Dataset: {name}\n"
    summary += f"Path: {path}\n"

    try:
        # Read the dataset using Dask with na_values
        na_values_list = ["(empty)", "N/A", "NULL", "?", "Unknown"]  # Add more representations as needed
        df = dd.read_csv(
            path,
            assume_missing=True,
            dtype=str,
            na_values=na_values_list,
            keep_default_na=True,  # Retain default NaN values
            on_bad_lines='skip'    # Handle bad lines gracefully
        )
        print(f"Loaded dataset: {name}")

        # Trim whitespace from column names
        df = trim_column_names(df)

        # Trim whitespace from string data
        df = trim_data_whitespace(df)

        # Handle missing values based on the chosen strategy
        df, missing_summary_before_imputation = handle_missing_values(df, strategy=strategy)
        summary += f"Number of Rows (after handling missing values): {df.shape[0].compute()}\n"
        summary += f"Missing Values Summary (Before Imputation):\n{missing_summary_before_imputation}\n"

        # If imputation is requested, compare before and after imputation
        if impute:
            # Record missing values before imputation
            before_counts = missing_summary_before_imputation['Missing Count']
            before_percent = missing_summary_before_imputation['Missing Percentage']

            # Perform imputation
            df = impute_missing_values(df)
            summary += "Missing values imputed based on previous behavior of Source IP / Destination IP.\n"

            # Now re-check missing values after imputation
            after_missing_counts = df.isnull().sum().compute()
            total_rows = df.shape[0].compute()
            after_missing_percent = (after_missing_counts / total_rows) * 100
            after_summary = pd.DataFrame({
                'Missing Count (After)': after_missing_counts,
                'Missing % (After)': after_missing_percent
            })

            # Combine before and after into a comparison
            comparison = pd.DataFrame({
                'Missing Count (Before)': before_counts,
                'Missing % (Before)': before_percent
            }).join(after_summary, how='outer')

            # Calculate differences
            comparison['Count Difference'] = comparison['Missing Count (Before)'] - comparison['Missing Count (After)']
            comparison['% Difference'] = comparison['Missing % (Before)'] - comparison['Missing % (After)']

            # Add this comparison to the summary
            summary += "Comparison of Missing Values Before and After Imputation:\n"
            summary += f"{comparison}\n"

        # Standardize column names (after all missing handling steps)
        df = standardize_column_names(name, df)

        # Update columns after standardization
        columns = df.columns.tolist()
        summary += f"Columns: {', '.join(columns)}\n"

        # Get data types of each column
        dtypes = df.dtypes
        dtype_info = ', '.join([f"{col}: {dtype}" for col, dtype in dtypes.items()])
        summary += f"Data Types: {dtype_info}\n"

        # Save the cleaned dataset
        cleaned_filename = f"{CLEANED_PREFIX}{name}"
        cleaned_path = os.path.join(os.path.dirname(path), cleaned_filename)
        df.to_csv(cleaned_path, single_file=True, index=False)
        summary += f"Cleaned dataset saved as: {cleaned_filename}\n"

    except Exception as e:
        summary += f"Error processing dataset: {e}\n"
        cleaned_path = None

    summary += "-" * 50 + "\n"
    return summary, cleaned_path

# --------------------------- Main Execution ---------------------------

def main():
    """
    Main function to analyze, clean, and prepare datasets for further analysis.
    """
    # Initialize an empty string to hold all summaries
    all_summaries = "Dataset Analysis, Cleaning, and Inspection Summary\n"
    all_summaries += "=" * 50 + "\n\n"

    # Dictionary to hold cleaned datasets for integration
    cleaned_datasets = {}

    # Iterate over each dataset and analyze & clean
    for name, path in DATASETS.items():
        # Check if the file exists
        if not os.path.exists(path):
            all_summaries += f"Dataset: {name}\nPath: {path}\nError: File does not exist.\n"
            all_summaries += "-" * 50 + "\n"
            continue

        # Analyze and clean the dataset with imputation set to True to see before/after differences
        summary, cleaned_path = analyze_and_clean_dataset(name, path, strategy='inspect', impute=True)
        all_summaries += summary

        # Store the path of the cleaned dataset for integration
        if cleaned_path:
            cleaned_datasets[name] = cleaned_path

    # Save all summaries to the output file
    output_path = os.path.join(os.path.dirname(__file__), OUTPUT_FILE)
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(all_summaries)
        print(f"Dataset analysis and cleaning complete. Summary saved to '{OUTPUT_FILE}'.")
    except Exception as e:
        print(f"Failed to write summary to '{OUTPUT_FILE}': {e}")

    # ----------------------- Inspect Extra Spaces -----------------------
    # Identify and summarize extra spaces in cleaned datasets

    extra_space_summary_total = "Extra Spaces Inspection Summary\n"
    extra_space_summary_total += "=" * 50 + "\n\n"

    for name, cleaned_path in cleaned_datasets.items():
        try:
            df = dd.read_csv(cleaned_path, assume_missing=True, dtype=str, on_bad_lines='skip')
            extra_spaces = inspect_extra_spaces(df)
            if not extra_spaces.empty:
                extra_space_summary_total += f"Dataset: {cleaned_path}\n"
                extra_space_summary_total += f"Columns with Extra Spaces:\n{extra_spaces}\n"
                extra_space_summary_total += "-" * 50 + "\n"
            else:
                extra_space_summary_total += f"Dataset: {cleaned_path}\nNo extra spaces detected in string columns.\n"
                extra_space_summary_total += "-" * 50 + "\n"
        except Exception as e:
            extra_space_summary_total += f"Dataset: {cleaned_path}\nError inspecting extra spaces: {e}\n"
            extra_space_summary_total += "-" * 50 + "\n"

    # Append extra spaces summary to the output file
    try:
        with open(output_path, 'a', encoding='utf-8') as f:
            f.write(extra_space_summary_total)
        print("Extra spaces inspection complete. Summary appended to the summary file.")
    except Exception as e:
        print(f"Failed to append extra spaces summary to '{OUTPUT_FILE}': {e}")

    # ----------------------- Handling Extra Spaces -----------------------
    # After inspection, decide how to handle extra spaces
    # For demonstration, we'll remove extra spaces from string columns

    all_summaries_spaces_handled = "Extra Spaces Handling Summary\n"
    all_summaries_spaces_handled += "=" * 50 + "\n\n"

    for name, cleaned_path in cleaned_datasets.items():
        try:
            df = dd.read_csv(cleaned_path, assume_missing=True, dtype=str, on_bad_lines='skip')
            obj_columns = df.select_dtypes(['object']).columns
            for col in obj_columns:
                # Remove leading and trailing spaces
                df[col] = df[col].str.strip()
            # Save the cleaned dataset again
            cleaned_path_no_spaces = cleaned_path  # Already trimmed, no need to change path
            df.to_csv(cleaned_path_no_spaces, single_file=True, index=False)
            all_summaries_spaces_handled += f"Extra spaces removed from '{cleaned_path}'.\n"
        except Exception as e:
            all_summaries_spaces_handled += f"Error handling extra spaces in '{cleaned_path}': {e}\n"

    # Append spaces handling summary to the output file
    try:
        with open(output_path, 'a', encoding='utf-8') as f:
            f.write(all_summaries_spaces_handled)
        print("Extra spaces handling complete. Summary appended to the summary file.")
    except Exception as e:
        print(f"Failed to append extra spaces handling summary to '{OUTPUT_FILE}': {e}")

    # ----------------------- Future Steps -----------------------
    # Additional custom analyses, advanced imputations, or further feature engineering
    # can be applied here as needed.

if __name__ == "__main__":
    main()
