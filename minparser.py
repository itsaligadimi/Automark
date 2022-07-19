import sys

app_name = ""
app_description = ""
app_footer_description = ""
commands = []

def add_command(command, description, function):
    commands.append({
        'command': command,
        'description': description,
        'function': function
    })

def run():  
    # print(sys.argv)
    try:
        first_arg = sys.argv[1]
        if first_arg[0] == '-':
            raise NoCommandException()
    except NoCommandException as exp:
        describe_app()
    
    for comm in commands:
        if first_arg == comm['command']:
            comm['function']()
            return

    print("Command not found")
    print("Use --help to get more information")

def describe_app():
    print(app_name)
    print(app_description)
    print("")
    if is_option_set('help'):
        print_help()
    else:
        print("Use --help to get more information")
    print("")
    print(app_footer_description)

def print_help():
    print("Commands:")
    for comm in commands:
        print("\t%s\t\t%s" % (comm['command'], comm['description']))
    



def get_param(name, default_value=None):
    try:
        for idx,arg in enumerate(sys.argv):
            if arg == '-' + name:
                return sys.argv[idx + 1]
        raise Exception()
    except:
        if default_value is not None:
            return default_value
        else:
            print('%s is required' % name)
            exit()



def get_param_arr(name, default_value=None):
    try:
        out = []
        for idx,arg in enumerate(sys.argv):
            if arg == '-' + name:
                out.append(sys.argv[idx + 1])

        if len(out):
            return out
        raise Exception()
    except:
        if default_value is not None:
            return default_value
        else:
            print('%s is required' % name)
            exit()


def is_option_set(name):
    for idx,arg in enumerate(sys.argv):
        if arg == '--' + name:
            return True
    return False


class NoCommandException(Exception):
    pass