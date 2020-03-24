import unittest

class TestDockerStructure(unittest.TestCase):
    def test_specific_directory(self):
        #Tests this specific directory
        #Not any easier than just making sure the req. file is made. 
        import os.path as path
        assert(path.exists("first_flask_app/requirements.txt"))
    
    

if __name__ == '__main__':
    unittest.main()
