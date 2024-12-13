import pandas as pd
from utils import handle_subnets

class ParallelSets:


    def get_parallel_sets_data(self, df: pd.DataFrame, subnet_bits: int):
        assert(df is not None)

        modified_df, x, y = handle_subnets(df, 'source_ip', 'destination_ip', subnet_bits)

        print("Length of parallel sets data: ", len(modified_df))
        modified_df = modified_df[["syslog_priority", "cat_src", "cat_dst", "destination_service"]]
        return modified_df.to_json(orient='records')

