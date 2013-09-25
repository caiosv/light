#_____BUILT-IN IMPORTS_____#
import os
from subprocess import call
from contextlib import contextmanager

#_____LIGHT IMPORTS_____#
from light.utils import indent
from light.colors import red, white, green, blue, gray, hr
from light.state import env


class _AttributeSting(str):
    """
    Simple string subclass to allow arbitrary attribute acess.
    """
    @property
    def stdout(self):
        return str(self)


def _run_command(command, shell=True, sudo=False):
    """
    Underpinnings of `run` and `sudo`. See their docstrings for more info.
    """
    if command:

        if env.command_prefixes:
            cmd_prefix = _AttributeSting(env.command_prefixes[0])
            command = cmd_prefix + command

        given_command = _AttributeSting(command)

        which = 'sudo' if sudo else 'run'

        if which == 'run':
            print(gray('Perfoming given command: ' + \
                blue(given_command, bold=True)))

            try:
                call(given_command, shell=shell)
            except Exception, e:
                hr()
                print(red('Command falied for the following reason:', bold=True))
                print(white(indent(e.message) + '\n', bold=True))
                hr()
        elif which == 'sudo':
            print(gray('Perfoming given command:' + \
                    blue('sudo ' + command, bold=True)))
            try:
                call('sudo %s' % given_command, shell=shell)
            except Exception, e:
                hr()
                print(red('Command failed for the following reason:', bold=True))
                print(white(indent(e.message) + '\n', bold=True))
                hr()
    elif not command:
        which = 'sudo' if sudo else 'run'
        hr()
        print(red('Unable to perfom command action for the following reason:', bold=True))
        print(white('No command was not written correct. Please se the doc of' + green(which, bold=True) + 'command.\n'))
        hr()


def run(command, shell=True):
    """
    Run a shell command.

    If ``shell`` is True (the default), `run` will execute the given command
    string via a shell interpreter.

    Exaples::

        run('ls /home/myuser/')
        run(')s /home/myuser/', shell=False)
        output = run('ls /home/myuser/')
        run('ls /home/myuser/', timeout=5)
    """
    return _run_command(command, shell)


def sudo(command, shell=True):
    """
    Run a shell command as sudo.

    If ``shell`` is True (the default), `sudo` will execute the given command
    string via a shell interpreter as sudo.

    Exaples::

        sudo('apt-get update')
        sudo('apt-get install mypackages')
        output = sudo('ls /tmp/')
        sudo('whoami')
    """
    return _run_command(command, shell, sudo=True)

# GLOBAL LIST OF NEW PATH TO CD
#new_cwd = []


@contextmanager
def cd(path):
    path = path.replace(' ', '\ ')
    old_dir = os.getcwd()

    if env.cwd:
        hold_path = ''
        for p in env.new_cwd:
            hold_path += p

        print(gray('Walking to: ' + \
                blue(hold_path + path, bold=True)))
        os.chdir(hold_path + path)
        env.new_cwd.append(path)
    else:
        print(gray('Walking to: ' + \
                blue(path, bold=True)))
        os.chdir(path)
        env.new_cwd.append(os.getcwd())
        env.cwd += str(env.new_cwd)
    try:
        yield
    finally:
        os.chdir(old_dir)
    env.cwd = ''  # clean env.cwd
    env.new_cwd = []  # clean env.new_cwd


@contextmanager
def prefix(command, shell=True):
    given_command = _AttributeSting(command)
    given_command = given_command + ' && '

    if not env.command_prefixes:
        env.command_prefixes.append(given_command)
    else:
        env.command_prefixes = []
        env.command_prefixes.append(given_command)
    try:
        yield
    finally:
        pass
