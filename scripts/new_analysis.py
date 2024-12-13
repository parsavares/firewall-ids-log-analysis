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
        if ip_obj == "172.23.0.1":
            return "int_cisco_firweall"
        if ip_obj == '172.23.0.2':
            return "int_log_server"
        if ip_obj == '172.23.0.10':
            return "int_dns_server"
        if ip_obj in ip_network('172.23.214.0/24'):
            return "int_financial_servers"
        if ip_obj in ip_network('172.23.229.0/24'):
            return "int_financial_servers"
        return "int_workstation"
    
    if ip_obj == "10.32.0.100":
        return "ext_dc_firewall"
    if ip_obj == "10.32.2.100" or ip_obj == "10.32.2.101":
        return "ext_financial_server"
    if ip_obj == "10.32.0.1":
        return "ext_cisco_firewall"
    
    
    if ip_obj in ip_network('10.32.0.0/16'): #external websites
        return "ext_website"
    
    return "ext_dns"

def main():
    
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

if __name__ == "__main__":
    main()