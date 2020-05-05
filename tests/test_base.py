import unittest
import yaml
import re
from dockerfile_parse import DockerfileParser
import os 
from app import app

class TestBase(unittest.TestCase):

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

    def get_container_port(self, dockerfile_string):
        '''
        #TODO: Could also get the host, but this part is currently skipped
        '''
        if self.is_gunicorn(dockerfile_string):
            return self.get_gunicorn_port(dockerfile_string)
        else:
            # No gunicorn
            #Must get port from app.py
            return self.get_app_port()
            

    def get_gunicorn_port(self, dockerfile_string):
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
            #No port is specified, then default for gunicorn is 8000
            #host = hp_ls[0] #TODO: Could also get host
            port=8000
        else:
            #host = hp_ls[0]
            port = int(hp_ls[1])
        return port
    
    def get_app_port(self):
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

    def cmd_last_in_dockerfile(self, path='app'):
        '''
        See if CMD is the last command in Dockerfile
        #TODO: The last strip() added here is for if the line starts with spaces. But maybe that will break the Dockerfile?

        '''
        dockerfile_string=self.get_dockerfile_string(path=path)
        num_CMD = dockerfile_string.count('CMD')
        if dockerfile_string.find('CMD[') != -1:
            string_modified= re.sub("CMD\[(.*?)\]", 'CMD[]', dockerfile_string)
            return string_modified.endswith('CMD[]')
        elif dockerfile_string.find('CMD') != -1:
            #CMD exists, but without brackets. Find last line of Dockerfile
            #and check if starts with CMD
            dfc = DockerfileParser(path=path)
            all_content = dfc.content.strip()#Remove trailing spaces
            last_line = all_content.split('\n')[-1].strip()
            return last_line.startswith('CMD')
        else: 
            #No CMD
            return False