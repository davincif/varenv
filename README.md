# Varenv
[![current](https://img.shields.io/badge/version-1.0.6%20-brightgreen.svg)](https://pypi.org/project/simplestRPC/) :green_heart:
[![license](https://img.shields.io/badge/license-zlib-brightgreen.svg)](https://www.zlib.net/zlib_license.html)
[![python](https://img.shields.io/badge/python-3.5+-brightgreen.svg)](https://python.org)

A simple way to mock your environment variables during development.

Just add'em to the varenv.conf.json and have fun =). The varenv package will not overwrite any already existente environment variables.

This library was designed to be inbuilt in pojects that, when going to production, will consume environment variable, very commonly used in application that'll run in docker containers. So, they need something to mock these variable under development but that won't get in the way in production.

<br>

## Basic Usage

Create a file called `varenv.conf.json` at your project's root path like this:
```json
{
  "SRPC_SERVER": "127.0.0.1",
  "SRPC_SERVER_PORT": "2727",
  "ANY_OTHER_VARIABLE_I_DESIRE": 567865
}
```

It can also be YAML file called `varenv.conf.yml` or `varenv.conf.yaml`. The equivalent to the above file being:
```yml
SRPC_SERVER: 127.0.0.1
SRPC_SERVER_PORT: '2727'
ANY_OTHER_VARIABLE_I_DESIRE: 567865
```

now use it like this in your program:
```python
import varenv.varenv as varenv

my_server_ip = varenv.get_env("SRPC_SERVER")
my_server_port = varenv.get_env("SRPC_SERVER_PORT")

# after a while, for some reason, something chaged your enviroment variables values
# then refresh it
varenv.refresh()
new_server_port = varenv.get_env("SRPC_SERVER_PORT")
```

<br>

If you want to change the location of the *virenv.conf.json* file, you can define a environment variable called **VARENV_CONF_FILE_PATH** to any path you desire.

You can do that in a variaty of ways, here is two exemples:

by python:
```python
import os
os.environ['VARENV_CONF_FILE_PATH'] = '/folder/my_path/virenv.conf.json'
import varenv
```

<br>

by your .bashrc file:
```python
VARENV_CONF_FILE_PATH=/folder/my_path/virenv.conf.json
```

<br>

by bash when calling your python program:
```python
VARENV_CONF_FILE_PATH=/folder/my_path/virenv.conf.json python3 my_program.py
```

<br>

## Using Variales with Alias
In the version 1.0.6 a new feature was added thinking about the following user case: considering the existense of 3 clusters environments in a company's cloud system, let's say: development, production and homolog; and a CI/CD server like GitLab's* one *─[have a look](https://docs.gitlab.com/ee/ci/)─* is also being used. It may be needed to use the same variable with different values across all these clusters, this can lead to a problem when configuring that on GitLab's enviroment variables.

**Exemple**: Supposing the need to define a database password. That's gonna have different values on the development, production and homolog clusters enviroments, also it's gotta a value for the developer to use in his personal machine. To approach this question, define the *varenv.conf.yml* file like this:
```yml
DATA_BASE_ENDPOINT: localhost
DATA_BASE_PORT: '5432'
DATA_BASE_PASSWORD:
    alias:
        - DATA_BASE_PASSWORD_PROD
        - DATA_BASE_PASSWORD_HOMOLOG
        - DATA_BASE_PASSWORD_DEV
    value: p@ssword_f0r_the_developer
ANY_OTHER_VARIABLE_I_DESIRE: 567865
```
In the python code call the variable *DATA_BASE_PASSWORD* like this:
```python
import varenv.varenv as varenv


data_base_endpoint = varenv.get_env("DATA_BASE_ENDPOINT")
data_base_port = varenv.get_env("DATA_BASE_PORT")
data_base_password = varenv.get_env("DATA_BASE_PASSWORD")

# NOTE: the value defined within the code is gonna be the dict's key that defines the alias in the config file.

```
In the CI/CD server define the variables: *DATA_BASE_PASSWORD_PROD*, *DATA_BASE_PASSWORD_HOMOLOG* and *DATA_BASE_PASSWORD_DEV*, passing each one to it's respective cluster.

<br>

### How does it work?
When the Varenv get started and the variable with an alias is found, the module will search for the presence of every value in the alias array in the enviroment, stoping at the first match case found.

**Note**: The variables are gonna be searched at the same order as presented in the alias array in the file, and be resented to the programmer as in the object key. So if, for whatever reason, in the above exemple *DATA_BASE_PASSWORD_PROD* and *DATA_BASE_PASSWORD_DEV* get defined in the same enviroment, only the value of the first one will be taken into consideration and will be available in code as *DATA_BASE_PASSWORD*.

<br>

---

### Author's Note
create by me, [davincif](https://www.linkedin.com/in/davincif/), this project was first though to fulfill the needs of a another professional project I've made. But it sounds so potentially useful the the community that I decided to open this package here freely distributed.

I actively use this project since I created it back in 2018, and it happens to be pretty useful. Wich is surprising given that I thought it would be a one project thing. Thus I decided keep maintaining it, basically by solving bugs and adding new features required by other projects.

So let me know if you want to help out, or if you need any formal concentiment to use this software, despite the fact that it's already free and open by terms of a very permissive license as [zlib](https://opensource.org/licenses/Zlib).

<br>

##### See also
- [Dependency Manager](https://github.com/davincif/dependency_manager) project: A simple way of managing pip dependencies, separating in dev and prod, and tracking them.
- [SimplestRPC](https://github.com/davincif/simplestRPC) project: A simple RPC for python - *study project*.
