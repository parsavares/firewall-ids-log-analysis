import pandas as pd
from utils import handle_subnets

class ParallelSets:


    def get_parallel_sets_data(self, df: pd.DataFrame, subnet_bits: int):
        assert(df is not None)

        attrs = ['syslog_priority', 'cat_src', 'cat_dst', 'destination_service']
        modified_df = df
        if('source_ip' in attrs or 'destination_ip' in attrs):
            modified_df, x, y = handle_subnets(df, 'source_ip', 'destination_ip', subnet_bits)

        grouped_df = modified_df.groupby(attrs).size().reset_index(name='count')
        print("Length of parallel sets data: ", len(grouped_df))
        attrs.append('count')
        grouped_df = grouped_df[attrs]
        return grouped_df.to_json(orient='records')

