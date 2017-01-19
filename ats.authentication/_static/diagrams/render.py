#!/usr/bin/env python

# https://market.mashape.com/smhanov/websequencediagrams

import glob
import os.path
import re

try:
    from urllib.request import urlopen, urlretrieve
except ImportError:
    from urllib import urlopen, urlretrieve

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


def create_diagram(text, output, style='default'):
    request = {
        'message': text,
        'style': style,
        'apiVersion': '1',
    }

    f = urlopen('http://www.websequencediagrams.com/',
                urlencode(request).encode('utf8'))

    line = f.readline().decode('utf8')

    f.close()

    expr = re.compile('(\?(img|pdf|png|svg)=[a-zA-Z0-9]+)')
    m = expr.search(line)

    if m is None:
        print('Cannot create %s, invalid response from server.' % output)
        return

    urlretrieve('http://www.websequencediagrams.com/' + m.group(0), output)


def main():
    for filename in glob.glob('*.txt'):
        output = os.path.join('png', os.path.splitext(filename)[0] + '.png')
        print('%s...' % filename)

        with open(filename) as fin:
            text = fin.read()
        create_diagram(text, output, style='qsd')


if __name__ == "__main__":
    main()
