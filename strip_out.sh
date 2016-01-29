#!/usr/bin/env python

import sys
import os
import subprocess

for dirpath, dirnames, filenames in os.walk(sys.argv[1]):
    if os.path.basename(dirpath) != '.ipynb_checkpoints':
        for filename in filenames:
            _, ext = os.path.splitext(filename)
            if ext == '.ipynb':
                filepath = os.path.join(dirpath, filename)
                cmd = ('jupyter-nbconvert --inplace --to notebook '
                       '--ClearOutputPreprocessor.enabled=True {} --out {}')
                subprocess.check_call(cmd.format(filepath, filepath).split())
