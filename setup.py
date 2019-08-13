#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import find_packages, setup
from distutils.util import convert_path

print(sys.argv, sys.path)
print(list(os.walk('.')))

pkgname = 'pygrpc'  # this is imported with 'import pygrpc'

setupdir = os.path.dirname(__file__)

def get_version(pkg_name):
    ver_path = convert_path('{}/version.py'.format(pkg_name))
    with open(ver_path) as ver_file:
        text = ver_file.read()
    try:
        ver = text.split('version=')[1]
    except IndexError:
        raise RuntimeError('Could not parse version string: {}'.format(text))
    return ver.strip('"').strip("'")


def get_git_version():
    from subprocess import Popen, PIPE
    lastdir = os.getcwd()
    os.chdir(setupdir)
    p = Popen(['git', 'rev-parse', '--short', 'HEAD'], stdout=PIPE)
    gitsha, err = p.communicate()
    gitsha = gitsha.decode().replace('\n', '')
    q = Popen(['git', 'status', '--porcelain'], stdout=PIPE)
    dirty_files, err = q.communicate()
    os.chdir(lastdir)
    if dirty_files:
        gitsha += '-dirty'
    return gitsha
