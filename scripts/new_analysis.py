import pandas as pd
import numpy as np
import re
from ipwhois import IPWhois
from ipaddress import ip_address, ip_network


#this function classify the ip
def classify_ip(ip):
    try:
        ip_obj = ip_address(ip)
    except ValueError:
        # If the IP address is invalid, return NaN
        return "NaN"
    
    
    # Check if the IP is in the specific '172.23.X.X' range (private network of the bank)
    if ip_obj in ip_network('172.23.0.0/16'):
        if ip == '172.23.0.2':
            return "int_log_server"
        if ip == '172.23.0.10':
            return "int_dns_server"
        if ip_obj in ip_network('172.23.214.0/24'):
            return "int_financial_servers"
        if ip_obj in ip_network('172.23.229.0/24'):
            return "int_financial_servers"
        
    if ip_obj in ip_network('10.0.0.0/8'): #external websites
        return "ext_website"
    
    return "ext_dns"

def clean_firewall():
    
    #read data
    FIREWALL1 = pd.read_csv('../data/MC2-CSVFirewallandIDSlogs/Firewall-04062012.csv')
    FIREWALL2 = pd.read_csv('../data/MC2-CSVFirewallandIDSlogs/Firewall-04072012.csv')
    FIREWALL = pd.concat([FIREWALL1, FIREWALL2])
    #drop columns with only empty values
    FIREWALL = FIREWALL.drop(columns='Source hostname')
    FIREWALL = FIREWALL.drop(columns='Destination hostname')
    print(FIREWALL.head())
    
    
    
    
    
    #numer of lines in the original dataset FIREWALL
    FIREWALL = FIREWALL[~((FIREWALL['Syslog priority'] == 'Info') & 
                      (FIREWALL['Operation'] == 'Teardown') & 
                      (FIREWALL['Message code'] == 'ASA-6-305010'))]
    FIREWALL = FIREWALL[~((FIREWALL['Syslog priority'] == 'Info') & 
                      (FIREWALL['Operation'] == 'Teardown') & 
                      (FIREWALL['Message code'] == 'ASA-6-302010'))]
    FIREWALL = FIREWALL[~((FIREWALL['Syslog priority'] == 'Info') & 
                      (FIREWALL['Operation'] == 'Teardown') & 
                      (FIREWALL['Message code'] == 'ASA-6-302013'))]
    FIREWALL = FIREWALL[~((FIREWALL['Syslog priority'] == 'Info') & 
                      (FIREWALL['Operation'] == 'Teardown') & 
                      (FIREWALL['Message code'] == 'ASA-6-302015'))]
    FIREWALL = FIREWALL[~((FIREWALL['Syslog priority'] == 'Info') & 
                      (FIREWALL['Operation'] == 'Teardown') & 
                      (FIREWALL['Message code'] == 'ASA-6-302014'))]
    FIREWALL = FIREWALL[~((FIREWALL['Syslog priority'] == 'Info') & 
                      (FIREWALL['Operation'] == 'Teardown') & 
                      (FIREWALL['Message code'] == 'ASA-6-302016'))]

    print("Lines in FIREWALL Syslog priority 'Info' and Operation Teardown without code requiring actions:  ", len(FIREWALL))
    
    FIREWALL = FIREWALL[~((FIREWALL['Syslog priority'] == 'Info') & 
                      (FIREWALL['Operation'] == 'Built') & 
                      (FIREWALL['Message code'] == 'ASA-6-305009'))]
    FIREWALL = FIREWALL[~((FIREWALL['Syslog priority'] == 'Info') & 
                      (FIREWALL['Operation'] == 'Built') & 
                      (FIREWALL['Message code'] == 'ASA-6-302010'))]
    FIREWALL = FIREWALL[~((FIREWALL['Syslog priority'] == 'Info') & 
                      (FIREWALL['Operation'] == 'Built') & 
                      (FIREWALL['Message code'] == 'ASA-6-302013'))]
    FIREWALL = FIREWALL[~((FIREWALL['Syslog priority'] == 'Info') & 
                      (FIREWALL['Operation'] == 'Built') & 
                      (FIREWALL['Message code'] == 'ASA-6-302014'))]
    FIREWALL = FIREWALL[~((FIREWALL['Syslog priority'] == 'Info') & 
                      (FIREWALL['Operation'] == 'Built') & 
                      (FIREWALL['Message code'] == 'ASA-6-302015'))]
    FIREWALL = FIREWALL[~((FIREWALL['Syslog priority'] == 'Info') & 
                      (FIREWALL['Operation'] == 'Built') & 
                      (FIREWALL['Message code'] == 'ASA-6-302016'))]
    
    print("Lines in FIREWALL Syslog priority 'Info' and Operation Built without code requiring actions:  ", len(FIREWALL))
    
    
    #and now remove 'empty' fields
    #FIREWALL = FIREWALL[FIREWALL['Operation'] != '(empty)']
    #FIREWALL = FIREWALL[FIREWALL['Protocol'] != '(empty)']
    #FIREWALL = FIREWALL[FIREWALL['Direction'] != '(empty)']

    
    #change the name of column Date/time and Date_time
    FIREWALL.rename(columns={'Date/time': 'Date_time'}, inplace=True)
    
    # split the Date/time column into two columns
    FIREWALL[['Date', 'Time']] = FIREWALL['Date_time'].str.split(' ', expand=True)
    
    #change the Date format in the dataset
    FIREWALL['Date'] = pd.to_datetime(FIREWALL['Date'])
    
    #assign a category to the IPs
    FIREWALL['cat_src'] = FIREWALL['Source IP'].apply(classify_ip)
    FIREWALL['cat_dst'] = FIREWALL['Destination IP'].apply(classify_ip)

    # Clean the 'Destination Service' column
    FIREWALL['Destination service'] = FIREWALL['Destination service'].apply(lambda x: x.split('_')[-1] if pd.notnull(x) else x)

    print("Lines in FIREWALL  ", len(FIREWALL))
    
    print("LINES Syslog priority 'Info' and with Operation 'Built':  ", ((FIREWALL['Syslog priority'] == 'Info') & (FIREWALL['Operation'] == 'Built')).sum())
    print("LINES Syslog priority 'Info' and with Operation 'Teardown':  ", ((FIREWALL['Syslog priority'] == 'Info') & (FIREWALL['Operation'] == 'Teardown')).sum())
    print("LINES Syslog priority 'Info' and with Operation '(empty)':  ", ((FIREWALL['Syslog priority'] == 'Info') & (FIREWALL['Operation'] == '(empty)')).sum())
    print("LINES Syslog priority 'Info' and with Operation 'Command executed':  ", ((FIREWALL['Syslog priority'] == 'Info') & (FIREWALL['Operation'] == 'Command executed')).sum())
    print("LINES Syslog priority 'Info' and with Operation 'Deny':  ", ((FIREWALL['Syslog priority'] == 'Info') & (FIREWALL['Operation'] == 'Deny')).sum())
    print("LINES Syslog priority 'Info' and with Operation 'Deny by ACL':  ", ((FIREWALL['Syslog priority'] == 'Info') & (FIREWALL['Operation'] == 'Deny by ACL')).sum())
    
    # Rename columns to remove spaces, replace with underscores, and convert to lower case
    FIREWALL.columns = FIREWALL.columns.str.replace(' ', '_').str.lower()

    FIREWALL.to_csv('../data/MC2-CSVFirewallandIDSlogs/FIREWALL.csv')
    
    
    
    #Statistics on firewall
    '''
    #Syslog priority: Syslog priority: ['Info' 'Notice' 'Critical' 'Warning' 'Error']
    print("LINES with Syslog priority 'Info':  ", (FIREWALL['Syslog priority'] == 'Info').sum())
    print("LINES with Syslog priority 'Notice':  ", (FIREWALL['Syslog priority'] == 'Notice').sum())
    print("LINES with Syslog priority 'Critical':  ", (FIREWALL['Syslog priority'] == 'Critical').sum())
    print("LINES with Syslog priority 'Warning':  ", (FIREWALL['Syslog priority'] == 'Warning').sum())
    print("LINES with Syslog priority 'Error':  ", (FIREWALL['Syslog priority'] == 'Error').sum())
    
    #Operation: ['Teardown' 'Built' '(empty)' 'Command executed' 'Deny' 'Deny by ACL']
    print("LINES with Operation 'Teardown':  ", (FIREWALL['Operation'] == 'Teardown').sum())
    print("LINES with Operation 'Built':  ", (FIREWALL['Operation'] == 'Built').sum()) #sum 23090019
    print("LINES with Operation '(empty)':  ", (FIREWALL['Operation'] == '(empty)').sum())
    print("LINES with Operation 'Command executed':  ", (FIREWALL['Operation'] == 'Command executed').sum())
    print("LINES with Operation 'Deny':  ", (FIREWALL['Operation'] == 'Deny').sum())
    print("LINES with Operation 'Deny by ACL':  ", (FIREWALL['Operation'] == 'Deny by ACL').sum())
    
    #Info with different types of operation
    print("LINES Syslog priority 'Info' and with Operation 'Built':  ", ((FIREWALL['Syslog priority'] == 'Info') & (FIREWALL['Operation'] == 'Built')).sum())
    print("LINES Syslog priority 'Info' and with Operation 'Teardown':  ", ((FIREWALL['Syslog priority'] == 'Info') & (FIREWALL['Operation'] == 'Teardown')).sum())
    print("LINES Syslog priority 'Info' and with Operation '(empty)':  ", ((FIREWALL['Syslog priority'] == 'Info') & (FIREWALL['Operation'] == '(empty)')).sum())
    print("LINES Syslog priority 'Info' and with Operation 'Command executed':  ", ((FIREWALL['Syslog priority'] == 'Info') & (FIREWALL['Operation'] == 'Command executed')).sum())
    print("LINES Syslog priority 'Info' and with Operation 'Deny':  ", ((FIREWALL['Syslog priority'] == 'Info') & (FIREWALL['Operation'] == 'Deny')).sum())
    print("LINES Syslog priority 'Info' and with Operation 'Deny by ACL':  ", ((FIREWALL['Syslog priority'] == 'Info') & (FIREWALL['Operation'] == 'Deny by ACL')).sum())
    
    #Info + Built + Message code which not requires actions
    print("LINES Syslog priority 'Info' and with Operation 'Built + ASA-6-302013':  ", ((FIREWALL['Syslog priority'] == 'Info') & (FIREWALL['Operation'] == 'Built') &(FIREWALL['Message code'] == 'ASA-6-302013')).sum())
    
    #Info + Teardown + Message code which not requires actions
    print("LINES Syslog priority 'Info' and with Operation 'Teardown + ASA-6-302010':  ", ((FIREWALL['Syslog priority'] == 'Info') & (FIREWALL['Operation'] == 'Teardown') &(FIREWALL['Message code'] == 'ASA-6-302010')).sum())
    print("LINES Syslog priority 'Info' and with Operation 'Teardown + ASA-6-302013':  ", ((FIREWALL['Syslog priority'] == 'Info') & (FIREWALL['Operation'] == 'Teardown') &(FIREWALL['Message code'] == 'ASA-6-302013')).sum())
    print("LINES Syslog priority 'Info' and with Operation 'Teardown + ASA-6-302014':  ", ((FIREWALL['Syslog priority'] == 'Info') & (FIREWALL['Operation'] == 'Teardown') &(FIREWALL['Message code'] == 'ASA-6-302014')).sum())
    print("LINES Syslog priority 'Info' and with Operation 'Teardown + ASA-6-302015':  ", ((FIREWALL['Syslog priority'] == 'Info') & (FIREWALL['Operation'] == 'Teardown') &(FIREWALL['Message code'] == 'ASA-6-302015')).sum())
    print("LINES Syslog priority 'Info' and with Operation 'Teardown + ASA-6-302016':  ", ((FIREWALL['Syslog priority'] == 'Info') & (FIREWALL['Operation'] == 'Teardown') &(FIREWALL['Message code'] == 'ASA-6-302016')).sum())
    
    print("Lines in FIREWALL:  ", len(FIREWALL))
    print("LINES Syslog priority 'Info' and with Operation 'Teardown + ASA-6-302014':  ", 
          ((FIREWALL['Syslog priority'] == 'Info') & 
           (FIREWALL['Operation'] == 'Teardown') &
           (FIREWALL['Message code'] == 'ASA-6-302014')).sum())
    print("LINES Syslog priority 'Info' and with Operation 'Teardown + ASA-6-302014':  ", 
          ((FIREWALL['Syslog priority'] == 'Info') & 
           (FIREWALL['Operation'] == 'Teardown') &
           (FIREWALL['Message code'] == 'ASA-6-302016')).sum())
           
    #considering this statistics we start to cut
    #df = df.drop(df[(df.score < 50) & (df.score > 20)].index)
    '''
    return

def clean_ids():
    IDS1 = pd.read_csv('../data/MC2-CSVFirewallandIDSlogs/IDS-0406.csv')
    IDS2 = pd.read_csv('../data/MC2-CSVFirewallandIDSlogs/IDS-0407.csv')
    IDS = pd.concat([IDS1, IDS2])

    print(IDS.head())
    
    print("lines in the original IDS datset: ", len(IDS))
    
    # Remove white spaces from column names
    IDS.columns = IDS.columns.str.replace(' ', '')

    #change the Date format in the dataset
    IDS.rename(columns={"time": "date_time", "sourceIP": "source_ip", "destIP": "dest_ip", "sourcePort": "source_port", "destPort": "destination_port", "packetinfocont'd": "packetinfo_2"}, inplace=True) 
    IDS['date_time'] = pd.to_datetime(IDS['date_time'])
    #assign a category to the IPs
    IDS['cat_src'] = IDS['source_ip'].apply(classify_ip)
    IDS['cat_dst'] = IDS['dest_ip'].apply(classify_ip)

    # To lowercase 
    IDS.columns = IDS.columns.str.lower()


    IDS.to_csv('../data/MC2-CSVFirewallandIDSlogs/IDS.csv')
    
    
    '''
    #print("lines in IDS with NaN as label", (IDS[' label'] == 'NaN').sum())
    print("lines in IDS with NaN as label", IDS[' label'].isna().sum())
    print("lines in IDS with with priority minimum", (IDS[' priority'] == 3).sum())
    
    # Get the value that appears most frequently and its count
    most_common_value = IDS[' classification'].value_counts().idxmax()
    count_of_most_common = IDS[' classification'].value_counts().max()

    # Print the results
    print(f"The most frequent value in 'classification' is '{most_common_value}' with {count_of_most_common} occurrences.")
    print("lines in IDS with with priority minimum and generic command decode", ((IDS[' classification'] == ' Generic Protocol Command Decode') & (IDS[' priority'] == 3)).sum())
    print("lines in IDS with MISC activity", (IDS[' classification'] == ' Misc activity').sum())
    print("lines in IDS with with priority minimum and MISC activity", ((IDS[' classification'] == ' Misc activity') & (IDS[' priority'] == 3)).sum())
    #we can ignore priority equal to 3 (the lowest)
    # Filter the DataFrame to exclude specified classifications
    
    # Filter rows where classification is 'Generic Protocol Command Decode'
    filtered_data = IDS[IDS[' classification'] == ' Generic Protocol Command Decode']

    # Find the most common value in the 'label' column
    most_common_label = filtered_data[' label'].value_counts().idxmax()
    count_most_common = filtered_data[' label'].value_counts().max()

    # Print the result
    #print(f"The most frequent value in 'label' for classification 'Generic Protocol Command Decode' is '{most_common_label}' with {count_most_common} occurrences.")
    # Filter rows where classification is 'Generic Protocol Command Decode'
    filtered_data_1 = IDS[IDS[' classification'] == ' Generic Protocol Command Decode']
    # Count the occurrences of each unique value in the 'label' column
    label_counts_1 = filtered_data_1[' label'].value_counts()
    # Print the result
    print("Value counts in 'label' for classification 'Generic Protocol Command Decode':")
    print(label_counts_1)

    filtered_data_2 = IDS[IDS[' classification'] == ' Misc activity']
    # Count the occurrences of each unique value in the 'label' column
    label_counts_2 = filtered_data_2[' label'].value_counts()
    # Print the result
    print("Value counts in 'label' for classification 'Misc activity':")
    print(label_counts_2)
    
    
    
    #IDS = IDS[~((IDS[' classification'] == ' Generic Protocol Command Decode') | (IDS[' classification'] == ' Misc activity'))]

    # Print the number of remaining rows
    #print("Lines in the IDS dataset: ", len(IDS))
    '''

    return

def main():
    
    #clean_firewall()
    clean_ids()
    return

if __name__ == "__main__":
    main()