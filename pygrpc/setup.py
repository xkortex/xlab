#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import find_packages, setup
from distutils.util import convert_path

superpkg = 'xlab'
pkgname = 'pygrpc'  # this is imported with 'import pygrpc'

setupdir = os.path.dirname(__file__)


def get_date_version():
    """returns the current time like '2019.8.13.17.15'"""
    from datetime import datetime
    return '.'.join(list(map(str, datetime.now().utctimetuple()))[:5])


def package_files(directories):
    if isinstance(directories, str):
        directories = [directories]
    paths = []
    for directory in directories:
        for (path, directories, filenames) in os.walk(directory):
            for filename in filenames:
                paths.append(os.path.join('..', path, filename))
    return paths

def compile_protobufs(pkgname='pygrpc', protod='proto'):
    """compile the protobuf files.
    A few notes:
        - Protoc/protobuf is VERY TOUCHY when it comes to python, paths, and
            packages. This is likely a continuous WIP as I figure out better
            patterns and methods.
        - I think the dot matters, sometimes.
        - If you want typical package namespacing, you are kinda stuck with
            repodir/pkgname/foobar/qux.proto which generates
            repodir/pkgname/foobar/qux_pb2.py if you want
            from pkgname.foobar import qux

    We want to emulate this command:
    python -m grpc_tools.protoc --proto_path=pygrpc/proto --python_out=. \
        --grpc_python_out=. pygrpc/proto/pygrpc/*.proto
    """
    from grpc_tools import protoc
    import shlex
    proto_path = os.path.join(pkgname, protod)
    out = protoc.main(shlex.split(
        "--proto_path={proto_path} "
        "--python_out={out} "
        "--grpc_python_out={out} "
        "./{proto_path}/time.proto".format(proto_path=proto_path, out='.')))
    if out:
        raise RuntimeError('Protobuf failed. Setup with --verbose to see why')


data_files = []

package_data = []

packages = find_packages(exclude=[])
print('Packages:', packages)

# common dependencies
# todo: fully test unified dependencies
deps = [
    'grpcio',
    'grpcio-tools',
    'protobuf'
]

compile_protobufs()

setup(
    name='.'.join([superpkg, pkgname]),
    version=get_date_version(),
    script_name='setup.py',
    python_requires='>3.5',
    zip_safe=False,
    packages=packages,
    install_requires=deps,
    data_files=data_files,
    include_package_data=True,
    extras_require={
    }
)

