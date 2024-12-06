import pandas as pd
import pandasql as ps  # To run SQL queries on DataFrame

# Load the CSV file into a DataFrame
df = pd.read_csv('/home/df/Documenti/Universita/HPDA/ProjectData/MC2-CSVFirewallandIDSlogs/MC2-CSVFirewallandIDSlogs/Firewall-04062012.csv')

# Write a SQL query and run it on the DataFrame
query = """
SELECT 'Syslog priority', 'Operation', 'Message code'
FROM df
WHERE 'Syslog priority' = 'Error'
"""

# Execute the query
result = ps.sqldf(query)

# Display the result
print(result)
