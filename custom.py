#!/usr/bin/env python
import string
import venv
import os
import sys
import subprocess
import argparse

parser = argparse.ArgumentParser(
    description='Processing commands from vscode tasks.')
parser.add_argument(
    'command',
    help='Command to execute',
    type=str,
    choices=[
        'prepare',
        'configure',
        'hello',
        'build',
        'serve',
        'preview',
        'publish',
    ]
)
args = parser.parse_args()

# Path to this file.


def getMyPath():
    if getattr(sys, 'frozen', False):
        return sys.executable
    elif __file__:
        return __file__

# Path to directory with this file.


def getMyDirectory():
    return os.path.dirname(getMyPath())


def isVirtualEnvironment():
    return sys.prefix != sys.base_prefix


def getEnvironmentDirectory():
    # Get path to venv directory.
    environmentDirectory = os.path.join(getMyDirectory(), '.venvs/pelican')
    environmentDirectory = os.path.normpath(environmentDirectory)
    return environmentDirectory


def passToVirtualEnvironment(command):
    environmentDirectory = getEnvironmentDirectory()

    # Run this file in venv.
    pythonBin = os.path.join(environmentDirectory, "Scripts/python.exe")
    pythonBin = os.path.normpath(pythonBin)
    scriptPath = getMyPath()
    # print(isVirtualEnvironment())
    res = subprocess.Popen([pythonBin, scriptPath, command])
    res.wait()


def hello():
    print("Hello!")


# Paths.
contentPath = os.path.join(getMyDirectory(), 'content')
outputPath = os.path.join(getMyDirectory(), 'output')
localConfigPath = os.path.join(getMyDirectory(), 'pelicanconf.py')
publishConfigPath = os.path.join(getMyDirectory(), 'publishconf.py')

# Prepare environmemt.


def prepare():
    environmentDirectory = getEnvironmentDirectory()

    # Create new venv with pip.
    builder = venv.EnvBuilder(clear=True, with_pip=True)
    builder.create(environmentDirectory)

    passToVirtualEnvironment('configure')


def configure():
    print('Executing inside venv...')
    subprocess.check_call([sys.executable, '-m', 'pip',
                           'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pelican'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'invoke'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Markdown'])
    subprocess.check_call(
        [sys.executable, '-m', 'pip', 'install', 'typogrify'])
    subprocess.check_call(
        [sys.executable, '-m', 'pip', 'install', 'ghp-import'])


def build():
    print('Build site...')
    res = subprocess.check_call([
        sys.executable,
        '-m',
        'pelican',
        contentPath,
        '-o', outputPath,
        '-s', localConfigPath,
    ])


def serve():
    print('Serve site...')
    res = subprocess.check_call([
        sys.executable,
        '-m',
        'pelican',
        '-l',
        contentPath,
        '-o', outputPath,
        '-s', localConfigPath,
    ])


def preview():
    print('Build site for publising...')
    res = subprocess.check_call([
        sys.executable,
        '-m',
        'pelican',
        contentPath,
        '-o', outputPath,
        '-s', publishConfigPath,
    ])


def publish():
    preview()
    print('Build site for publising...')
    commit_message = "\"Publish site on {}\"".format(
        datetime.date.today().isoformat())
    res = subprocess.check_call([
        sys.executable,
        '-m', commit_message,
        'ghp-import',
        '-n',
        '-c', 'www.riuson.com',
        '-r', 'github',
        outputPath
    ])


scriptCommand = args.command

handlers = {
    'hello': hello,
    'configure': configure,
    'build': build,
    'serve': serve,
    'preview': preview,
    'publish': publish,
}

if scriptCommand == 'prepare':
    prepare()
else:
    if isVirtualEnvironment():
        handler = handlers[scriptCommand]
        handler()
    else:
        passToVirtualEnvironment(scriptCommand)
