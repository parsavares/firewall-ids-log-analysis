import pandas as pd

class DataHandler: 

    def __init__(self):
        self.df = None

    def get_dataframe(self, start_datetime_str=None, end_datetime_str=None):

        assert(self.df is not None)

        print(self.df["date_time"][0])
        print(pd.to_datetime(start_datetime_str))
        
        if start_datetime_str and end_datetime_str:

            # !! @TODO: This is a temporary fix, we need to handle different date formats
            date_column = 'date_time'  # Change this to match the actual column name in your CSV
            mask = (pd.to_datetime(self.df[date_column]) >= pd.to_datetime(start_datetime_str)) & (pd.to_datetime(self.df[date_column]) <= pd.to_datetime(end_datetime_str))
            return self.df.loc[mask]

        return self.df

    def load_csv(self, file_path, num_rows=None):
        """
        Load a CSV file into a pandas DataFrame.

        Parameters:
        file_path (str): The path to the CSV file.

        Returns:
        DataFrame: The loaded pandas DataFrame.
        """
        try:
            if(num_rows):
                self.df = pd.read_csv(file_path, nrows=num_rows)
            else:
                self.df = pd.read_csv(file_path)
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            return None