===========
  Light
===========

Light provides a pythonic framework to help automate system administration jobs.
Just a simple example::
    
    #!/usr/bin/env python

    from light import api
    from light import utils

    def _do_something():
      run('ls /tmp/')
      with cd('/tmp'):
        sudo('mkdir -p somedir/anotherone/')
      
      print red('Job done!', bold=True)

-----------------------------------------------------

    light come with commands line built-in like:
    
    ubuntu@ubuntu:~$ rmif
    File deleted: colors.py~
    File deleted: colors.pyc
    File deleted: context_managers.py~
    File deleted: context_managers.pyc
    
    ubuntu@ubuntu:~$ rmif -p $HOME -a .txt~
    File deleted: README.txt~
    
    * Every command has --help (-h) argument and --version (-v) one too.
    ubuntu@ubuntu:~$ rmif --help


Install
=========

To intsall:

* First of all git clone https://github.com/caiosv/light.git

* Then run python setup.py install

Know more about light
-------------

* Run from console: man light

`visit <http://light.org>`
