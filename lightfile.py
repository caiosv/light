#!/usr/bin/env python
#_____GLOBAL IMPORTS_____#
import sys
import getopt
#_____LIGHT PACKAGES IMPORTS_____#
from light.api import *
from light.operations import prefix

#_____SET ENVIRONMENT_____#
env.user = 'ubuntu'
env.git_user_name = 'cSv'
env.git_user_email = 'caiovianna@gmail.com'
env.git_repo_dotfiles = 'git://github.com/caiosv/dotfiles.git'

# env project
env.git_repo_project = 'https://github.com/caiosv/atrend_shop.git'
env.project_base = 'atrend'
env.project_home = 'atrend_shop'
env.project_requirements = '%(project_home)s/atrend_requirements.txt' % env

# env database
env.db_root = ''
env.db_root_pass = ''
env.db_user = ''
env.db_user_pass = ''
env.db_pass = ''
env.db_name = ''
# MySQL database commands
env.db_create_user = 'CREATE USER "%(db_user)s"@"localhost" IDENTIFIED BY "%(db_user_pass)s"' % env
env.db_create_database = 'CREATE DATABASE %(db_name)s' % env
env.db_grant_all_privileges = 'GRANT ALL PRIVILEGES ON %(db_name)s.* TO "%(db_user)s"@"localhost"' % env
env.db_flush_privileges = 'FLUSH PRIVILEGES'

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

# VERSION
VERSION = '0.1.0'


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


def _set_up_webservers():
    """
    """
    hr()
    print magenta("Set up Web Servers.")
    hr()
    with cd('%(home)s/%(project_base)s/%(project_home)s/conf/' % env):
        print magenta('Automatic Green Unicorn..')
        sudo('mv atrend_shop_app.conf /etc/init/')  # green unicorn automatic start

        #_____set up nginx_____#
        print magenta("Set Up Nginx..")
        sudo('mkdir -p /opt/%(project_base)s/logs/nginx/' % env)
        sudo('ln -s %(home)s/%(project_base)s/%(project_home)s/static /opt/atrend' % env)  # sys link static
        sudo('mv /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup')
        sudo('mv default /etc/nginx/sites-available/default')
        print magenta('[DONE] Set up Web Servers.')


def _set_up_database():
    """
    Set up database, create user, create database, set privileges.
    """
    print red('Start set up mysql:')
    _mysql_execute(env.db_create_user, env.db_root, env.db_root_pass)
    _mysql_execute(env.db_create_database, env.db_root, env.db_root_pass)
    _mysql_execute(env.db_grant_all_privileges, env.db_root, env.db_root_pass)
    _mysql_execute(env.db_flush_privileges, env.db_root, env.db_root_pass)
    print red('[DONE] set up mysql')


def _mysql_execute(sql, user=None, password=None):
    """
    Executes passed sql command using mysql shell.
    """
    user = user or env.conf.DB_USER

    if user == 'root' and password is None:
        password = _get_root_password()
    elif password is None:
        password = env.conf.DB_PASSWORD
        sql = sql.replace("'", r'\"')

    return run("echo '%s' | mysql --user='%s' --password='%s' " % (sql, user, password))


#_____SET PROJECT_____#
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

            if env.project_requirements is not '':
                pass
            else:
                env.project_requirements = raw_input(red('Please enter the path to your' + \
                                                                red('requirements file', bold=True) + \
                                                                ': '))
            print magenta('Install Requirements..')
            with prefix('. bin/activate'):
                run('pip install -r %(project_requirements)s' % env)

    _set_up_webservers()
    _set_up_database()

    with cd('%(home)s/%(project_base)s/%(project_home)s' % env):
        print magenta('Syncing database..')
        with prefix('. bin/activate'):
            run('python manage.py syncdb')
    hr()
    print magenta('[DONE] PROJECT IS READY.')
    hr()


def update_project():
    """
    Updates the remote project
    """
    with cd('%(home)s/%(project_base)s' % env):
        run('git pull')
        with prefix('. bin/activate'):
            run('pip install -r %(project_requirements)s' % env)
            run('python manage.py syncdb')


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
    with cd('/home/ubuntu/confs/light'), prefix('. bin/activate'):
            run('pip install ipython')


def caio():
    print "HELO MY NEW BABY"


def main():
    from datetime import datetime
    startTime = datetime.now()
    #argv = sys.argv[1:]
    #_job_execute(argv).execute()
    #install_packages()
    #git_global_config()
    #operations()

    from light.main import file_find_word
    m_dict = file_find_word('/home/ubuntu/confs/light/lightfile.py')

    """
    from light.read_methods_file import file_find_word
    m_dict = file_find_word('/home/ubuntu/confs/light/bootstrap.py')
    print blue(m_dict)

    list_keys = list(m_dict.iterkeys())
    for key in list_keys:
        val = m_dict.get(key)
        print yellow(val)
        up_dic = {key: eval(val)}
        m_dict.update(up_dic)
    print red(m_dict)
    """
    #methods = {'git_global_config': git_global_config, 'operations': operations}

    from light.main import job_execute
    job_execute(sys.argv, m_dict).execute()

    print red('It took: ' + str(datetime.now() - startTime), bold=True)

if __name__ == '__main__':
    main()
