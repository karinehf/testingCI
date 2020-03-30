import unittest
import yaml
import re
from dockerfile_parse import DockerfileParser
import os 
from app import app

class TestPortsBase(unittest.TestCase):

    def is_dockercompose(self, path='app'):
        filename = path + '/docker-compose.yml'
        return os.path.exists(filename)

    def get_ports_dockercompose(self, path = 'app'):
        if self.is_dockercompose(path = path):
            filename = path + '/docker-compose.yml'
            with open(filename, 'r') as stream:
                try:
                    yml_dict = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)
            ports_str = yml_dict['services']['app']['ports'][0]
            ports= ports_str.split(':')
            return([int(ports[0]), int(ports[1])])
        else: 
            #TODO: Figure out what to do if there is no compose-file
            return([None, None])

    def get_dockerfile_string(self, path='app'):
        '''
        Read dockerfile, remove comments, remove newlines and whitespaces
        Return as single string
        '''
        dfc = DockerfileParser(path=path)
        all_content = dfc.content
        lines = all_content.split('\n')
        new_content = ''
        for line in lines: 
            #Removes part of lines after # (but comments will perhaps only start at beginning of line?)
            newline = line.split('#', 1)[0]
            new_content= new_content + newline
        #Remove all whitespaces
        stripped_content = "".join(new_content.split())
        return(stripped_content)

    def is_gunicorn(self, dockerfile_string):
        '''
        Check if the dockerfile is using gunicorn
        '''
        if dockerfile_string.find('gunicorn') != -1:
            return True
        else:
            return False

    def get_container_host_and_port(self, dockerfile_string):
        
        if self.is_gunicorn(dockerfile_string):
            '''
            #TODO: If gunicorn is used, we assume host is always specified there.
            '''
            return self.get_gunicorn_host_and_port(dockerfile_string)
        else:
            '''
            #TODO: If gunicorn is not used, we assume host is always specified in app.py
            '''
            # No gunicorn
            #Must get host and port from app.py
            return self.get_app_host_and_port()
            

    def get_gunicorn_host_and_port(self, dockerfile_string):
        '''
        #TODO: If gunicorn is used, we assume host is always specified there.
        '''
        
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
            #No port is specified
            host = hp_ls[0]
            port=8000
        else:
            host = hp_ls[0]
            port = int(hp_ls[1])
        return [host, port]

    def get_app_host_and_port(self):
        '''
        #TODO: If gunicorn is not used, we assume host is always specified in app.py
        #TODO: We assume host and port are always given as variable
        '''
        host = app.host
        port_temp = app.port
        if port_temp is None:
            #Default port
            port = 5000
        else: 
            #If the port is a string which cannot be transformed to int, it seems the app will not run.
            #TODO: Exception if port is not valid
            port = int(port_temp)

        return [host, port]