import os
import sh
from pathlib import Path
import git
import dvc.api
from dvc.repo import Repo

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
shgit = sh.git.bake(_cwd=dir_path)

repo = git.Repo(dir_path)



# latest tag: 'data6_v1.2'

resource_url = dvc.api.get_url(
    'data6/',
    repo='https://github.com/Ayan-Bandyopadhyay/yeet'
    )

print(resource_url)

Repo.get('https://github.com/Ayan-Bandyopadhyay/yeet', 'data6/')