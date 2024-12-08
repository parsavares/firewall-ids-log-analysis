import utils
import json

class Heatmap:

    def get_heatmap_data():
        
        df = utils.load_csv("/home/df/Documenti/Universita/HPDA/firewall-ids-log-analysis/data/Firewall-04062012.csv")
        heatmap_data = df.groupby('Source IP')['Destination IP'].value_counts().unstack(fill_value=0)

        df['Source Subnet'] = df['Source IP'].apply(lambda x: '.'.join(x.split('.')[:3]) + '.0/24')
        df['Destination Subnet'] = df['Destination IP'].apply(lambda x: '.'.join(x.split('.')[:3]) + '.0/24')
        heatmap_data = df.groupby('Source Subnet')['Destination Subnet'].value_counts().unstack(fill_value=0)

        melted_data = []
        for i in range(len(heatmap_data)):
            for j in range(len(heatmap_data.columns)):
                melted_data.append({
                    'xAttribute': heatmap_data.index[i],
                    'yAttribute': heatmap_data.columns[j],
                    'frequency': int(heatmap_data.iat[i, j])
                })

        #print(melted_data) 

        return json.dumps(melted_data)