import unittest

class TestDockerStructure(unittest.TestCase):
    APP_FOLDER = "first_flask_app"

    def test_specific_directory(self):
        #Tests this specific directory
        #Not any easier than just making sure the req. file is made. 
        import os.path as path
        assert(path.exists(self.APP_FOLDER+"/requirements.txt"))
    
    

if __name__ == '__main__':
    unittest.main()
