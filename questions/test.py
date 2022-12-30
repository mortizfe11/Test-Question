from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)

from test_routes import *

app.config["MYSQL_DATABASE_HOST"] = 'localhost'
app.config["MYSQL_DATABASE_USER"] = 'root'
app.config["MYSQL_DATABASE_PASSWORD"] = 'MySQL123/'
app.config["MYSQL_DATABASE_DB"] = 'test_db'

mysql = MySQL()
mysql.init_app(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5015, debug = True)