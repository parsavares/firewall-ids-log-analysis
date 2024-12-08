import pandas as pd



def load_csv(file_path, num_rows=None):
    """
    Load a CSV file into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    DataFrame: The loaded pandas DataFrame.
    """
    try:
        if(num_rows):
            df = pd.read_csv(file_path, nrows=num_rows)
        else:
            df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None