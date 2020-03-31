#print("Hello World")

#import os
#print(os.getcwd())
#full_dir = os.path.dirname(os.getcwd())
#print(full_dir)
#dir_folder = os.path.basename(full_dir)
#print(dir_folder)

#import yaml
#with open("app/docker-compose.yml", 'r') as stream:
#    try:
#        yml_dict = yaml.safe_load(stream)
#    except yaml.YAMLError as exc:
#        print(exc)
#ports_str = yml_dict['services']['web']['ports'][0]
#ports= ports_str.split(':')
#portOut = int(ports[0])
#portsIn = int(ports[1])
#print(str(portsIn))
#print(type(str(portsIn)))

import re
from dockerfile_parse import DockerfileParser

def get_dockerfile_string(my_path=''):
    '''
    Read dockerfile, remove comments, remove newlines and whitespaces
    Return as single string
    '''
    dfc = DockerfileParser(path=my_path)
    all_content = dfc.content
    lines = all_content.split('\n')
    new_content = ''
    for line in lines: 
        #Removes part of lines after # (but comments will perhaps only start at beginning of line?)
        newline = line.split('#', 1)[0]
        new_content=''.join([new_content, newline])
    #Remove all whitespaces
    stripped_content = "".join(new_content.split())
    return(stripped_content)

def is_gunicorn(dockerfile_string):
    '''
    Check if the dockerfile is using gunicorn
    '''
    if dockerfile_string.find('gunicorn') != -1:
        return True
    else:
        return False

def get_gunicorn_port(dockerfile_string):
    '''
    If gunicorn is used, use regex to find the port specified for gunicorn
    '''
    if is_gunicorn(dockerfile_string):
        try:
            hp_match= re.search("\-b\",\"(.*?)\"", dockerfile_string)
            if hp_match:
                hp_str = hp_match.group(1)
            else: 
                hp_match= re.search("\-bind\",\"(.*?)\"", dockerfile_string)
                hp_str = hp_match.group(1)
        except:
            #Not sure how to handle this in a good way
            print("No string matches the regex pattern")
            raise

        hp_ls = hp_str.split(':')
        #Do not get the host now, but can easily do so.
        if len(hp_ls)==1:
            port_dockerfile=None
        else:
            port_dockerfile = int(hp_ls[1])
            return port_dockerfile
    else:
        #Should be difference between not using gunicorn and not having port specified?
        return None

def cmd_last_in_dockerfile(path='app'):
    '''
    See if CMD is the last command in Dockerfile
    '''
    dockerfile_string=get_dockerfile_string(path)
    num_CMD = dockerfile_string.count('CMD')
    if dockerfile_string.find('CMD[') != -1:
        string_modified= re.sub("CMD\[(.*?)\]", 'CMD[]', dockerfile_string)
        return string_modified.endswith('CMD[]')
    elif dockerfile_string.find('CMD') != -1:
        #CMD exists, but without brackets. Find last line of Dockerfile
        #and check if starts with
        dfc = DockerfileParser(path=path)
        all_content = dfc.content.strip()
        last_line = all_content.split('\n')[-1].strip()
        #strip added here if it may start with spaces. But maybe that will break the Dockerfile?
        return last_line.startswith('CMD')
    else: 
        #No CMD
        return False

from app import app
import re
def get_app_port():
    try: 
        #host = app.host #TODO: Could also get the host
        port_temp = app.port
        if port_temp is None:
            #Default port for flask app
            port = 5000
        else: 
            #TODO: Exception if port is not valid?
            port = int(port_temp)
        return port
    except:
        #host = None #Finding host skipped
        port = None

        with open("app/app.py", "r") as f:
            lines = f.readlines()
            port_var = "port"
            keyword_found = False
            for line in reversed(lines):
                #Removes part of lines after #
                line = line.split('#', 1)[0]
                port_match = re.search("(?:^|;| ) *" + port_var + " *= *([A-Za-z0-9_\.-]*)", line)
                if port_match:
                    keyword_found=True
                    port_str = port_match.group(1)
                    #TODO: Here we assume we will find valid output
                    try: 
                        port = int(port_str)
                        break
                    except:
                        port_var = port_str
                else:
                    continue
            if port is None and not keyword_found: 
                port = 5000

        return port


print(get_app_port())
'''
line = "port = 3000 #hello"
port_var = "port"
port_match = re.search("(?:^|;) *" + port_var+ " *= *([A-Za-z0-9]*)", line)
port_str = port_match.group(1)
print(len(port_str))
print(port_str)
'''

