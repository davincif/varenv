# varenv
[![current](https://img.shields.io/badge/version-1.0.1--rc%20-brightgreen.svg)](https://pypi.org/project/simplestRPC/) :green_heart:
[![license](https://img.shields.io/badge/license-zlib-brightgreen.svg)](https://www.zlib.net/zlib_license.html)
[![python](https://img.shields.io/badge/python-3.5+-brightgreen.svg)](https://python.org)

A simple way to mock your environment variables during development.

Just add'em to the varenv.conf.json and have fun =). The varenv package will not overwrite any already existente environment variables.

This library was designed to be inbuilt in pojects that, when going to production, will consume environment variable, very commonly used in application that'll run in docker containers. So, they need something to mock these variable under development but that won't get in the way in production.

### Usage

Create a file called 'varenv.conf.json' at your project's root path like this:
```json
{
  "SRPC_SERVER": "127.0.0.1",
  "SRPC_SERVER_PORT": "2727",
  "ANY_OTHER_VARIABLE_I_DESIRE": 567865
}
```

now use it like this in your program:
```python
import os
import varenv

my_server_ip = os.getenv("SRPC_SERVER")
my_server_port = os.getenv("SRPC_SERVER_PORT")
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

---

### Author's Note
create by me, [davincif](https://www.linkedin.com/in/davincif/), this project of first though the needs of a another professional project made by me. But it sounds so potentially useful the the community that I decided to open this package here freely distributed.

I have no intention to continue enhancing this project professionally, but would love to carry its development with the community if there's anyone interest.

So let me know if you want to help, or also if you need any formal concentiment to use this software, despite the fact that it's already free and open by terms of a very permissive license as zlib.

<br>

##### See also
[SimplestRPC](https://github.com/davincif/simplestRPC) project
