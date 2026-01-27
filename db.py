from flask_mysqldb import MySQL

mysql = MySQL()

import os

def init_db(app):
    # 1. Try MYSQL_URL first (most reliable in Railway)
    mysql_url = os.environ.get('MYSQL_URL')
    host = user = password = db_name = port = None

    if mysql_url and mysql_url.startswith('mysql://'):
        try:
            # Format: mysql://user:password@host:port/database
            print("Found MYSQL_URL, parsing...")
            url = mysql_url.replace('mysql://', '')
            auth, rest = url.split('@')
            user, password = auth.split(':')
            host_port, db_name = rest.split('/')
            if ':' in host_port:
                host, port = host_port.split(':')
            else:
                host = host_port
                port = 3306
        except Exception as e:
            print(f"Error parsing MYSQL_URL: {e}")

    # 2. Fallback to individual variables
    host = host or os.environ.get('MYSQLHOST') or os.environ.get('MYSQL_HOST')
    user = user or os.environ.get('MYSQLUSER') or os.environ.get('MYSQL_USER')
    password = password or os.environ.get('MYSQLPASSWORD') or os.environ.get('MYSQL_PASSWORD')
    db_name = db_name or os.environ.get('MYSQLDATABASE') or os.environ.get('MYSQL_DB')
    port = port or os.environ.get('MYSQLPORT') or os.environ.get('MYSQL_PORT') or 3306

    # 3. Last fallback to local defaults
    if not host or not user:
        print("⚠️ WARNING: No MySQL environment variables found. Using local defaults.")
        host = host or 'localhost'
        user = user or 'root'
        db_name = db_name or 'cppt_db'
        password = password or ''

    print(f"Final Config -> Host: {host}, User: {user}, DB: {db_name}, Port: {port}, Pwd Set: {'YES' if password else 'NO'}")
    
    app.config['MYSQL_HOST'] = host
    app.config['MYSQL_USER'] = user
    app.config['MYSQL_PASSWORD'] = password
    app.config['MYSQL_DB'] = db_name
    app.config['MYSQL_PORT'] = int(port)
    
    mysql.init_app(app)
