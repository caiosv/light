"""
    I NEED AN ELSE after: if len(sysArgv) > 1:
    TO RUN ALL METHODS ONCE WITHOUT ARGUMENTS.


    THINK ABOUT MAKE A LIGHT COMMAND-LINE TO SEARCH
    FOR A lightfile.py FILE IN THE DIR OF WORK ENV
    THEN HANDLE THOSE THINGS WE HAVE ALREADY DONE.
"""
import os
import sys
import re
from light.operations import run
from light.colors import log
from lightfile import *


class job_execute(object):
    def __init__(self, sysArgv, methods):
        try:
            log('methods: %s' % methods)
            log('lenght methods: %s' % len(methods))
            self.function = None
            self.args = []
            self.modulePath = sysArgv[0]
            log('Module Path: %s' % self.modulePath)
            self.moduleDir, tail = os.path.split(self.modulePath)
            log('Module Dir: %s' % self.moduleDir)
            self.moduleName, ext = os.path.splitext(tail)
            log('Module Name: %s' % self.moduleName)
            #__import__(self.moduleName)
            #self.module = sys.module.__dict__[self.moduleName]
            if len(sysArgv) > 1:
                self.functionName = sysArgv[1]
                log('Function Name: %s' % self.functionName)
                #self.function = globals()[self.functionName]
                possibles = globals().copy()
                possibles.update(locals())
                self.function = possibles.get(self.functionName)
                if self.function:
                    pass
                else:
                    for method in methods:
                        if self.functionName == method:
                            self.function = methods[self.functionName]
                log('self func: %s' % self.function)
                self.args = sysArgv[2:]
        except Exception, e:
            sys.stderr.write('%s %s\n' % ('job_execute#__init__', e))

    def execute(self):
        try:
            if self.function:
                self.function(*self.args)
        except Exception, e:
            sys.stderr.write('%s %s\n' % ('job_execute#execute', e))


def opp():
    run('ls -la /home/ubuntu/')


"""
I NEED FIND A WAY TO ORDERED MY DIC or LIST
"""


def words(fileobj):
    for line in fileobj:
        for word in line.split():
            yield word


def file_find_word(thisfile):
    searchterms = ['def']
    found_word = {}
    with open(thisfile) as wordfile:
        print wordfile
        wordgen = words(wordfile)
        for word in wordgen:
            if word in searchterms:
                nw = next(wordgen, None)
                nw = re.split('\(.*\):', nw)[0]
                if not nw.startswith('_') and not 'main' in nw:
                    fw_dict = {nw: eval(nw)}
                    found_word.update(fw_dict)
            else:
                word = None
        foundwords = [word, next(wordgen, None)]
        print foundwords
        print 'Found Word dict: %s' % found_word
        return found_word

"""
def main():

    m_dict = file_find_word('/home/ubuntu/confs/light/lightfile.py')

    job_execute(sys.argv, m_dict).execute()
"""
