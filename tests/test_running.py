import unittest
import requests

#NB, for running code.
class TestFlaskRunning(unittest.TestCase):
    URL = "http://0.0.0.0:5000/" 

    def test_status_code(self):
        #Test that status code is OK.
        
        #Should maybe explore having a testing environment (test client...?)
        #url = "http://0.0.0.0:5000/" #Have so far not found a good way of getting the URL
        response = requests.head(self.URL)
        self.assertEqual(response.status_code, 200)

    def test_health_endpoint(self):
        health_url = self.URL + "health"
        response = requests.get(health_url)
        response_dict = response.json()
        self.assertEqual(response_dict["status"], "success")


if __name__ == '__main__':
    unittest.main()