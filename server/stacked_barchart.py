import pandas as pd

class StackedBarchart:


    def get_stacked_barchart_data(self, df: pd.DataFrame, xAttribute: str, yAttribute: str):
        assert(df is not None)
        assert(xAttribute is not None)
        assert(yAttribute is not None)

        # Not supported yet, not very useful
        assert(xAttribute not in ['destination_ip', 'source_ip'] or yAttribute not in ['destination_ip', 'source_ip'])
        assert(xAttribute not in ['destination_port', 'source_port'] or yAttribute not in ['destination_port', 'source_port'])

        json_data = df[[xAttribute, yAttribute]].to_json(orient='records')
        print(json_data)
        return json_data

