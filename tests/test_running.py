import requests
from app import app
from tests.test_base import TestPortsBase

#NB, for running code.
class TestFlaskRunning(TestPortsBase):

    def setUp(self):
        self.PORT_OUT = self.get_ports_dockercompose()[0]
        dockerfile_string = self.get_dockerfile_string()
        host_and_port = self.get_container_host_and_port(dockerfile_string)
        self.HOST = host_and_port[0]
        self.URL = "http://" + self.HOST + ":" + str(self.PORT_OUT)+ "/" + app.app_name + "/"

    #def test_URL(self):
    #    self.assertEqual(self.URL, "http://0.0.0.0:3000/testingCI/")


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