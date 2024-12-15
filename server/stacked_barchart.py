import pandas as pd

class StackedBarchart:


    def get_stacked_barchart_data(self, df: pd.DataFrame, yAttribute: str):

        assert(df is not None)
        df['date_time_objs'] = pd.to_datetime(df['date_time'])
        df['date_bin'] = pd.cut(df['date_time_objs'], bins=150)
        bins = df.groupby(['date_bin', yAttribute]).size().unstack(fill_value=0)

        result = []
        for date_bin, group in bins.iterrows():
            occurrences = group.to_dict()
            total_occurrences = sum(occurrences.values())

            interval_data = {
                'interval_center': date_bin.mid,
                'occurrences': occurrences,
                'total_occurrences': total_occurrences
            }
            result.append(interval_data)
        
        grouped = result

        return grouped

