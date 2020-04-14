import json

from pathlib import Path
home = str(Path.home())

data = None

with open(home + "/files.json") as file:
	data = json.load(file)

print(data)