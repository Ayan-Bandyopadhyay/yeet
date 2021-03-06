import json
import os
import sh
from pathlib import Path
import git
from dvc.repo import Repo
from distutils.dir_util import copy_tree

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
# git = sh.git.bake(_cwd=dir_path) 

repo = git.Repo(dir_path)
origin = repo.remote('origin')
dvc_repo = Repo()

# git.config('--global', 'user.email', 'ayanb9440@gmail.com')
# git.config('--global user.name "Ayan Bandyopadhyay"')

dependency_graph = {
	'data6.dvc': ['data5.dvc']
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


	def get_name(self):
		return self.filename + '_v' + ("%0.1f" % self.version)

	def increment(self):
		self.version += 0.1

		


def get_latest_tag(filename):
	origin.pull()
	tagrefs = sorted(repo.tags, key=lambda t: t.commit.committed_datetime, reverse= True)
	for tagref in tagrefs:
		print(tagref.path)
		tag = Tag(tagref.path, '')
		if tagref.tag is not None:
			tag.message = tagref.tag.message
			
		if filename == tag.filename:
			return tag
	return Tag('refs/tags/' + filename + '_v0.9', '')



def update_file(filename, dependencies):
	print(filename)

	latest_tag = get_latest_tag(filename)
	latest_tag.message = ''

	contents = ''

	dir_name = filename[:len(filename) - len('.dvc')]
	os.makedirs(dir_name)

	for dependency in dependencies:

		dep_file = dependency
		if isinstance(dep_file, dict):
			dep_file = list(dep_file.keys())[0]

		latest_tag.message += get_latest_tag(dep_file).get_name()
		# each dependency is a .dvc file corresponding to a folder
		# get url of dependency folder

		name = dependency[:len(dependency) - len('.dvc')]

		Repo.get('https://github.com/Ayan-Bandyopadhyay/yeet', name)

		copy_tree(name, dir_name)


	dvc_repo.add(dir_name)
	dvc_repo.pull()
	dvc_repo.push()

	repo.index.add([filename])

	msg = 'update ' + filename + ' based on dependencies'
	repo.index.commit(msg)

	latest_tag.increment()
	new_tag = repo.create_tag(latest_tag.get_name(), message = latest_tag.message)
	origin.push()
	origin.push(new_tag)
	find_and_update_dependencies(dependency_graph, filename)




# changed_file = 'update_dependencies.py'


def find_and_update_dependencies(graph, changed_file):
	for (filename, dependencies) in graph.items():
		should_update = False
		for dependency in dependencies:


			if isinstance(dependency, dict) and list(dependency.keys())[0] != changed_file:
				find_and_update_dependencies(dependency, changed_file)
			elif isinstance(dependency, dict) and list(dependency.keys())[0] == changed_file:
				update_file(filename, dependencies)
			elif isinstance(dependency, str) and dependency == changed_file:
				update_file(filename, dependencies)

def update_tag(filename):
	latest_tag = get_latest_tag(filename)
	latest_tag.increment()
	new_tag = repo.create_tag(latest_tag.get_name(), message = latest_tag.message)
	origin.push(new_tag)


home = str(Path.home())
changed_file = None

with open(home + "/files.json") as file:
	changed_file = json.load(file)[0]

if changed_file[0] != '.':
	print("updating tags")
	update_tag(changed_file)

print("updating dependencies")
find_and_update_dependencies(dependency_graph, changed_file)
		


	

# print(git.tag()[0])



