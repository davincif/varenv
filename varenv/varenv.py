import os
import json
try:
    import yaml
    hasyaml = True
except Exception as exp:
    hasyaml = False


# local vars
__CONF_FILE = None

# exported vars
envyVars = {}


# local funtions
def __detect_confile_extension():
    global __CONF_FILE

    # file ends in yaml or yml?
    fileext = ""
    filetype = ""
    if os.path.isfile(__CONF_FILE + ".json"):
        fileext = "json"
        filetype = "json"
    elif os.path.isfile(__CONF_FILE + ".yml"):
        fileext = "yml"
        filetype = "yml"
    elif os.path.isfile(__CONF_FILE + ".yaml"):
        fileext = "yaml"
        filetype = "yml"

    return [filetype, fileext]


def __search_alias(varname: str, conf_dict):
    alias_found = ''
    value = None

    if 'alias' not in conf_dict[varname]:
        print("Varenv error: variable '%s' has no alias. Ignoring..." % varname)
    elif 'value' not in conf_dict[varname]:
        print("Varenv error: variable '%s' has no value. Ignoring..." % varname)
    else:
        for alias in conf_dict[varname]['alias']:
            envval = os.getenv(alias)
            if envval is not None:
                # check of unsuported types
                if not isinstance(conf_dict[varname]['value'], (int, float, complex, str, bool)):
                    raise TypeError("%s, with value: %s. Is of type %s but only (int, float, complex, str, bool) are supported yet" % (
                        varname, str(conf_dict[varname]['value']), type(conf_dict[varname]['value'])))

                # set responses
                alias_found = alias
                value = envval
                break

    return [alias_found, value]


def __get_var(varname: str, conf_dict):
    value = None

    typeof = type(conf_dict[varname])
    # check of unsuported types
    if not isinstance(conf_dict[varname], (int, float, complex, str, bool, dict)):
        raise TypeError("%s, with value: %s. Is of type %s but only (int, float, complex, str, bool) are supported yet" % (
            varname, str(conf_dict[varname]), type(conf_dict[varname])))

    # check which variable and value is gonna be added, if any
    if typeof is dict:
        # check if object has the needed params
        if 'alias' not in conf_dict[varname]:
            varname = ''
            print("Varenv error: variable '%s' has no alias. Ignoring..." % varname)
        elif 'value' not in conf_dict[varname]:
            varname = ''
            print("Varenv error: variable '%s' has no value. Ignoring..." % varname)
        else:
            # search for the alias
            varfound, valuefound = __search_alias(varname, conf_dict)
            if not varfound:
                value = conf_dict[varname]['value']
            else:
                varname = varfound
                value = valuefound
            typeof = type(value)
    else:
        # get var value, add on the os env and the envyVars obj
        value = conf_dict[varname]

    # now add value to varname if any was found
    if varname:
        value = value if typeof is str else str(value)
        envval = os.getenv(varname)
        if envval is None:
            os.environ[varname] = value
        else:
            typeof = type(envval)

    return [value, typeof]


def __load_envy():
    global __CONF_FILE
    global envyVars

    # load __CONF_FILE and add standard file
    if __CONF_FILE is None:
        __CONF_FILE = os.getenv("VARENV_CONF_FILE_PATH")
        if __CONF_FILE is None:
            __CONF_FILE = "./varenv.conf"

    # load local enviroment variables
    conf_dict = None
    try:
        filetype, fileexp = __detect_confile_extension()
        if filetype == 'yml' and hasyaml:
            print("ymal module detected")
            filename = __CONF_FILE + "." + fileexp
            with open(filename, "r") as confFile:
                conf_dict = yaml.load(confFile, Loader=yaml.FullLoader)
        elif filetype == 'json':
            print("loading with json")
            with open(__CONF_FILE + ".json", "r") as confFile:
                conf_dict = json.loads(confFile.read())
        elif filetype == 'yml' and not hasyaml:
            print("Varenv warning: the file present is '%s.%s' but there's not yaml models" % (__CONF_FILE, fileexp))
        else:
            print("Varenv warning: file '%s.(json, yml or yaml)' is not present, you are depending entirely on the already declared enviroment variables. If you are in produciton, ignore this warning." % __CONF_FILE)
    except FileNotFoundError:
        # nothing to be loaded
        print("Varenv warning: file '%s.(json, yml or yaml)' is not present, you are depending entirely on the already declared enviroment variables. If you are in produciton, ignore this warning." % __CONF_FILE)
    else:
        for config in conf_dict:
            # check of unsuported types
            value, typeof = __get_var(config, conf_dict)
            if value is not None:
                envyVars[config] = {'value': value, 'type': typeof}


def __update_and_clean_envy():
    global envyVars

    for var in envyVars:
        env = os.getenv(var)
        if env is None:
            del envyVars[var]
        elif env != envyVars[var]['value']:
            try:
                envyVars[var]['type'](env)
            except Exception as e:
                raise TypeError("The new '%s' variable has tye %s but show have %s" %
                                (var, str(type(env)), str(envyVars[var]['type'])))
            else:
                envyVars[var]['value'] = env


# exported functions
def refresh():

    if not envyVars:
        __load_envy()
    else:
        __update_and_clean_envy()


def get_env(varName, varType=str):
    global envyVars

    # search on already load variables
    if varName in envyVars:
        return envyVars[varName]['type'](envyVars[varName]['value'])

    # search in the system variables
    value = os.getenv(varName)
    if value is not None:
        envyVars[varName] = {'value': value, 'type': varType}
        return type(value)

    return None


refresh()


if __name__ == '__main__':
    var = 'two'
    a = get_env(var)
    print(var, a, type(a))
    os.environ[var] = '263734'
    refresh()
    var = 'two'
    a = get_env(var)
    print(var, a, type(a))
