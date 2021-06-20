#!/usr/bin/python3

import argparse
import glob
import subprocess
import os


def conan_export(file, keep_source):
    conan_arguments = ["conan", "export", file, "alex_profile/stable"]
    if keep_source:
        conan_arguments.insert(2, "--keep-source")
    return conan_arguments


def os_current_file_path():
    return os.path.dirname(os.path.abspath(__file__))


def conan_files():
    return glob.iglob(os.path.join(os_current_file_path(), '**', 'conanfile.py'))


def get_args():
    parser = argparse.ArgumentParser(description='Configure conan recipes.')
    parser.add_argument('-k', '--keep-source', dest='keep_source', action='store_true', help='keep source')
    return parser.parse_args()


args = get_args()
for file in conan_files():
    subprocess.run(conan_export(file, args.keep_source))
