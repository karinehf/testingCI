import unittest
import os 

class TestDockerStructure(unittest.TestCase):

    def test_requirements_exists(self):
        #Tests this specific directory
        #Not any easier than just making sure the req. file is made. 
        assert(os.path.exists("app/requirements.txt"))
        
    
    

if __name__ == '__main__':
    unittest.main()
