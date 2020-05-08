import json
import os
import sh
from pathlib import Path
import git


dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
git = sh.git.bake(_cwd=dir_path)

repo = git.repo(dir_path)

# git.config('--global', 'user.email', 'ayanb9440@gmail.com')
# git.config('--global user.name "Ayan Bandyopadhyay"')

dependency_graph = {
	'report.txt': ['data5.dvc', 'data6.dvc']
}

def update_file(filename, dependencies):

	tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
	print(tags)

	contents = ''
	for dep in dependencies:

		# each dependency is a .dvc file corresponding to a folder
		# get url of dependency folder
		with open(dep, 'r') as file:
			contents += file.read()
			
	with open(filename, 'w') as file:
		file.write(contents)
	repo.index.add([filename])

	msg = 'update ' + filename + ' based on dependencies'
	print(msg)
	repo.index.commit(msg)
	origin = repo.remote('origin')
	origin.push()



home = str(Path.home())
changed_files = None

with open(home + "/files.json") as file:
	changed_files = json.load(file)

changed_file = changed_files[0]
for (filename, dependencies) in dependency_graph.items():
	if changed_file in dependencies:
		update_file(filename, dependencies)

# print(git.tag()[0])



