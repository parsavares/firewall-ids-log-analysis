from flask import Flask
from flask_cors import CORS

from flask import request
import pandas as pd
from data_handler import DataHandler

from heatmap import Heatmap 
from stacked_barchart import StackedBarchart
from parallel_sets import ParallelSets
from sanke_diagram import SankeDiagram

app = Flask(__name__)
app.debug = True

data_handler = DataHandler()
data_handler_ids = DataHandler()

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
    data_source = params.get('data_source')

    assert xAttribute is not None
    assert yAttribute is not None
    assert start_datetime_str is not None
    assert end_datetime_str is not None
    assert data_source is not None

    # Used when dealing with IPS, so optional    
    subnet_bits = int(params.get('subnet_bits'))

    heatmap = Heatmap()
    df = data_handler.get_dataframe(start_datetime_str, end_datetime_str) if data_source == "FIREWALL" else data_handler_ids.get_dataframe(start_datetime_str, end_datetime_str)
    return heatmap.get_heatmap_data(df, xAttribute, yAttribute, subnet_bits)

@app.route("/debug")
def debug():

    sanke_diagram = SankeDiagram()
    return sanke_diagram.get_sanke_diagram_data(data_handler.get_dataframe(), 24)

@app.route("/debug_ids")
def debug_ids():
    stacked_barchart = StackedBarchart()
    xAttribute = "date_time"
    yAttribute = "priority"
    return stacked_barchart.get_stacked_barchart_data_2(data_handler_ids.get_dataframe("2000-01-01 00:00:00", "2020-01-01 00:00:00"), yAttribute)


@app.route("/getStackedBarchart")
def get_stacked_barchart():
    params = request.args
    yAttribute = params.get('yAttribute')
    start_datetime_str = params.get('start_datetime')
    end_datetime_str = params.get('end_datetime')
    data_source = params.get('data_source')

    assert yAttribute is not None
    assert start_datetime_str is not None
    assert end_datetime_str is not None
    assert data_source is not None

    print("start: ", start_datetime_str)
    stacked_barchart = StackedBarchart()
    df = data_handler.get_dataframe(start_datetime_str, end_datetime_str) if data_source == "FIREWALL" else data_handler_ids.get_dataframe(start_datetime_str, end_datetime_str)
    return stacked_barchart.get_stacked_barchart_data(df, yAttribute)

@app.route("/getParallelSets")
def get_parallel_sets():
    start_datetime_str = request.args.get('start_datetime')
    end_datetime_str = request.args.get('end_datetime')
    data_source = request.args.get('data_source')

    subnet_bits = int(request.args.get('subnet_bits'))

    assert start_datetime_str is not None
    assert end_datetime_str is not None
    assert data_source is not None
    assert subnet_bits is not None

    parallel_sets = ParallelSets()
    df = data_handler.get_dataframe(start_datetime_str, end_datetime_str) if data_source == "FIREWALL" else data_handler_ids.get_dataframe(start_datetime_str, end_datetime_str)
    return parallel_sets.get_parallel_sets_data(df, subnet_bits)

@app.route("/getSankeDiagram")
def get_sanke_diagram():
    start_datetime_str = request.args.get('start_datetime')
    end_datetime_str = request.args.get('end_datetime')
    data_source = request.args.get('data_source')

    subnet_bits = int(request.args.get('subnet_bits'))

    assert start_datetime_str is not None
    assert end_datetime_str is not None
    assert data_source is not None
    assert subnet_bits is not None

    sanke_diagram = SankeDiagram()
    return sanke_diagram.get_sanke_diagram_data(data_handler.get_dataframe(start_datetime_str, end_datetime_str), subnet_bits)

if __name__ == "__main__":
    print("Loading data...")
    data_handler.load_csv("../data/MC2-CSVFirewallandIDSlogs/FIREWALL.csv")
    data_handler_ids.load_csv("../data/MC2-CSVFirewallandIDSlogs/IDS.csv")

    print("Data loaded.")
    app.run()
