# Jawf
Just Another Web Framework - streamlining flask application development

## Basic Usage

### Create JAWF project

    $ cd <project-folder>
    $ jawf.py init Project1

### Add an app to project

    $ jawf app add newapp
    checking for .jawf in 
    Not inside existing jawf project
    Error: 
    add app must be used within an existing project directory or 
    combined with <--project | -p <project path>

    /Project1 $ cd  <project-folder>/Project1 
    /Project1 $ jawf app add newapp
    checking for .jawf in 
    Detected Existing project: Project1
    adding app newapp

    $ cd apps/newapp/
    /Project1/apps/newapp$ ls
    __init__.py  newapp.py

    #Default NewAPP Shell - route can be modified 
    def run(server):
    @server.route("/newapp")
    def newapp_func():
        # insert code 
        return "<h1> Hello new application development world! </h1>"
    
    /Project1/apps/newapp$ cd ..; cd ..
    
    /Project1$ ls
    apps  dbs  server.py  setup.py

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


### Add an DB to project

    /Project1$ jawf db add newdatabase
    checking for .jawf in 
    Detected Existing project: Project1
    adding db newdatabase

    Project1$ cd dbs/newdatabase/

    /Project1/dbs/newdatabase$ ls
    __init__.py  newdatabase_db.py  setup.py  tables

    #newdatabase_db.py
    def run(server):
        import sys, os
        config={}
        env = ['DB_USER','DB_PASSWORD','DB_HOST', 'DB_PORT']
        conf = ['user','password','database','host','port']
        try:
            config = {cnfVal: os.getenv(dbVal).rstrip() for dbVal,cnfVal in zip(env,conf)}
        except Exception as e:
            print('Missing an environment variable')
            print({cnfVal: os.getenv(dbVal).rstrip() for dbVal,cnfVal in zip(env,conf)})
        #PATH for PYQL library
        sys.path.append('/pyql/')
        import data, sqlite
        from . import setup
        server.data['newdatabase'] = data.database(sqlite.connect, **config)
        setup.attach_tables(server)

Defaults to sqlite, mysql can be selected using the following:

    $ jawf db add newmysql-database mysql
    ['/home/josh/python/Jawf/jawf.py', 'db', 'add', 'newmysql-database', 'mysql']
    checking for .jawf in 
    Detected Existing project: Project1/
    adding db newmysql-database

As long as you are within Project1/ app add or db add can be run. 

    /newmysql-database$ ls
    __init__.py  newmysql-database_db.py  setup.py  tables


#### Add a Table to a DB
TOODOO
