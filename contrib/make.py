#!/usr/bin/python3
import os
import configparser
import subprocess
import argparse


class DirectoryHolder(object):

    def __init__(self, cd):
        self.work_dir = cd
        self.base_dir = os.getcwd()

    def __enter__(self):
        os.makedirs(self.work_dir, exist_ok=True)
        os.chdir(self.work_dir)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.base_dir)


#
# Tools
#
def os_windows():
    return os.name == 'nt'


def os_current_file_path():
    return os.path.dirname(os.path.abspath(__file__))


#
# Env variables
#
def windows_vcvars_path():
    return os.path.join('C:\\', 'Program Files (x86)', 'Microsoft Visual Studio', '2019',
                        'Community', 'VC', 'Auxiliary', 'Build', 'vcvars64.bat')


def wrap_with_windows_vcvars(func):
    def wrapper(*args, **kwargs):
        command = func(*args, **kwargs)
        if os_windows():
            return [windows_vcvars_path(), '&&'] + command
        return command
    return wrapper


def os_env():
    new_env = dict(os.environ)
    if not os_windows():
        new_env["CFLAGS"] = "-fPIC"
        new_env["CPPFLAGS"] = "-fPIC"
    return new_env


#
# Executors
#
def execute(command, raise_exception=True):
    p = subprocess.Popen(command, stderr=subprocess.PIPE, env=os_env())
    output, error = p.communicate()
    if p.returncode != 0 and raise_exception:
        raise ValueError("\n\n{}\n\ncommand: {}".format(error.decode(), ' '.join(command)))


def execute_in(output_path, command):
    with DirectoryHolder(cd=output_path) as dh:
        execute(command)

#
# Other
#
@wrap_with_windows_vcvars
def conan_install_command(conan_install_file_path, build_type, profile, target):
    return ['conan', 'install', conan_install_file_path,
            '--profile', profile,
            '--settings', 'build_type={}'.format(build_type.title()),
            '--build', target]


def get_args():
    parser = argparse.ArgumentParser(description='Configure conan recipes.', add_help=True)
    parser.add_argument('-g', '--debug', dest='build_type', action='store_const', const='debug', default='release',
                        help='debug')
    parser.add_argument('-p', '--package', dest='build_package', default='outdated', help='build package, default it will build all')
    return parser.parse_args()


#
# Main
#
args = get_args()

execute(['conan', 'profile', 'update', 'settings.compiler.cppstd=20', 'alex_profile'])

execute_in(output_path=os.path.join(os_current_file_path(), 'build', args.build_type, 'qt'),
           command=conan_install_command(
               conan_install_file_path=os_current_file_path(),
               build_type=args.build_type,
               profile='alex_profile',
               target=args.build_package))
