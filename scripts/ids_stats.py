import pandas as pd

def main():
    # Load the data
    data1 = pd.read_csv('../data/IDS-0406.csv')
    data2 = pd.read_csv('../data/IDS-0407.csv')

    data = pd.concat([data1, data2])

    print(data.head())
    # Retrieve the categorical values for each column

    categorical_unique_values = {col: data[col].unique() for col in data.columns}

    for key, value in categorical_unique_values.items():
        print(f'{key}: {len(value)}')
    
    for key, value in categorical_unique_values.items():
        if len(value) < 100:
            print(f'{key}: {value}')
    


if __name__ == '__main__':
    main()
