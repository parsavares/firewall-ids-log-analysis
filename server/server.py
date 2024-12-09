from flask import Flask
from flask_cors import CORS

from heatmap import Heatmap 
from stacked_barchart import StackedBarchart

from flask import request
import pandas as pd
from data_handler import DataHandler

app = Flask(__name__)
app.debug = True

data_handler = DataHandler()

# allows cross origin to be called from localhost:3000
# not recommended in production
CORS(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/getHeatmap")
def get_heatmap():
    params = request.args
    xAttribute = params.get('xAttribute')
    yAttribute = params.get('yAttribute')
    start_datetime_str = params.get('start_datetime')
    end_datetime_str = params.get('end_datetime')
    print(params)
    assert xAttribute is not None
    assert yAttribute is not None
    assert start_datetime_str is not None
    assert end_datetime_str is not None

    # Used when dealing with IPS, so optional    
    subnet_bits = int(params.get('subnet_bits'))

    heatmap = Heatmap()
    return heatmap.get_heatmap_data(data_handler.get_dataframe(start_datetime_str, end_datetime_str), xAttribute, yAttribute, subnet_bits)

@app.route("/getStackedBarchart")
def get_stacked_barchart():
    params = request.args
    xAttribute = params.get('xAttribute')
    yAttribute = params.get('yAttribute')
    start_datetime_str = params.get('start_datetime')
    end_datetime_str = params.get('end_datetime')
    print(params)
    assert xAttribute is not None
    assert yAttribute is not None
    assert start_datetime_str is not None
    assert end_datetime_str is not None

    stacked_barchart = StackedBarchart()
    return stacked_barchart.get_stacked_barchart_data(data_handler.get_dataframe(start_datetime_str, end_datetime_str), xAttribute, yAttribute)

if __name__ == "__main__":
    print("Loading data...")
    data_handler.load_csv("/home/df/Documenti/Universita/HPDA/firewall-ids-log-analysis/data/Firewall-04062012.csv", 1000)
    print("Data loaded.")
    app.run()
