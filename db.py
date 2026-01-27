from flask_mysqldb import MySQL

mysql = MySQL()

import os

def init_db(app):
    # Railway uses MYSQLHOST, MYSQLUSER, etc. while my app used MYSQL_HOST, MYSQL_USER
    # This logic handles both automatically
    host = os.environ.get('MYSQLHOST') or os.environ.get('MYSQL_HOST', 'localhost')
    user = os.environ.get('MYSQLUSER') or os.environ.get('MYSQL_USER', 'root')
    db_name = os.environ.get('MYSQLDATABASE') or os.environ.get('MYSQL_DB', 'cppt_db')
    
    print(f"Connecting to host: {host}, user: {user}, db: {db_name}")
    
    app.config['MYSQL_HOST'] = host
    app.config['MYSQL_USER'] = user
    app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQLPASSWORD') or os.environ.get('MYSQL_PASSWORD', '')
    app.config['MYSQL_DB'] = db_name
    app.config['MYSQL_PORT'] = int(os.environ.get('MYSQLPORT') or os.environ.get('MYSQL_PORT', 3306))
    
    mysql.init_app(app)
