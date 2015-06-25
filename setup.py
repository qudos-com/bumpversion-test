#!/usr/bin/env python
import os
import re
import subprocess
import sys

from setuptools import find_packages, setup

version = None
for l in open('version.py'):
    try:
        version = re.match('__version__\s*=\s*[\'\"](.+)[\"\']', l).groups(1)[0]
        break
    except AttributeError:
        pass

assert version, "Could not find version"


def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')


if sys.argv[-1] == 'publish':
    current_branch = next(run_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])).strip()
    if current_branch != 'master':
        print "not currently on master branch!"
        sys.exit(1)
    last_commit_message = next(run_command(['git', 'log', '-1', '--pretty=%B'])).strip()
    if not last_commit_message.startswith('Bump version:'):
        print "Last commit was not a version bump"
        print "Run 'bumpversion' to create a new version tag"
        sys.exit(1)

    print "Pushing latest code/tags"
    if os.system("git push"):
        print "error pushing code"
        sys.exit(1)
    if os.system("git push --tags"):
        print "error pushing tags"
    print "Uploading to source distribution qudos pypi"
    os.system("python setup.py sdist upload -r qudos")
    sys.exit()


def inject_custom_repository(repository_name):
    blacklist = ['register', 'upload']
    inject_arg = '--repository=%s' % (repository_name)

    for command in blacklist:
        try:
            index = sys.argv.index(command)
        except ValueError:
            continue

        sys.argv.insert(index + 1, inject_arg)

inject_custom_repository('qudos')


setup(
    name='bumpversion-test',
    description='''Tiny services for everyone.''',
    version=version,
    author='Qudos',
    author_email='simon@qudos.com',
    url='http://github.com/qudos/bumpversion-test',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
)
