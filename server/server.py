from flask import Flask
from flask_cors import CORS

from flask import request
import pandas as pd
from data_handler import DataHandler

from heatmap import Heatmap 
from stacked_barchart import StackedBarchart
from parallel_sets import ParallelSets

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

@app.route("/debug")
def debug():
    stacked_barchart = StackedBarchart()
    xAttribute = "date_time"
    yAttribute = "syslog_priority"
    return stacked_barchart.get_stacked_barchart_data_2(data_handler.get_dataframe("2000-01-01 00:00:00", "2020-01-01 00:00:00"), yAttribute)

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

@app.route("/getParallelSets")
def get_parallel_sets():
    start_datetime_str = request.args.get('start_datetime')
    end_datetime_str = request.args.get('end_datetime')
    print(request.args)
    assert start_datetime_str is not None
    assert end_datetime_str is not None

    subnet_bits = int(request.args.get('subnet_bits'))

    parallel_sets = ParallelSets()
    return parallel_sets.get_parallel_sets_data(data_handler.get_dataframe(start_datetime_str, end_datetime_str), subnet_bits)

if __name__ == "__main__":
    print("Loading data...")
    data_handler.load_csv("../data/MC2-CSVFirewallandIDSlogs/FIREWALL.csv", 100000)

    print("Data loaded.")
    app.run()
