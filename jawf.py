"""
    Just another web frame-work
"""

def check_for_project(name=None):
    try:
        print ("checking for .jawf in ")
        with open(".jawf", 'r') as jawf:
            for line in jawf:
                print ("Detected Existing project: %s" %(line))
            return True
    except:
        try:
            with open('.cmddir', 'r') as c:
                for line in c:
                    print ("Detected Existing project: %s" %(line))
                return True
        except:
            print ("Not inside existing jawf project")
            return False
def get_proj_dir(command):
    try:
        proj_dir = ''
        with open('.cmddir','r') as c:
            for l in c:
                proj_dir = l
        return proj_dir
    except:
        print("{cmd} must be run within an existing project dir".format(cmd=command))
        return
def add_db_table(db, table_name):
    """
        table to create within existing db, used within existing jawf proj dir
    """
    proj_dir = get_proj_dir('add_db_table')
    try:
        with open(proj_dir + 'dbs/'+db.lower()+'/tables/%s.py'%(table_name.lower()), 'r') as table:
            print ("Table %s in DB  %s already exists"%(table_name,db))
    except:
        # create schema file to declare columns 
        with open(proj_dir+'dbs/%s/tables/%s.py'%(db,table_name), 'w') as tbl:
            tbl.write("""
def db_attach(server):
    db = server.data['{name}']
    col = server.data_col
    # Example 
    # db.create_table(
    #    'users', # 
    #     [
    #        col('userid', int, 'AUTOINCREMENT'),
    #        col('username', str, 'UNIQUE NOT NULL'),
    #        col('email', str, 'NOT NULL'),
    #        col('join_date', str, None),
    #        col('last_login', str, None),
    #     ],
    # 'userid' # Primary Key
    # )
    #UNCOMMENT Below to create
    #
    #db.create_table(
    #   '{table}', col(), col(), col()
    #)
    pass # Enter db.create_table statement here
            """.format(
                name=db,
                table=table_name
            ))
        with open(proj_dir + 'dbs/%s/setup.py'%(db), 'a') as stp:
            toWrite = [
                "    from dbs.{name}.tables import {tbl}\n".format(name=db, tbl=table_name),
                "    {tbl}.db_attach(server)\n".format(tbl=table_name)
            ]
            for l in toWrite:
                stp.write(l)
        
def add_db(name, db_type='sqlite'):
    """
        db to create within existing jawf project dir
    """
    proj_dir = get_proj_dir('add_db')

    try:
        with open(proj_dir + 'dbs/'+name+'/__init__.py', 'r') as initpy:
            print ("DB with name %s already exists"%(name))
    except:
        # Update dbs/setup.py
        with open(proj_dir+'dbs/setup.py', 'a') as setup:
            setup.write('    from dbs.%s import %s_db\n'%(name.lower(), name) +
                        '    %s_db.run(server)\n'%(name))
        # Make dir with db name ( __init__.py, app_name.py)
        import os
        os.makedirs(proj_dir +'dbs/'+name.lower())

        #Make tables dir within db dir
        os.makedirs(proj_dir +'dbs/'+name.lower()+'/tables')
        with open(proj_dir+'dbs/%s/tables/.cmddir'%(name), 'a') as c:
            c.write(proj_dir)
        with open(proj_dir+'dbs/%s/tables/.jawf_db'%(name), 'a') as j:
            j.write(name)

        # make __init__.py & app.py
        with open(proj_dir + 'dbs/'+name.lower()+'/__init__.py', 'w') as initpy:
            initpy.write('# created for db %s'%(name))
        with open(proj_dir + 'dbs/'+name.lower()+'/.cmddir', 'w') as c:
            c.write(proj_dir)
        connector = 'mysql.connector' if db_type == 'mysql' else 'sqlite'
        with open(proj_dir + 'dbs/%s/'%(name.lower())+'%s_db.py'%(name), 'w') as newdb:
            toWrite=[
            "def run(server):\n",
            "    import sys, os\n",
            "    config={}\n"
            "    config['user'] = os.getenv('DB_USER')\n",
            "    config['password'] = os.getenv('DB_PASSWORD')\n",
            "    config['database'] = os.getenv('DB_NAME')\n",
            "    config['host'] = os.getenv('DB_HOST')\n",
            "    sys.path.append('/pyql/')\n",
            '    import data, {db_type}\n'.format(db_type=db_type),
            '    from . import setup\n',
            "    server.data['{name}'] = data.database({connector}.connect, **config)\n".format(
                    name=name,
                    connector=connector
                ),
            '    server.data_col = data.col\n',
            '    setup.attach_tables(server)\n'
            ]
            for l in toWrite:
                newdb.write(l)
        with open(proj_dir + 'dbs/%s/setup.py'%(name.lower()), 'w') as db_stp:
            db_stp.write("def attach_tables(server):\n")
        
def add_app(name, route=None):
    """
        app name to init within jawf project dir
    """
    proj_dir = get_proj_dir('add_app')
    try:
        with open(proj_dir + 'apps/'+name+'/__init__.py', 'r') as initpy:
            print ("App with name %s already exists"%(name))
    except:
        # Update apps/setup.py 
        with open(proj_dir + 'apps/setup.py', 'a') as setup:
            setup.write('    from apps.%s import %s\n'%(name.lower(), name) +
                        '    %s.run(server)\n'%(name))
            """
            Inserting app factory into setup.py
            from apps.helloworld import HelloWorld
            HelloWorld.run(server)
            """
        # Make dir with app name ( __init__.py, app_name.py)
        import os
        os.makedirs(proj_dir + 'apps/'+name.lower())
        # make __init__.py & app.py
        with open(proj_dir + 'apps/'+name.lower()+'/__init__.py', 'w') as initpy:
            initpy.write('# created for app %s'%(name))
        with open(proj_dir + 'apps/'+name.lower()+'/.cmddir', 'w') as initpy:
            initpy.write(proj_dir)
        with open(proj_dir + 'apps/%s/'%(name.lower())+'%s.py'%(name), 'w') as newapp:
            newapp.write('def run(server):\n' +
                         '    @server.route(%s)\n'%(str('"/%s"'%(name)) if route == None else route) +
                         '    def %s_func():\n'%(name) +
                         '        # insert code \n'
                         )

def init(name):
    """
        project name for init jawf project
    """
    ## checking for existing .jawf project in cd
    if check_for_project(name):
        return
    else:
        import os
        os.makedirs(name+'/apps')
        os.makedirs(name+'/dbs')
        real_path = ''
        with open(name + "/.jawf", 'w') as jawf:
            jawf.write(name)
            real_path = str(os.path.realpath(jawf.name)).split('.jawf')[0]
        with open(name + "/.cmddir", 'w') as c:
            c.write(real_path)
        with open(name + "/server.py", 'w') as srv:
            serverpy = ['from flask import Flask\n', 
                'app = Flask(__name__)\n',
                'import setup\n',
                'setup.run(app)\n',
                "app.run('0.0.0.0','8080', debug=True)\n"]
            for l in serverpy:
                srv.write(l)
        with open(name + '/setup.py', 'w') as stp:
            setuppy = ['def run(server):\n',
                    '    try:\n'
                    '        from apps import setup\n'
                    '        setup.run(server)\n',
                    '        from dbs import setup as dbsetup\n'
                    '        dbsetup.run(server)\n',
                    '    except Exception as e:\n',
                    '        print("Project may not have any apps configured or apps setup.py cannot be found")\n'
                    '        print(repr(e))\n']
            for l in setuppy:
                stp.write(l)

        for dir in ['apps', 'dbs']:
            with open(name+'/%s/__init__.py'%(dir), 'w') as jawf:
                jawf.write("#initialized for project: %s" %(name))
            with open(name+'/%s/.cmddir'%(dir), 'w') as jawf:
                jawf.write(real_path)
        with open(name + '/apps/setup.py', 'w') as stp:
            stp.write(
                'def run(server):\n'+
                '    pass # apps start here\n'
                    )
        print ("Succesfully created jawf project: %s" %(name))
        with open(name + '/dbs/setup.py', 'w') as stp:
            toWrite =[
                "def run(server):\n" +
                "    server.data = dict()\n"
            ]
            for l in toWrite:
                stp.write(l)
       
if __name__ == "__main__":
    import sys
    if len (sys.argv) < 3:
        print ("jawf takes at least 2 argument: \n Example: \n  jawf.py init Project1")
    else:
        print (sys.argv)
        arg1,arg2 = sys.argv[1], sys.argv[2] 
        if arg1 == 'init':
            init(arg2)
        if arg1 == 'app':
            if len(sys.argv) > 3:
                arg3 = sys.argv[3]
                if arg2 == 'add':
                    if check_for_project():
                        print ("adding app %s"%(arg3))
                        add_app(arg3)
                    else:
                        print ("Error: \n" +
                            "   add app must be used within an existing project directory or \n" +
                            "   combined with <--project | -p <project path>")
                    
            else:
                print ("Usage: \n" +
                    "   jawf.py app add <name> \n" +
                    "   Example: \n" +
                    "   jawf.py app add HelloWorld")
        if arg1 == 'db':
            if len(sys.argv) > 3:
                arg3 = sys.argv[3]
                if arg2 == 'add':
                    if check_for_project():
                        print("adding db {name}".format(name=arg3))
                        db_type ='sqlite' if len(sys.argv) < 5 else sys.argv[4]
                        add_db(arg3, db_type)
                    else:
                        print ("Error: \n" +
                            "   add db must be used within an existing project directory or \n" +
                            "   combined with <--project | -p <project path>")
                if arg2 == 'table':
                    if arg3 == 'add':
                        def error():
                            print("Error: \n" + 
                                "   add db table must include db name & new_table_name &&\n" +
                                "   must be used within existing jawf project dir\n\n" +
                                "   Example:\n" +
                                "       jawf add db table db_1 users\n"
                                )
                        if check_for_project():
                            if len(sys.argv) > 5:
                                db_name, table_name  = sys.argv[4],sys.argv[5]
                                add_db_table(db_name, table_name)
                            else:
                                error()
                        else:
                            error()

                    #TOODOO - table remove / table import / table modify?