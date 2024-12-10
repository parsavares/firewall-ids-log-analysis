import dask.dataframe as dd

# Path to a cleaned dataset
cleaned_firewall = '..\\data\\MC2-CSVFirewallandIDSlogs\\cleaned_Firewall-04062012.csv'

# Load the cleaned dataset
df_cleaned = dd.read_csv(cleaned_firewall, assume_missing=True, dtype=str, on_bad_lines='skip')

# Check for missing values
missing_counts = df_cleaned.isnull().sum().compute()
print(missing_counts)

# Sample a few rows
sample = df_cleaned.head(10)
print(sample)