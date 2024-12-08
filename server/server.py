from flask import Flask
from flask_cors import CORS

from heatmap import Heatmap 

app = Flask(__name__)
app.debug = True

# allows cross origin to be called from localhost:3000
# not recommended in production
CORS(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/getHeatmap")
def get_heatmap():
    return Heatmap.get_heatmap_data()

if __name__ == "__main__":
    app.run()
