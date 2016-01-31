#!/usr/bin/env python
import subprocess


cmds = [  # upgrading pip
        ('pip install -U pip', None),
        #   # initializing submodules
        #('git submodule init', None),
        #('git submodule update', None),
        #   # installing third-party libraries
        ('pip install -r requirements.txt', './submodules'),
       ]

  # installing submodules
for pkg in ['scicfg', 'clusterjobs',
            'environments', 'fastlearners', 'learners', 'explorers',
            'experiments']:

    cwd = './submodules/{}'.format(pkg)
    #cmd = 'git describe --tags --dirty --always --long'
    cmd = 'pip uninstall {} -y; pip install -e .'.format(pkg)
    cmds.append((cmd, cwd))


if __name__ == '__main__':
    for cmd, cwd in cmds:
        print(cmd, cwd)
        p = subprocess.check_call(cmd, shell=True, cwd=cwd, stderr=subprocess.STDOUT)
