from setuptools import setup, find_packages
from light.install import _man_pages, _install_commands

VERSION = '0.1.0'

readme = open('README.md').read()

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
    packages=find_packages(),
    entry_points={
            'light': [
                'light = light.main:main',
            ]
    },



    classifiers=[
        'Development Status :: 5 - Production/Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Clustering',
        'Topic :: System :: Software Distribution',
        'Topic :: System :: Systems Administration',
    ],

)

_man_pages()
_install_commands()
