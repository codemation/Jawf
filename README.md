# Jawf
Just Another Web Framework - streamlining flask application development

## Basic Usage

### Initialize a JAWF Project directory
    
    $ jawf --init <projName> 

    $ jawf --init Project1

    Not inside existing jawf project
    Succesfully created jawf project: Project1

### Add an app to project

    Usage: jawf --add-app <app-name> [--route <urlpattern> default: /app-name]
    $ jawf --add-app myfirstapp
    $ jawf --add-app homepage --route /

    $ jawf --add-app myfirstapp
    Not inside existing jawf project
    --add-app
    must be used within an existing project directory
    or combined with --project <project-path> 

    $ cd Project1/
    /Project1 $ jawf --add-app myfirstapp
    Detected Existing project:Project1
    app myfirstapp was created successfully within /home/josh/python/mysql/Project1/

This creates an application which is immedietly wired up to the project. Can be tested right away. 

    /Project1$ python3 server.py 
    * Serving Flask app "server" (lazy loading)
    * Environment: production
    WARNING: This is a development server. Do not use it in a production deployment.
    Use a production WSGI server instead.
    * Debug mode: on
    * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
    * Restarting with stat
    * Debugger is active!
    * Debugger PIN: 144-714-176

    $ curl http://0.0.0.0:8080/myfirstapp
    <h1>Hello myfirstapp World</h1>

A closer look at the skeleton of the application created.

    Project1/apps/myfirstapp/myfirstapp.py

    # myfirstapp
    def run(server):
        # Add import libraries here, run only once, when server is started
        @server.route('/myfirstapp')
        def myfirstapp_func():
            # Add repeatable logic here, run as often as endpoint is called.
            print("Hello myfirstapp World") 
            return "<h1>Hello myfirstapp World</h1>", 200

If you are familiar with flask routing, this is exactly the same. The work of wiring together multiple endpoints to a primary server app is done for you.    
### Add an DB to project

JAWF makes it easy to add new databaes, tables to a project as well as accessing the data in combination with [pyql]<https://github.com/codemation/pyql>

#### Supported database types: sqlite3, mysql

    jawf --add-db <db-name> [--type mysql default: sqlite3]
    jawf --add-db finance --type mysql
    jawf --add-db stocks 

sqlite3 is a builtin library with python3 and creates light-weight databases in place for storing / retreiving data. 

#### sqlite3

    Project1$ jawf --add-db stocks
    Detected Existing project:Project1
    db stocks created successfully

This does not immedietly create a database until a table is added, and server is started.

##### Lets have a look at the DB file created at Project1/dbs/stocks/

    stocks_db.py

    # stocks - type sqlite3
    def run(server):
        import sys, os
        @server.route('/stocks_attach')
        def stocks_attach():
            config=dict()
                
            with open('.cmddir', 'r') as projDir:
                for projectPath in projDir:
                    config['database'] = f'{projectPath}dbs/stocks/stocks'
            #USE ENV PATH for PYQL library or /pyql/
            sys.path.append('/pyql/' if os.getenv('PYQL_PATH') == None else os.getenv('PYQL_PATH'))
            try:
                import data, sqlite3
                from . import setup
                server.data['stocks'] = data.database(sqlite3.connect, **config)
                setup.attach_tables(server)
                return {"status": 200, "message": "stocks attached successfully"}, 200
            except Exception as e:
                return {"status": 200, "message": repr(e)}, 500
        stocks_attach()

##### Whats happening here:
Similar to app's there is an endpoint created to allow app developers control on when the web-server will attempt to access the DB
This becomes more useful with remote-db's or in micro-service deployments, when a DB server may not be ready as soon as the APP server. 

    # stocks - type sqlite3
    def run(server):
        import sys, os
        @server.route('/stocks_attach')
        def stocks_attach():
            config=dict()

Here we are first checking the project relative directory, as this is important wth sqlite3 databases which are always locally existing within the server.
By default, mysqlite Db will exist within dbs/db-name/db

            with open('.cmddir', 'r') as projDir:
                for projectPath in projDir:
                    config['database'] = f'{projectPath}dbs/stocks/stocks'

PYQL is a dependency. If not directly install int a venv, this can be accessed using a ENV Variable PYQL_PATH or default /pyql/ system path.

            #USE ENV PATH for PYQL library or /pyql/
            sys.path.append('/pyql/' if os.getenv('PYQL_PATH') == None else os.getenv('PYQL_PATH'))

Finally PYQL libraryies are imported, and DB connector is attached to the server object (available in all JAWF apps), then tables are attached, and configured if not existing.

            try:
                import data, sqlite3
                from . import setup
                server.data['stocks'] = data.database(sqlite3.connect, **config)
                setup.attach_tables(server)
                return {"status": 200, "message": "stocks attached successfully"}, 200
            except Exception as e:
                return {"status": 200, "message": repr(e)}, 500


#### mysql

    Project1$$ jawf --add-db trades --type mysql
    Detected Existing project:Project1
    db trades created successfully 

Databases must be created already within the mysql instance, as well as appropiate user / permissions for accessing the DB, creating tables.

    trades.py

    # trades - type mysql
    def run(server):
        import sys, os
        @server.route('/trades_attach')
        def trades_attach():
            config=dict()
                
            env = ['DB_USER','DB_PASSWORD','DB_HOST', 'DB_PORT']
            conf = ['user','password','database','host','port']
            try:
                config = {cnfVal: os.getenv(dbVal).rstrip() for dbVal,cnfVal in zip(env,conf)}
            except Exception as e:
                print('Missing an environment variable')
                config= {cnfVal: os.getenv(dbVal) for dbVal,cnfVal in zip(env,conf)}
                print(config)
                return {
                    "status": 500, 
                    "message": "Missing environment variable(s)",
                    "env-vars": config
                }, 500 
            #USE ENV PATH for PYQL library or /pyql/
            sys.path.append('/pyql/' if os.getenv('PYQL_PATH') == None else os.getenv('PYQL_PATH'))
            try:
                import data, mysql
                from . import setup
                server.data['trades'] = data.database(mysql.connector.connect, **config)
                setup.attach_tables(server)
                return {"status": 200, "message": "trades attached successfully"}, 200
            except Exception as e:
                return {"status": 200, "message": repr(e)}, 500
        trades_attach()

Much of the same logic is shared with SQLITE3 databases, but the most important different is the DB connector requirements. As this is not always a DB locally existing(it could be), we need to know a few more details on how to access the database.

Here we are looking for 4 different ENV vars. These can be set in a number of different ways or passed into the /DB_NAME_attach endpoint via a POST request, passing in a JSON key-value pair for 'user','password','database','host','port'

            env = ['DB_USER','DB_PASSWORD','DB_HOST', 'DB_PORT', DB_NAME]
            conf = ['user','password','host','port', database]
            try:
                config = {cnfVal: os.getenv(dbVal).rstrip() for dbVal,cnfVal in zip(env,conf)}
            except Exception as e:
                print('Missing an environment variable')
                config= {cnfVal: os.getenv(dbVal) for dbVal,cnfVal in zip(env,conf)}
                print(config)
                return {
                    "status": 500, 
                    "message": "Missing environment variable(s)",
                    "env-vars": config
                }, 500 

#### Add a Table to a DB
Databases are comprised of tables, so we need to configure the schema for each of the tables we want the JAWF project to create. PYQL will automatically discover tables which already exist and be made accessible via the server.data['databaseName'].tables['tableName']

    jawf --add-db-table <db-name> --table <table-name>
    jawf --add-db-table finance --table purchaseOrders

    $ jawf --add-db-table trades --table daytrades
    Detected Existing project:Project1
    table daytrades config created within db trades

This creates a daytrades table within the tables dir of the trades database. 

    def db_attach(server):
        db = server.data['trades']
        # Example 
        # db.create_table(
        #    'users', # table-name
        #     [
        #        ('userid', int, 'AUTOINCREMENT'),
        #        ('username', str, 'UNIQUE NOT NULL'),
        #        ('email', str, 'NOT NULL'),
        #        ('join_date', str),
        #        ('last_login', str),
        #     ],
        # 'userid' # Primary Key
        # )
        #UNCOMMENT Below to create
        #
        #db.create_table(
        #    'daytrades', [
        #        (), 
        #        (), 
        #        ()
        #)
        pass # Enter db.create_table statement here

See PYQL docs for more information Table SCHEMA usage, but the above template gets you started. 