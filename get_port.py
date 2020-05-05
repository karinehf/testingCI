from tests import test_base
import os
test_base_obj = test_base.TestBase()
dockerfile_string = test_base_obj.get_dockerfile_string()
PORT= test_base_obj.get_container_port(dockerfile_string)
print(PORT)
