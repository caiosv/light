from subprocess import call
from light.state import env


def _wrap_with(code):

    def inner(text, bold=False):
        c = code
        clear_bold = '\033[21m'
        if bold:
            c = "1;%s" % c
        return "%s\033[%sm %s \033[0m" % (clear_bold, c, text)
    return inner

red = _wrap_with('91')
magenta = _wrap_with('95')
blue = _wrap_with('34')
cyan = _wrap_with('96')
green = _wrap_with('32')
yellow = _wrap_with('93')
white = _wrap_with('97')
gray = _wrap_with('90')


def log(text, bold=False):
    if env.debug:
        c = env.log_color
        l = '\n[LOG]:'
        clear_bold = '\033[21m'
        if bold:
            c = "1;%s" % c
        print "%s\033[%sm%s %s \033[0m" % (clear_bold, c, l, text)
    else:
        pass


def _wrap_hr(code):

    def hr_inner(symbol='~', width=40):
        for i in range(1, width):
            color = '\033[%s;5m' % code
            call(['echo', '-en', '' +
                        color + '' + symbol + '\e[0m'])
        call('echo')
    return hr_inner

hr = _wrap_hr('34')
hr_red = _wrap_hr('91')
hr_magenta = _wrap_hr('95')
hr_blue = _wrap_hr('34')
hr_cyan = _wrap_hr('96')
hr_green = _wrap_hr('32')
hr_yellow = _wrap_hr('93')
hr_white = _wrap_hr('97')
hr_gray = _wrap_hr('90')
