from contextlib import contextmanager
from light.colors import log, blue, gray
from light import state


def documented_contextmanager(func):
    wrapper = contextmanager(func)
    wrapper.undecorated = func
    return wrapper


@documented_contextmanager
def _setenv(variables):

    log('env: \n %s' % state.env)

    if callable(variables):
        variables = variables()
    clean_revert = variables.pop('clean_revert', False)
    previous = {}
    new = []
    for key, value in variables.iteritems():
        if key in state.env:
            previous[key] = state.env[key]
        else:
            new.append(key)
        state.env[key] = value
    try:
        yield
    finally:
        if clean_revert:
            for key, value in variables.iteritems():
                if key in state.env and value == state.env[key]:
                    if key in previous:
                        state.env[key] = previous[key]
                    else:
                        del state.env[key]
        else:
            log('env: \n %s' % state.env)
            state.env.update(previous)
            log('env: \n %s' % state.env)
            for key in new:
                del state.env[key]

            value = str(value)
            value = value.replace("['", '')
            value = value.replace("']", '')
            print(gray('Perfoming given command:' + \
                    blue(value, bold=True)))


def prefix(command):

    return _setenv(lambda: {'command_prefixes':
                                state.env.command_prefixes + [command]})
