#!/usr/bin/env python

import sys
import os
import subprocess


def publish(filepath):
    _, filename = os.path.split(filepath)
    name, ext = os.path.splitext(filename)
    if ext == '.ipynb':
        cmd = ('jupyter-nbconvert --to notebook '
               '--ClearOutputPreprocessor.enabled=True '
               '--execute '
               '{} --out htmls/{}')
        subprocess.check_call(cmd.format(filepath, filename).split())

        cmd = ('jupyter-nbconvert --to html '
               'htmls/{} --out htmls/{}.html')
        subprocess.check_call(cmd.format(filename, name).split())


def publish_folder(path):
    for dirpath, dirnames, filenames in os.walk(path):
        if os.path.basename(dirpath) != '.ipynb_checkpoints':
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                publish(filepath)


if __name__ == '__main__':

    assert len(sys.argv) > 1
    filepaths = sys.argv[1:]

    for filepath in filepaths:
        if not os.path.exists(filepath):
            print("error: {} not found".format(filepath))
            sys.exit(1)


    for filepath in filepaths:
        if os.path.isfile(filepath):
            publish(filepath)
        else:
            publish_folder(filepath)
