import pandas as pd
from utils import handle_subnets
import json

class SankeDiagram:


    def get_sanke_diagram_data(self, df: pd.DataFrame, subnet_bits: int):
        assert(df is not None)

        attrs = ['syslog_priority', 'cat_src', 'cat_dst', 'destination_service', 'protocol']
        modified_df = df
        if('source_ip' in attrs or 'destination_ip' in attrs):
            modified_df, x, y = handle_subnets(df, 'source_ip', 'destination_ip', subnet_bits)

        modified_df = modified_df[modified_df['syslog_priority'] != 'Info']
        sanke_matrix = []
        for i in range(len(attrs)-1):
            tmp = modified_df.groupby([attrs[i], attrs[i+1]]).size().reset_index(name='count')
            for index, row in tmp.iterrows():

                sanke_matrix.append({
                    "source": row[attrs[i]]+"_"+str(i),
                    "target": row[attrs[i+1]]+"_"+str(i+1),
                    "value": row['count']
                })  

        print(sanke_matrix)
        return json.dumps(sanke_matrix)

        '''
        grouped_df = modified_df.groupby(attrs).size().reset_index(name='count')
        print("Length of parallel sets data: ", len(grouped_df))
        attrs.append('count')
        grouped_df = grouped_df[attrs]
        return grouped_df.to_json(orient='records')
        '''
