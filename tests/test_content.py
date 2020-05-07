
from app import app
import unittest

class TestFlaskContent(unittest.TestCase):
    
    def test_hello_world(self):
        #Tests content of web app.
        hW = app.HelloWorld()
        self.assertEqual(hW.get(), "Hello Wwworld!")

if __name__ == '__main__':
    unittest.main()