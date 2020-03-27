from tests.test_base import TestPortsBase
import os

class TestDockerStructure(TestPortsBase):

    def setUp(self):
        self.PORT_COMPOSE= self.get_ports_dockercompose()[1]
        dockerfile_string = self.get_dockerfile_string()
        self.PORT_GUNICORN = self.get_gunicorn_port(dockerfile_string)

   
    def test_gunicorn_port(self):
         #Temporary test:
        assert(self.PORT_GUNICORN is None)

    def test_is_dockercompose(self):
        assert(self.is_dockercompose())

    def test_port_mapping(self):
        #No dockerfile/gunicorn port: 
        if not self.is_dockercompose():
            #What happens if there is no docker-compose file?
            assert(False)
        elif self.PORT_GUNICORN is None:
            #Must check what happens when gunicorn does not specify port
            assert(True)
        else:
            self.assertEqual(self.PORT_GUNICORN, self.PORT_COMPOSE)

    def test_exists_requirements(self):
        assert(os.path.exists("app/requirements.txt"))
        
    
    

if __name__ == '__main__':
    unittest.main()
