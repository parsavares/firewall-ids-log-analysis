import pandas as pd

def main():
    # Load the data
    data1 = pd.read_csv('../data/Firewall-04062012.csv')
    data2 = pd.read_csv('../data/Firewall-04072012.csv')

    data = pd.concat([data1, data2])
    n = 1000
    #data = pd.read_csv('../data/Firewall-04062012.csv', nrows=n)

    # Retrieve the categorical values for each column

    #categorical_values = {col: data[col].unique() for col in data.columns}
    protocol_values = data['Protocol'].unique()
    categorical_attributes = [
    'Syslog priority', 
    'Operation', 
    'Message code', 
    'Protocol', 
    'Source IP', 
    'Destination IP',
    'Source hostname',
    'Destination hostname',
    'Source port',
    'Destination port',
    'Direction',
    'Connections built',
    'Connections torn down'] 

    categorical_unique_values = {col: data[col].unique() for col in categorical_attributes}


    for key, value in categorical_unique_values.items():
        if len(value) < 25:
            print(f'{key}: {value}')

    # Drop the rows with missing values
#    data = data.dropna()
    # Save the cleaned data


    #data.to_csv('data/firewall_ids_cleaned.csv', index=False)

if __name__ == '__main__':
    main()
