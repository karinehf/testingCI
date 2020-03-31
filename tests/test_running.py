import requests
from app import app
from tests.test_base import TestPortsBase

#NB, for running code.
class TestFlaskRunning(TestPortsBase):

    def setUp(self):
        self.PORT_OUT = self.get_ports_dockercompose()[0]
        self.HOST = '0.0.0.0'
        self.URL = "http://" + self.HOST + ":" + str(self.PORT_OUT)+ "/" + app.app_name + "/"


    def test_status_code(self):
        #Test that status code is OK.
        response = requests.head(self.URL)
        self.assertEqual(response.status_code, 200)

    def test_health_endpoint(self):
        #Test that status code is OK by using health endpoint
        health_url = self.URL + "health"
        response = requests.get(health_url)
        response_dict = response.json()
        self.assertEqual(response_dict["status"], "success")


if __name__ == '__main__':
    unittest.main()