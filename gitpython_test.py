import os
import sh
from pathlib import Path
import git
import dvc.api
from dvc.repo import Repo
import sys
from distutils.dir_util import copy_tree
import shutil

# ssh_password = sys.argv[1]

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
shgit = sh.git.bake(_cwd=dir_path)

repo = git.Repo(dir_path)

origin = repo.remote('origin')

# print(ssh_password)



# Repo.get('https://github.com/Ayan-Bandyopadhyay/yeet', 'data6/')

# shutil.rmtree('data6')
# os.makedirs('data6')
# with open("data6/copy.txt", "w") as file:
#     file.write("Your text goes here")

# dvc_repo = Repo()
# dvc_repo.add('data6')
# dvc_repo.pull()
# dvc_repo.push()


# repo.index.add('data6.dvc')
# repo.index.commit('update data6')
# origin.push()

from dvc.config import Config

config = Config()
with config.edit(0) as conf:                       
    conf["remote"]['myremote']['keyfile'] = 'value'