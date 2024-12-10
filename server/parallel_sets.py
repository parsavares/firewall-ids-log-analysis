import pandas as pd
from utils import handle_subnets

class ParallelSets:


    def get_parallel_sets_data(self, df: pd.DataFrame, subnet_bits: int):
        assert(df is not None)

        modified_df, x, y = handle_subnets(df, 'Source IP', 'Destination IP', subnet_bits)

        print("Length of parallel sets data: ", len(modified_df))
        modified_df = modified_df[["Syslog priority", "Message code", "Source IP Subnet", "Destination port"]]
        return modified_df.to_json(orient='records')

