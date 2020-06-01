import os
import sh
from pathlib import Path
import git
import dvc.api
from dvc.repo import Repo
import sys

# ssh_password = sys.argv[1]

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
shgit = sh.git.bake(_cwd=dir_path)

repo = git.Repo(dir_path)



# print(ssh_password)



Repo.get('https://github.com/Ayan-Bandyopadhyay/yeet', 'data6/')