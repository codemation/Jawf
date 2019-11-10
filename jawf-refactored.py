#!/usr/bin/python3
"""
    Just another web frame-work
"""
import os, sys
def first_line(f):
    for l in f:
        return l

def check_for_project(name=None):
    try:
        with open(".jawf", 'r') as jawf:
            print (f"Detected Existing project:{first_line(jawf)}")
            return True
    except:
        try:
            with open('.cmddir', 'r') as cmdir:
                print (f"Detected Existing project:{first_line(cmdir)}")
                return True
        except:
            print ("Not inside existing jawf project")
            return False
def get_proj_dir(command):
    try:
        proj_dir = ''
        with open('.cmddir','r') as c:
            return first_line(c)
    except:
        usage(f"{command} must be run within an existing project dir")
        return 
def add_db_table(db, tableName):
    """
        table to create within existing db, used within existing jawf proj dir
    """
    proj_dir = get_proj_dir('add_db_table')
    try:
        with open(f'{proj_dir}dbs/{db.lower()}/tables/{tableName}.py', 'r') as table:
            print (f"Table {tableName} in DB {db} already exists")
    except:
        # create schema file to declare columns 
        try:
            with open(f'{proj_dir}dbs/{db}/tables/{tableName}.py', 'w') as tbl:
                tbl.write(f"""
def db_attach(server):
    db = server.data['{db}']
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
    #    '{tableName}', [
    #        (), 
    #        (), 
    #        ()
    #)
    pass # Enter db.create_table statement here
            """)
        except FileNotFoundError:
            print(f'Error when creating file {proj_dir}dbs/{db}/tables/{tableName}.py')
            print(f'db {db} directory may have moved or does not exist, was DB ever created?')
            return
        with open(f'{proj_dir}dbs/{db}/setup.py', 'a') as setup:
            setup.write(f"""
    from dbs.{db}.tables import {tableName}
    {tableName}.db_attach(server)
            """)
        print(f"table {tableName} config created within db {db}")
def add_db(dbName, dbType='sqlite3'):
    """
        db to create within existing jawf project dir
        default: sqlite3 
        other supported: myql
    """
    proj_dir = get_proj_dir('add_db')

    try:
        with open(f'{proj_dir}dbs/{dbName}/__init__.py', 'r') as initpy:
            print (f"DB with name {dbName} already exists")
    except:
        # Update dbs/setup.py
        with open(f'{proj_dir}dbs/setup.py', 'a') as setup:
            setup.write(f"""
    from dbs.{dbName.lower()} import {dbName}_db
    {dbName}_db.run(server)
            """)
        # Make dir with db name ( __init__.py, app_name.py)
        os.makedirs(f'{proj_dir}dbs/{dbName.lower()}')
        #Make tables dir within db dir
        os.makedirs(f'{proj_dir}dbs/{dbName.lower()}/tables')
        with open(f'{proj_dir}dbs/{dbName}/tables/.cmddir', 'a') as c:
            c.write(proj_dir)
        with open(f'{proj_dir}dbs/{dbName}/tables/.jawf_db', 'a') as j:
            j.write(dbName)

        # make __init__.py & app.py
        with open(f'{proj_dir}dbs/{dbName.lower()}/__init__.py', 'w') as initpy:
            initpy.write(f'# created for db {dbName}')
        with open(f'{proj_dir}dbs/{dbName.lower()}/.cmddir', 'w') as c:
            c.write(proj_dir)
        connector = 'mysql.connector' if dbType == 'mysql' else 'sqlite3'
        with open(f'{proj_dir}dbs/{dbName.lower()}/{dbName}_db.py', 'w') as newdb:
            newdb.write(f"""# {dbName} - type {dbType}
def run(server):
    import sys, os
    config=dict()
            """)
            if dbType == 'mysql':
                newdb(f"""
    env = ['DB_USER','DB_PASSWORD','DB_HOST', 'DB_PORT']
    conf = ['user','password','database','host','port']
    try:
        config = {'{cnfVal: os.getenv(dbVal).rstrip() for dbVal,cnfVal in zip(env,conf)}'}
    except Exception as e:
        print('Missing an environment variable')
        config= {'{cnfVal: os.getenv(dbVal) for dbVal,cnfVal in zip(env,conf)}'}
        print(config)""")
            elif dbType=='sqlite3':
                newdb.write(f"""
    config['database'] = '{dbName}'""")
            else:
                print(f"un-support type {dbType} provided with --type . Use: mysql or sqlite3")
                return
            newdb.write(f"""
    #USE ENV PATH for PYQL library or /pyql/
    sys.path.append('/pyql/' if os.getenv('PYQL_PATH') == None else os.getenv('PYQL_PATH'))

    import data, {dbType}
    from . import setup
    server.data['{dbName}'] = data.database({connector}.connect, **config)
    setup.attach_tables(server)
            """)
        with open(f'{proj_dir}dbs/{dbName}/setup.py', 'w') as db_setup:
            db_setup.write(f""" # {dbName}
def attach_tables(server):
    #Tables are added  here
    pass
            """)
        #
        print(f"db {dbName} created successfully ")
        
def add_app(appName, route=None):
    """
        app name to init within jawf project dir
    """
    proj_dir = get_proj_dir('add_app')
    try:
        with open(f'{proj_dir}apps/{appName}/__init__.py', 'r') as initpy:
            print(f"App with name {appName} already exists")
    except:
        # Update apps/setup.py 
        with open(f'{proj_dir}apps/setup.py', 'a') as setup:
            setup.write(f"""
    from apps.{appName.lower()} import {appName}
    {appName}.run(server)            
            """)
        # Make dir with app name ( __init__.py, app_name.py)
        os.makedirs(f'{proj_dir}apps/{appName.lower()}')
        # make __init__.py & app.py
        with open(f'{proj_dir}apps/{appName.lower()}/__init__.py', 'w') as initpy:
            initpy.write(f'# created for app {appName}')
        with open(f'{proj_dir}apps/{appName.lower()}/.cmddir', 'w') as initpy:
            initpy.write(proj_dir)
        with open(f'{proj_dir}apps/{appName.lower()}/{appName}.py', 'w') as newapp:
            newapp.write(f"""# {appName}
def run(server):
    @server.route('/{appName.lower() if route == None else route}')
    def {appName}_func():
        #Add Code here
        print("Hello {appName} World") 
        return "<h1>Hello {appName} World</h1>", 200
            """)
        print(f"app {appName} was created successfully within {proj_dir}")

def init(projName):
    """
        project name for init jawf project
    """
    ## checking for existing .jawf project in cd
    if check_for_project(projName):
        return
    else:
        os.makedirs(f'{projName}/apps')
        os.makedirs(f'{projName}/dbs')
        real_path = ''
        with open(f'{projName}/.jawf', 'w') as jawf:
            jawf.write(projName)
            real_path = str(os.path.realpath(jawf.name)).split('.jawf')[0]
        with open(f'{projName}/.cmddir', 'w') as c:
            c.write(real_path)
        with open(f'{projName}/server.py', 'w') as server:
            server.write(f"""
from flask import Flask
app = Flask(__name__)
import setup
setup.run(app)
app.run('0.0.0.0','8080', debug=True)
            """)
        with open(f'{projName}/setup.py', 'w') as setup:
            setup.write(f"""# {projName}
def run(server):
    try:
        import os
        cmddirPath = None
        realPath = None
        with open('./.cmddir', 'r') as cmddir:
            for line in cmddir:
                cmddirPath = line
            realPath = str(os.path.realpath(cmddir.name)).split('.cmddir')[0]
        if not realPath == cmddirPath:
            print(f"NOTE: Project directory may have moved, updating project cmddir files from {'{cmddirPath}'} -> {'{realPath}'}")
            import os
            os.system("find . -name .cmddir > .proj_cmddirs")
            with open('.proj_cmddirs', 'r') as projCmdDirs:
                for f in projCmdDirs:
                    with open(f.rstrip(), 'w') as projCmd:
                        projCmd.write(realPath)
    except Exception as e:
        print("encountered exception when checking projPath")
        print(repr(e))
    try:
        from apps import setup
        setup.run(server)
        from dbs import setup as dbsetup # TOO DOO -Change func name later
        dbsetup.run(server) # TOO DOO - Change func name later
    except Exception as e:
        print("Project may not have any apps configured or apps setup.py cannot be found")
        print(repr(e))
            """)
        for dir in ['apps', 'dbs']:
            with open(f'{projName}/{dir}/__init__.py', 'w') as jawf:
                jawf.write(f"#initialized for project: {projName}")
            with open(f'{projName}/{dir}/.cmddir', 'w') as jawf:
                jawf.write(real_path)
        with open(f'{projName}/apps/setup.py', 'w') as setup:
            setup.write("""
def run(server):
    pass # apps start here

            """)
        print (f"Succesfully created jawf project: {projName}")
        with open(f'{projName}/dbs/setup.py', 'w') as setup:
            setup.write("""
def run(server):
    server.data = dict()
            """)
def parse_args(args):
    dArgs = {}
    for ind, arg in enumerate(args):
        if '--' in arg:
            if len(args) > ind+1:
                dArgs[arg] = args[ind+1]
            else:
                usage(f"missing argument for {arg} or syntax is invalid ", **{'_'.join(arg[2:].split('-')): True})
    return dArgs
def init_help():
    return """# Initialize Project directory
jawf --init <projName> 
jawf --init Project1"""
def add_app_help():
    return """# Add application
jawf --add-app <app-name> [--route <urlpattern> default: /app-name]
jawf --add-app myfirstapp
jawf --add-app homepage --route /"""
def add_db_help():
    return """# Add database
Supported database types: sqlite3, mysql
jawf --add-db <db-name> [--type mysql default: sqlite3]
jawf --add-db finance --type mysql
jawf --add-db stocks """
def add_db_table_help():
    return """# Add database table
jawf --add-db-table <db-name> --table <table-name>
jawf --add-db-table finance --table purchaseOrders"""

def usage(message=None, **kw):
    print(f"""{message if not message == None else ''}
JAWF Usage: --help""")
    for k in kw:
        try:
            print(getattr(sys.modules[__name__],f'{k}_help')())
        except:
            pass

if __name__ == "__main__":
    import sys
    if '--help' in sys.argv:
        usage(init=True, add_app=True, add_db=True, add_db_table=True)
    else:
        args = parse_args(sys.argv)
        if '--init' in args:
            init(args['--init'])
        else:
            argOptions=['--add-app', '--add-db', '--add-db-table']
            noOpton = True
            for option in argOptions:
                if option in args:
                    noOpton = False
                    # Check if jawf command was run from a jawf project directory
                    if check_for_project():
                        if '--add-app' in args:
                            add_app(args['--add-app'], args['--route'] if '--route' in args else None)
                        if '--add-db' in args:
                            add_db(args['--add-db'], args['--type'] if '--type' in args else 'sqlite3')
                        
                        if '--add-db-table' in args:
                            if '--table' in args: 
                                add_db_table(args['--add-db-table'], args['--table'])
                            else:
                                usage("missing table name or argument", add_db_table=True)
                    else:
                        print(f"""{' '.join(list(args.keys()))}
must be used within an existing project directory
or combined with --project <project-path> 
                        """)
                    break
            if noOpton:
                print("invalid or no argument")
    