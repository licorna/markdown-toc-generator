#!/usr/bin/env python
'''Generates a Tablo of Contents for a Github Markdown Document'''


import re
import sys


def is_header(line):
    'Returns header level, depending on amount of # at the start of line'
    match = re.match(r'^(#+)\s(.*)', line)
    if match:
        return len(match.group(1)), match.group(2)

    return 0, ''

def name_for_header(line):
    'Returns what I assume is the label of the a element used by Github'
    return line.lower().replace(' ', '-')

def generate_toc(lines):
    'Returns a TOC from lines.'
    toc = []
    check_skippable = skippable_section()
    for line in lines:
        if check_skippable(line):
            continue
        level, title = is_header(line)
        if level:
            toc.append((level, title, name_for_header(title)))

    return toc

def create_link(name, slug):
    'Returns markup equivalent to in-page link'
    return '[%s](#%s)' % (name, slug)

def tab(level):
    'Returns a markdown bullet with proper spaces for tabulation'
    return '  ' * (level - 1)

def toc_line(element):
    'Returns a tabulated TOC line string ready for output.'
    level, name, slug = range(3)
    return tab(element[level]) + '* ' + create_link(element[name],
                                                    element[slug])

def skippable_section():
    "Returns if inside a block section (```) to avoid grabbing #'s from code."
    def inner(line):
        'Closure, will switch inside_skippable_section flag.'
        if re.match('^```.*', line):
            # pylint: disable=used-before-assignment
            inner.inside_skippable_section = not inner.inside_skippable_section
            # pylint: enable=used-before-assignment
        return inner.inside_skippable_section

    inner.inside_skippable_section = False
    return inner

def write_toc(toc):
    'Writes one line of the TOC.'
    for element in toc:
        print toc_line(element)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage:', __file__, '<mdfile>'
        sys.exit(1)

    with open(sys.argv[1], 'r') as fd:
        write_toc(generate_toc(fd.readlines()))
