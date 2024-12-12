import pandas as pd

class StackedBarchart:


    def get_stacked_barchart_data_2(self, df: pd.DataFrame, yAttribute: str):

        df['date_time_objs'] = pd.to_datetime(df['date_time'])
        df['date_bin'] = pd.cut(df['date_time_objs'], bins=100)
        bins = df.groupby(['date_bin', yAttribute]).size().unstack(fill_value=0)

        result = []
        for date_bin, group in bins.iterrows():
            occurrences = group.to_dict()
            total_occurrences = sum(occurrences.values())

            interval_data = {
                'interval_center': date_bin.left.strftime('%Y-%m-%d %H:%M:%S') + ' - ' + date_bin.right.strftime('%Y-%m-%d %H:%M:%S'),
                'occurrences': occurrences,
                'total_occurrences': total_occurrences
            }
            result.append(interval_data)
        
        grouped = result

        return grouped

    def get_stacked_barchart_data(self, df: pd.DataFrame, xAttribute: str, yAttribute: str):
        assert(df is not None)
        assert(xAttribute is not None)
        assert(yAttribute is not None)

        # Not supported yet, not very useful
        assert(xAttribute not in ['destination_ip', 'source_ip'] or yAttribute not in ['destination_ip', 'source_ip'])
        assert(xAttribute not in ['destination_port', 'source_port'] or yAttribute not in ['destination_port', 'source_port'])

        json_data = df[[xAttribute, yAttribute]].to_json(orient='records')
        return json_data