#_____GLOBAL IMPORTS_____#
import sys
from light.utils import _AttributeDict


win32 = (sys.platform == 'win32')


def _get_system_username():
    """
    """
    import getpass
    username = None
    try:
        username = getpass.getuser()
        """
        """
    except KeyError:
        pass
    except ImportError:
        if win32:
            import win32api
            import win32security
            import win32profile
            username = win32api.GetUserName()
    return username


def _get_home():
    """
    Get home directory. This will ensure it works
    on all plataforms.
    """
    from os.path import expanduser
    home = expanduser('~')
    return home


env = _AttributeDict({
    'debug': True,
    'log_color': 96,
    'cwd': '',
    'new_cwd': [],
    'command_prefixes': [],
    'passwords': {},
    'local_user': _get_system_username(),
    'user': None,
    'home': _get_home(),
    'git_repo_dotfiles': '',
    'git_repo_project': '',
    'project_base': '',
    'project_home'
    'project_requirements': '',
    })
