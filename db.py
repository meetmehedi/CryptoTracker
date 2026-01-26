from flask_mysqldb import MySQL

mysql = MySQL()

import os

def init_db(app):
    app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
    app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
    app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', '')
    app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'cppt_db')
    # app.config['MYSQL_UNIX_SOCKET'] = '/tmp/mysql.sock' # macOS socket, uncomment if needed
    mysql.init_app(app)
