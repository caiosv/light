from distutils.core import setup
from light.install import _man_pages

VERSION = '0.1.0'

readme = open('README.txt').read()

long_description = """
To find out what's new in this version of Fabric, please see `the changelog
<http://docs.light.org/en/%s/changelog.html>`_.

You can also install the `in-development version
<https://github.com/caiosv/light/tarball/master#egg=light-dev>`_ using
pip, with `pip install fabric==dev`.

----

%s

----

For more information, please see the Light website or execute ``light --help`.
""" % (VERSION, readme)


setup(
    name='Light',
    version=VERSION,
    author='Caio Vianna',
    author_email='caiovianna@gmail.com',
    url='http://pypi.python.org/pypi/Light',
    license='LICENSE.txt',
    description='Light is a simple, Pythonic tool for execution System Administration.',
    long_description=long_description,

    # Package Info
    packages=[
        'light',
        'light.cmds',
        'light.api',
        'light.colors',
        'light.context_managers',
        'light.operations',
        'light.state',
        'light.utils',
        ],

)

_man_pages
