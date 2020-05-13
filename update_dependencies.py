import json
import os
import sh
from pathlib import Path
import git


dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
# git = sh.git.bake(_cwd=dir_path)

repo = git.Repo(dir_path)

# git.config('--global', 'user.email', 'ayanb9440@gmail.com')
# git.config('--global user.name "Ayan Bandyopadhyay"')

dependency_graph = {
	'report.txt': ['update_dependencies.py']
}

class Tag:
	def __init__(self, path):

		# prefix is "refs/tags/"
		i = len("refs/tags/")
		j = len(path) - 2

		while path[j] != '_' and path[j+1] != 'v':
			j -= 1
		self.filename = path[i:j]
		self.version = float(path[j+2:])
		self.message = tagref.tag.message

	def get_name(self):
		return self.filename + '_v' + str(self.version)

	def increment(self):
		self.version += 0.1

		


def get_latest_tag(filename):
	tagrefs = sorted(repo.tags, key=lambda t: t.commit.committed_datetime, reverse: True)

	for tagref in tagrefs:
		tag = Tag(tagref.path)
		if filename == tag.filename:
			return tag
	return Tag('refs/tags' + filename + '_v0.9')



def update_file(filename, dependencies):

	latest_tag = get_latest_tag(filename)
	latest_tag.message = ''
	print(latest_tag)

	contents = ''
	for dep in dependencies:

		latest_tag.message += get_latest_tag(dep).get_name()
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

	latest_tag.increment()
	new_tag = repo.create_tag(latest_tag.get_name(), message = latest_tag.message)
	origin = repo.remote('origin')
	origin.push()
	origin.push(new_tag)


home = str(Path.home())
changed_files = None

# with open(home + "/files.json") as file:
# 	changed_files = json.load(file)

# changed_file = changed_files[0]
changed_file = 'update_dependencies.py'
for (filename, dependencies) in dependency_graph.items():
	if changed_file in dependencies:
		update_file(filename, dependencies)

# print(git.tag()[0])



