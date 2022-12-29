from flask import Flask

app = Flask(__name__)

from test_routes import *

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5015, debug = True)