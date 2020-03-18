
from first_flask_app import app #Works for python3, not for python 2.7
import unittest
import requests

class TestFlask(unittest.TestCase):
    
    def test_hello_world(self):
        #Tests content of web app.
        self.assertEqual(app.hello_world(), "Hello World!")
    
    def test_page(self):
        #Test that status code is OK.
        #NB, for running code.
        #Should maybe explore having a testing environment (test client...?)
        url = "http://127.0.0.1:5000/" #Have so far not found a good way of getting the URL
        response = requests.head(url)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()