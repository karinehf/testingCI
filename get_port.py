from tests import test_base
import os
test_base_instance = test_base.TestBase()
dockerfile_string = test_base_instance.get_dockerfile_string()
PORT= test_base_instance.get_container_port(dockerfile_string)
print(PORT)
