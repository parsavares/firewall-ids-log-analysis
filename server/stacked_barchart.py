import pandas as pd

class StackedBarchart:


    def get_stacked_barchart_data(self, df: pd.DataFrame, xAttribute: str, yAttribute: str):
        assert(df is not None)
        assert(xAttribute is not None)
        assert(yAttribute is not None)

        # Not supported yet, not very useful
        assert(xAttribute not in ['Destination IP', 'Source IP'] or yAttribute not in ['Destination IP', 'Source IP'])
        assert(xAttribute not in ['Destination Port', 'Source Port'] or yAttribute not in ['Destination Port', 'Source Port'])

        json_data = df[[xAttribute, yAttribute]].to_json(orient='records')
        print(json_data)
        return json_data

