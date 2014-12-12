# -*- coding: utf-8 -*-

import codecs


with codecs.open('../corpus/fr.txt', 'r') as f:
    lines = f.readlines()

    for i in xrange(100):
        l1 = lines[i][0: len(lines[i]) - 1]
        print l1

        l2 = l1.decode('utf-8')
        print l2

        print

