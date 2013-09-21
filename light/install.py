#!/usr/bin/env python

# FILE TO PERFORM VITAL INSTALLS,
# TO light WORKS PROPERLY.

import os
import re
from subprocess import Popen, PIPE
from light.colors import hr, red, magenta, yellow
from light.operations import cd, sudo, run


file_path = os.path.dirname(os.path.abspath(__file__))


def _man_pages():
    with cd('%s' % file_path):
        sudo('mkdir -p /usr/man/man1')
        sudo('cp docs/light.1mp /usr/man/man1/')
        sudo('gzip /usr/man/man1/light.1mp')


def _install_commands():
    """
    INSTALL LINUX COMMANDS IN /home/my_user/.bin
    """
    with cd('%s/cmds' % file_path):

        proc = Popen('ls', stdout=PIPE)
        c = proc.communicate()[0]
        commands = re.split('\\n', c)
        for i in commands:
            try:
                commands.remove('')
            except ValueError:
                pass

        if commands:
            run('mkdir ~/.bin')
            for command in commands:
                if '.' in command:
                    c = re.split('\.', command)
                    run('cp %s ~/.bin/%s' % (command, c[0]))
                    run('chmod +x ~/.bin/%s' % c[0])
                    print magenta('Command:' + \
                                        yellow('%s' % c[0], bold=True) + \
                                        magenta('is ready to use, type:') + \
                                        yellow('man %s' % c[0], bold=True) + \
                                        magenta('to see how it works.'))
                else:
                    run('cp {0} ~/.bin/{0}'.format(command))
                    run('chmod +x ~/.bin/%s' % command)
                    print magenta('Command:' + \
                                        yellow('{0}'.format(command), bold=True) + \
                                        magenta('is ready to use, type:') + \
                                        yellow('man {0}'.format(command), bold=True) + \
                                        magenta('to see how it works.'))
        else:
            hr()
            print red('You do not have any command to be install.\n \
                        Please check if there is any command inside of\n \
                        light/cmds/ folder, and if ``commands`` list have those commands.')
            hr()
        #run('cp %s.py ~/.bin/%s' % command)


def main():
    _man_pages()
    _install_commands()


if __name__ == '__main__':
        main()
