#!/usr/bin/env python
import sys
COLORS = (
    'BLACK', 'RED', 'GREEN', 'YELLOW',
    'BLUE', 'MAGENTA', 'CYAN', 'WHITE'
)

def color_text(text, color_name, bold=False):
    if color_name in COLORS:
        return '\033[{0};{1}m{2}\033[0m'.format(
            int(bold), COLORS.index(color_name) + 30, text)
    sys.stderr.write('ERROR: "{0}" is not a valid color.\n'.format(color_name))
    sys.stderr.write('VALID COLORS: {0}.\n'.format(', '.join(COLORS)))

# TESTS
if __name__ == '__main__':
    for bold in (False, True):
        for color_name in COLORS:
            print color_text('Example of {0}'.format(color_name), color_name, bold)
    print
    # test error handling
    color_text('TEST', 'SILVER')

