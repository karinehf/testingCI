
from first_flask_app import app #Works for python3, not for python 2.7
import unittest

class TestFlaskContent(unittest.TestCase):
    
    def test_hello_world(self):
        #Tests content of web app.
        self.assertEqual(app.hello_world(), "Hello World!")

if __name__ == '__main__':
    unittest.main()