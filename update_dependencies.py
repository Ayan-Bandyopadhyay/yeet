import json

import os

from pathlib import Path
home = str(Path.home())

data = None

with open(home + "/files.json") as file:
	data = json.load(file)

print(data)



for root, dirs, files in os.walk(home, topdown=True):
   for name in files:
      print(os.path.join(root, name))
   for name in dirs:
      print(os.path.join(root, name))