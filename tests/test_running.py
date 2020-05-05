import requests
from app import app
from tests.test_base import TestBase

#NB, for running code.
class TestFlaskRunning(TestBase):
        
    def setUp(self):
        dockerfile_string = self.get_dockerfile_string()
        self.PORT= self.get_container_port(dockerfile_string)
        self.HOST = '0.0.0.0'
        self.URL = "http://" + self.HOST + ":" + str(self.PORT)+ "/" + app.app_name + "/"


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