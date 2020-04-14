import json

import os

from pathlib import Path
home = str(Path.home())

data = None

with open(home + "/files.json") as file:
	data = json.load(file)

print(data)



dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)