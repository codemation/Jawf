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
        print ("Not inside existing jawf project")
        return False
def add_app(name, route=None):
    """
        app name to init within jawf project dir
    """
    try:
        with open('apps/'+name+'/__init__.py', 'r') as initpy:
            print ("App with name %s already exists"%(name))
    except:
        # Update apps/setup.py 
        with open('apps/setup.py', 'a') as setup:
            setup.write('   from apps.%s import %s\n'%(name.lower(), name) +
                        '   %s.run(server)\n'%(name))
            """
            Inserting app factory into setup.py
            from apps.helloworld import HelloWorld
            HelloWorld.run(server)
            """
        # Make dir with app name ( __init__.py, app_name.py)
        import os
        os.makedirs('apps/'+name.lower())
        # make __init__.py & app.py
        with open('apps/'+name.lower()+'/__init__.py', 'w') as initpy:
            initpy.write('# created for app %s'%(name))
        with open('apps/%s/'%(name.lower())+'%s.py'%(name), 'w') as newapp:
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
        os.makedirs(name+'/pages')
        with open(name + "/.jawf", 'w') as jawf:
            jawf.write(name)
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
                    '   try:\n'
                    '       from apps import setup\n'
                    '       setup.run(server)\n',
                    '   except ImportError:\n',
                    '       print("Project does not have any apps configured or apps\setup.py cannot be found")\n']
            for l in setuppy:
                stp.write(l)

        for dir in ['apps', 'pages']:
            with open(name+'/%s/__init__.py'%(dir), 'w') as jawf:
                jawf.write("#initialized for project: %s" %(name))
            with open(name+'/%s/.cmddir'%(dir), 'w') as jawf:
                jawf.write(dir)
        with open(name + '/apps/setup.py', 'w') as stp:
            stp.write('def run(server):\n')
        print ("Succesfully created jawf project: %s" %(name))

if __name__ == "__main__":
    import sys
    if len (sys.argv) < 3:
        print ("jawf takes at least 2 argument: \n Example: \n  jawf.py init Project1")
    else:
        print (sys.argv)
        arg1,arg2 = sys.argv[1], sys.argv[2] 
        if arg1 == 'init':
            init(arg2)
        #TODOO - add app
        if arg1 == 'app':
            #init(arg2)
            #TODOO - add app
            if len(sys.argv) > 3:
                arg3 = sys.argv[3]
                if arg2 == 'add':
                    print ("adding app")
                    #arg4 = sys.argv[4]
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
        #TODOO - add webpage 