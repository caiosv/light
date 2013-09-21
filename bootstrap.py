#!/usr/bin/env python
#_____GLOBAL IMPORTS_____#

#_____LIGHT PACKAGES IMPORTS_____#
from light.api import *

#_____SET ENVIRONMENT_____#
env.user = 'ubuntu'
env.git_user_name = 'cSv'
env.git_user_email = 'caiovianna@gmail.com'
#env.git_repo_dotfiles = 'git://github.com/caiosv/dotfiles.git'


INSTALL_PACKAGES = [
        "vim",
        "python-setuptools",
        "python-dev",
        "git-man",
        "nginx",
        "nginx-full",
        "git",
        "git-man",
        "nginx",
        "nginx-full",
        "mysql-server",
        "python-mysqldb",
        "mysql-common",
        "mysql-client",
        "libmysqlclient-dev"
        ]


def install_packages():
    package_count = len(INSTALL_PACKAGES)
    hr()
    print (magenta("INSTALL %s PACKAGES:" % package_count, bold=True))
    for package in INSTALL_PACKAGES:
        print (cyan(package))
    hr()

    sudo('apt-get update')
    print (magenta("SYSTEM IS UP TO DATE NOW.", bold=True))
    package_str = " ".join(INSTALL_PACKAGES)
    sudo('apt-get -y install ' + package_str)
    sudo('easy_install pip')
    sudo('pip install --upgrade')
    sudo('pip install virtualenv')

    hr()
    print (magenta(" [DONE] PACKAGES INSTALLED!"))
    hr()


def git_global_config():
    """
    Set alias for git commands, color for present git
    in terminal and username and email.
    """
    hr()
    print magenta('SET UP GIT GLOBAL CONFIG...')
    hr()

    run('git config --global alias.st status')
    run('git config --global alias.cmt commit')
    run('git config --global alias.br branch')
    run('git config --global alias.cout checkout')
    run('git config --global color.ui true')
    run('git config --global user.name %(git_user_name)s' % env)
    run('git config --global user.email %(git_user_email)s' % env)

    hr()
    print (magenta('[DONE] GIT GLOBAL CONFIG IS SET UP!'))
    hr()


def clone_dotfiles():
    """
    Clone my dotfiles and set it up.
    """
    GIT_REPO_DOTFILES = ''

    if env.git_repo_dotfiles is not '':
        GIT_REPO_DOTFILES = '%(git_repo_dotfiles)s' % env
    else:
        hr(symbol='+', width=80)
        entry = raw_input(red('Please enter the repository to your dotfiles: '))
        GIT_REPO_DOTFILES = entry
    hr(width=80)
    print magenta('Clone dotfiles from --> %s' % GIT_REPO_DOTFILES)
    hr(width=80)

    with cd('%(home)s' % env):
        run('git clone %s' % GIT_REPO_DOTFILES)

    print magenta('MAKE SYS LINK TO .vim and .vimrc' % env)
    run('ln -s %(home)s/dotfiles/vim %(home)s/.vim' % env)
    run('ln -s %(home)s/dotfiles/vimrc %(home)s/.vimrc' % env)

    print magenta('INIT GIT SUBMODULE AND UPDATE IT')
    with cd('%(home)s/dotfiles' % env):
        run('git submodule init && git submodule update')

#_____SET UP VIM PLUGIN COMMAND-T_____#
if env.git_repo_dotfiles is not "git://github.com/caiosv/dotfiles.git":
    pass
else:
    print magenta('SET UP VIM PLUGIN COMMAND-T..')
    sudo('apt-get install ruby1.8-dev')
    with cd('%(home)s/dotfiles/vim/bundle/command-t/ruby/command-t' % env):
        run('ruby extconf.rb')
        run('make')

    print magenta('[DONE] VIM PLUGIN COMMAND-T IS READY.')


def start_project():
    """
    CLONE PROJECT FROM REPOSITORY AND THEN
    SET UP ENVIRONMENT FOR PROJECT.'))
    """
    hr()
    print magenta('START PROJECT')
    hr()
    with cd('%(home)s' % env):
        if env.base_project is not '':
            pass
        else:
            env.base_project = raw_input(red('Please enter the path to set your project\n \
                                                to prepare a virtualenv environment and\n \
                                                clone your project. Assume the path starts\n \
                                                at ' + yellow('%(home)s/' % env, bold=True)))
        run('virtualenv %(project_base)s' % env)
        with cd('%(project_base)s' % env):
            if env.git_repo_project is not '':
                pass
            else:
                env.git_repo_project = raw_input(red('Please enter the repository to your project: '))

            print magenta('Git clone repository from:' + \
                            yellow('%(git_repo_project)s' + '\nto:' + \
                            '%(home)s/%(project_base)s' % env, bold=True))

            run('git clone %(git_repo_project)s' % env)

            with prefix('source bin/activate'):
                if env.project_requirements is not '':
                    pass
                else:
                    env.project_requirements = raw_input(red('Please enter the path to your' + \
                                                                red('requirements file', bold=True) + \
                                                                ': '))
                print magenta('Install Requirements..')
                run('pip install -r %(project_requirements)s' % env)

    _set_up_webservers()
    _set_up_database()

    with cd('%(home)s/%(project_base)s' % env):
        with prefix('source bin/activate'):
            print magenta('Syncing database..')
            with cd('%(project_home)s' % env):
                run('python manage.py syncdb')
    hr()
    print magenta('[DONE] PROJECT IS READY.')
    hr()


def restart_webservers():
    """
    RESTART BOTH WEBSERVERS NGINX AND GREEN UNICORN.
    """
    hr()
    print magenta('Restart Web Servers')
    hr()
    print magenta('Restart Green Unicorn..')
    sudo('stop atrend_shop_app; start atrend_shop_app')
    print magenta('Restart Nginx..')
    sudo('service nginx restart')
    hr()
    print magenta('[DONE] Web Servers is up.')


def operations():
    hr()
    print (red("TEST OPERATIONS", bold=True))
    hr()
    print (magenta('Local system user: %(local_user)s' % env))
    with cd('/home'):
        run('pwd')
        run('ls -la')
        with cd('/ubuntu'):
            run('pwd')
            run('ls -la')
            with cd('/confs'):
                run('pwd')
                run('ls -la')
                with cd('/light'):
                    run('pwd')
                    run('ls -la')
    run('virtualenv /home/ubuntu/crappy')
    with cd('/home/ubuntu/crappy'):
        run('pwd')
        with prefix('source bin/activate'):
            run('ls -la')
    print red('%(home)s' % env)


def main():
    from datetime import datetime
    startTime = datetime.now()
    #install_packages()
    #git_global_config()
    operations()
    print (datetime.now() - startTime)

if __name__ == '__main__':
    main()
