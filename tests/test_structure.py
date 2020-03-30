from tests.test_base import TestPortsBase
import os

class TestDockerStructure(TestPortsBase):

    def setUp(self):
        self.PORT_COMPOSE= self.get_ports_dockercompose()[1]
        dockerfile_string = self.get_dockerfile_string()
        host_and_port = self.get_container_host_and_port(dockerfile_string)
        self.HOST = host_and_port[0]
        self.PORT_CONTAINER = host_and_port[1]

   
    #def test_container_port(self):
    #     #Temporary test:
    #    self.assertEqual(self.PORT_CONTAINER,5000)

    def test_is_dockercompose(self):
        #TODO: What to do if there is no compose-file?
        assert(self.is_dockercompose())

    def test_port_mapping(self):
        if not self.is_dockercompose():
            #TODO: What to do if there is no docker-compose file?
            assert(False)
        else:
            self.assertEqual(self.PORT_CONTAINER, self.PORT_COMPOSE)

    def test_exists_requirements(self):
        assert(os.path.exists("app/requirements.txt"))
        
    
    

if __name__ == '__main__':
    unittest.main()
