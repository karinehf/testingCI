print("Hello World")

import os
print(os.getcwd())
full_dir = os.path.dirname(os.getcwd())
print(full_dir)
dir_folder = os.path.basename(full_dir)
print(dir_folder)