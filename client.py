from flask import Flask, render_template
from flask_cors import CORS
from sys import argv
from block_data import Data

app = Flask(__name__)
CORS(app)

try:
    ip = argv[1]
except:
    ip = 'localhost'
try:
    port = argv[2]
except:
    port = 5001

@app.route("/")
def index():
    return render_template("client.html", ipaddress=ip, port=port, data=Data().required())

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5010)