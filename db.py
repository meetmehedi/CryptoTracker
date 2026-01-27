from flask_mysqldb import MySQL

mysql = MySQL()

import os

def init_db(app):
    # Railway uses MYSQLHOST, MYSQLUSER, etc. while my app used MYSQL_HOST, MYSQL_USER
    # This logic handles both automatically
    app.config['MYSQL_HOST'] = os.environ.get('MYSQLHOST') or os.environ.get('MYSQL_HOST', 'localhost')
    app.config['MYSQL_USER'] = os.environ.get('MYSQLUSER') or os.environ.get('MYSQL_USER', 'root')
    app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQLPASSWORD') or os.environ.get('MYSQL_PASSWORD', '')
    app.config['MYSQL_DB'] = os.environ.get('MYSQLDATABASE') or os.environ.get('MYSQL_DB', 'cppt_db')
    app.config['MYSQL_PORT'] = int(os.environ.get('MYSQLPORT') or os.environ.get('MYSQL_PORT', 3306))
    
    mysql.init_app(app)
