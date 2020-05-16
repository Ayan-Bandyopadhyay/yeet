import json
import os
import sh
from pathlib import Path
import git


dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
# git = sh.git.bake(_cwd=dir_path)

repo = git.Repo(dir_path)
origin = repo.remote('origin')

# git.config('--global', 'user.email', 'ayanb9440@gmail.com')
# git.config('--global user.name "Ayan Bandyopadhyay"')

dependency_graph = {
	'report2.txt': [
		{
			'report.txt': ['update_dependencies.py']
		},
		'report3.txt'
	],
	'report4.txt': ['update_dependencies.py']
}

class Tag:
	def __init__(self, path, message):

		# prefix is "refs/tags/"
		i = len("refs/tags/") 
		j = len(path) - 2

		while path[j] != '_' and path[j+1] != 'v':
			if j == 0:
				self.filename = ''
				self.version = None
				self.message = None
				return
			j -= 1
		self.filename = path[i:j]
		self.version = float(path[j+2:])
		self.message = message
		print(self.filename)
		print(self.version)

	def get_name(self):
		return self.filename + '_v' + ("%0.1f" % self.version)

	def increment(self):
		self.version += 0.1

		


def get_latest_tag(filename):
	origin.pull()
	tagrefs = sorted(repo.tags, key=lambda t: t.commit.committed_datetime, reverse= True)
	print(tagrefs)
	for tagref in tagrefs:
		print(tagref.tag.message)
		tag = Tag(tagref.path, tagref.tag.message)
		if filename == tag.filename:
			return tag
	return Tag('refs/tags/' + filename + '_v0.9', '')



def update_file(filename, dependencies):

	latest_tag = get_latest_tag(filename)
	latest_tag.message = ''
	print(latest_tag)

	contents = ''
	for dependency in dependencies:

		dep_file = dependency
		if isinstance(dep_file, dict):
			dep_file = list(dep_file.keys())[0]

		latest_tag.message += get_latest_tag(dep_file).get_name()
		# each dependency is a .dvc file corresponding to a folder
		# get url of dependency folder
		with open(dep_file, 'r') as file:
			contents += file.read()

	with open(filename, 'w') as file:
		file.write(contents)
	repo.index.add([filename])

	msg = 'update ' + filename + ' based on dependencies'
	print(msg)
	repo.index.commit(msg)

	latest_tag.increment()
	new_tag = repo.create_tag(latest_tag.get_name(), message = latest_tag.message)
	print(new_tag)
	origin.push()
	origin.push(new_tag)


home = str(Path.home())
changed_files = None

with open(home + "/files.json") as file:
	changed_files = json.load(file)

changed_file = changed_files[0]
# changed_file = 'update_dependencies.py'


def find_and_update_dependencies(graph):
	for (filename, dependencies) in graph.items():
		should_update = False
		for dependency in dependencies:
			if isinstance(dependency, dict):
				find_and_update_dependencies(dependency)
			elif isinstance(dependency, str) and dependency == changed_file:
				update_file(filename, dependencies)


find_and_update_dependencies(dependency_graph)
		


	

# print(git.tag()[0])



