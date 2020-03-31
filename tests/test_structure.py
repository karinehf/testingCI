from tests.test_base import TestPortsBase
import os

class TestDockerStructure(TestPortsBase):

    def setUp(self):
        self.PORT_COMPOSE= self.get_ports_dockercompose()[1]
        dockerfile_string = self.get_dockerfile_string()
        self.PORT_CONTAINER = self.get_container_port(dockerfile_string)

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

    def test_cmd_last_in_dockerfile(self):
        assert(self.cmd_last_in_dockerfile())
        
    
    

if __name__ == '__main__':
    unittest.main()
