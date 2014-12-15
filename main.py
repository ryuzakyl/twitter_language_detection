# -*- coding: utf-8 -*-

from language_detection import models
from language_detection import experiments as tests

tests.analyze_language(models.SPANISH)

# for l_id in models.language_id_to_code_mapper:
#     print models.language_id_to_code_mapper[l_id]
#
#     l = models.load_models_by_language(l_id)
#     for d in l:
#         print d
#
#     k = 0

# -----------------------------------------------------------------

# import codecs
#
# with codecs.open('./en.txt', 'r') as f:
#     lines = f.readlines()
#
#     data = lines[0]
#     data = data.decode('unicode_escape')
#
#     d = eval(data)
#
#     for key in d:
#         print "%s\t%i" % (key, d[key])
#
#     # ------------------------------------------------
#     #
#     # for i in xrange(100):
#     #     l1 = lines[i][0: len(lines[i]) - 1]
#     #     print l1
#     #
#     #     l2 = l1.decode('utf-8')
#     #     print l2
#     #
#     #     print