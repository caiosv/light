from distutils.core import setup
from light.install import _man_pages, _install_commands

VERSION = '0.1.0'

readme = open('README.txt').read()

long_description = """
To find out what's new in this version of Light, please see `the changelog
<http://docs.light.org/en/%s/changelog.html>`_.

----

%s

----

For more information, please see the Light website or execute ``man light`.
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
        'light.api',
        'light.colors',
        'light.context_managers',
        'light.operations',
        'light.state',
        'light.utils',
        ],

)

_man_pages()
_install_commands()
