from tests.test_base import TestBase
import os

class TestDockerStructure(TestBase):

    def test_exists_requirements(self):
        assert(os.path.exists("app/requirements.txt"))

    def test_cmd_last_in_dockerfile(self):
        assert(self.cmd_last_in_dockerfile())
        
    
    

if __name__ == '__main__':
    unittest.main()
