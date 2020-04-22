import json
import os
import sh
from pathlib import Path

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
git = sh.git.bake(_cwd=dir_path)

dependency_graph = {
	'report.txt': ['reports/report1.txt', 'reports/report2.txt']
}

def update_file(filename, dependencies):
	contents = ''
	for dep in dependencies:
		with open(dep, 'r') as file:
			contents += file.read()
	with open(filename, 'w') as file:
		file.write(contents)
	git.add(filename)
	msg = 'update ' + filename + ' based on dependencies'
	git.commit(m=msg)
	git.push()



home = str(Path.home())
changed_files = None

with open(home + "/files.json") as file:
	changed_files = json.load(file)

for changed_file in changed_files:
	for (filename, dependencies) in dependency_graph:
		if changed_file in dependencies:
			update_file(filename, dependencies)

# print(git.tag()[0])



