import pandas as pd
import ipaddress


def handle_subnets(df: pd.DataFrame, xAttribute: str, yAttribute: str, subnet_bits: int):

    # TO HANDLE!!
    df = df[(df[xAttribute] != "(empty)") & (df[yAttribute] != "(empty)")]

    xAttributeModified = xAttribute
    yAttributeModified = yAttribute
    if xAttribute in ['source_ip', 'destination_ip']:
        #df[f'{xAttribute} Subnet'] = df[xAttribute].apply(lambda x: '.'.join(x.split('.')[:3]) + '.0/' + str(subnet_bits))
        df[f'{xAttribute}_subnet'] = df[xAttribute].apply(lambda x: str(ipaddress.ip_network(f"{x}/{subnet_bits}", strict=False)))
        xAttributeModified = f'{xAttribute}_subnet'
    if yAttribute in ['source_ip', 'destination_ip']:
        df[f'{yAttribute}_subnet'] = df[yAttribute].apply(lambda x: str(ipaddress.ip_network(f"{x}/{subnet_bits}", strict=False)))
        yAttributeModified = f'{yAttribute}_subnet'

    return df, xAttributeModified, yAttributeModified

