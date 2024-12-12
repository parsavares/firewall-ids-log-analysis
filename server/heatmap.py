import json
import pandas as pd
from data_handler import DataHandler
import ipaddress
from utils import handle_subnets

class Heatmap:

    def get_heatmap_data(self, df: pd.DataFrame, xAttribute: str, yAttribute: str, subnet_bits=None):

        assert(df is not None)

        print("Lenght of dataframe: ", len(df)) 
        print("Preparing heatmap data...")

        xAttributeModified = xAttribute
        yAttributeModified = yAttribute 

        # If the rwequested attributes are IP addresses, we need to group them by subnet
        if(xAttribute == 'source_ip' or xAttribute == 'destination_ip' or yAttribute == 'source_ip' or yAttribute == 'destination_ip'):
            assert subnet_bits is not None
            df, xAttributeModified, yAttributeModified = handle_subnets(df, xAttribute, yAttribute, subnet_bits)

        heatmap_data = df.groupby(xAttributeModified)[yAttributeModified].value_counts().unstack(fill_value=0)

        melted_data = [
            {
            'xAttribute': x,
            'yAttribute': y,
            'frequency': int(heatmap_data.at[x, y])
            }
            for x in heatmap_data.index
            for y in heatmap_data.columns
        ]

        print("Length of heatmap data: ", len(melted_data)) 
        print("Heatmap data prepared.")
        return json.dumps(melted_data)