import pandas as pd
import ipaddress


def handle_subnets(df: pd.DataFrame, xAttribute: str, yAttribute: str, subnet_bits: int):

    # TO HANDLE!!
    df = df[(df[xAttribute] != "(empty)") & (df[yAttribute] != "(empty)")]

    xAttributeModified = xAttribute
    yAttributeModified = yAttribute
    if xAttribute in ['Source IP', 'Destination IP']:
        #df[f'{xAttribute} Subnet'] = df[xAttribute].apply(lambda x: '.'.join(x.split('.')[:3]) + '.0/' + str(subnet_bits))
        df[f'{xAttribute} Subnet'] = df[xAttribute].apply(lambda x: str(ipaddress.ip_network(f"{x}/{subnet_bits}", strict=False)))
        xAttributeModified = f'{xAttribute} Subnet'
    if yAttribute in ['Source IP', 'Destination IP']:
        df[f'{yAttribute} Subnet'] = df[yAttribute].apply(lambda x: str(ipaddress.ip_network(f"{x}/{subnet_bits}", strict=False)))
        yAttributeModified = f'{yAttribute} Subnet'

    return df, xAttributeModified, yAttributeModified

