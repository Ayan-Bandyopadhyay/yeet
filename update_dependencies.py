import json

data = None

with open("$HOME/files.json") as file:
	data = json.load(file)

print(data)