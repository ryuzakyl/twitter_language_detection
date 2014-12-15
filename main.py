# -*- coding: utf-8 -*-

from language_detection import models as mod
from language_detection import features as feat
from language_detection import experiments as tests

print "-------------------------------------------------------------------------------"

print 'Model (2-grams-vmml):'
print 'Precision:\t\t\t\t\tRecall:'
p, r = tests.test_language_detector(model_type=mod.MODEL_2_GRAMS, distance=feat.DIST_PROB_NORM)
print "%.2f\t\t\t\t\t\t%.2f\t(Normalized Probability Similarity)" % (p, r)
p, r = tests.test_language_detector(model_type=mod.MODEL_2_GRAMS, distance=feat.DIST_PROB)
print "%.2f\t\t\t\t\t\t%.2f\t(Simple Probability Similarity)" % (p, r)

print "-------------------------------------------------------------------------------"

print 'Model (3-grams-vmml):'
print 'Precision:\t\t\t\t\tRecall:'
p, r = tests.test_language_detector(model_type=mod.MODEL_3_GRAMS, distance=feat.DIST_PROB_NORM)
print "%.2f\t\t\t\t\t\t%.2f\t(Normalized Probability Similarity)" % (p, r)
p, r = tests.test_language_detector(model_type=mod.MODEL_3_GRAMS, distance=feat.DIST_PROB)
print "%.2f\t\t\t\t\t\t%.2f\t(Simple Probability Similarity)" % (p, r)

print "-------------------------------------------------------------------------------"

print 'Model (3-grams-3rdparty):'
print 'Precision:\t\t\t\t\tRecall:'
p, r = tests.test_language_detector(model_type=mod.MODEL_3RD_PARTY_3_GRAMS, distance=feat.DIST_PROB_NORM)
print "%.2f\t\t\t\t\t\t%.2f\t(Normalized Probability Similarity)" % (p, r)
p, r = tests.test_language_detector(model_type=mod.MODEL_3RD_PARTY_3_GRAMS, distance=feat.DIST_PROB)
print "%.2f\t\t\t\t\t\t%.2f\t(Simple Probability Similarity)" % (p, r)

print "-------------------------------------------------------------------------------"

print 'Model (2-3-grams-vmml):'
print 'Precision:\t\t\t\t\tRecall:'
p, r = tests.test_language_detector(model_type=mod.MODEL_2_3_GRAMS, distance=feat.DIST_PROB_NORM)
print "%.2f\t\t\t\t\t\t%.2f\t(Normalized Probability Similarity)" % (p, r)
p, r = tests.test_language_detector(model_type=mod.MODEL_2_3_GRAMS, distance=feat.DIST_PROB)
print "%.2f\t\t\t\t\t\t%.2f\t(Simple Probability Similarity)" % (p, r)

print "-------------------------------------------------------------------------------"

print 'Model (smallwords-vmml):'
print 'Precision:\t\t\t\t\tRecall:'
p, r = tests.test_language_detector(model_type=mod.MODEL_SMALLWORDS, distance=feat.DIST_PROB_NORM)
print "%.2f\t\t\t\t\t\t%.2f\t(Normalized Probability Similarity)" % (p, r)
p, r = tests.test_language_detector(model_type=mod.MODEL_SMALLWORDS, distance=feat.DIST_PROB)
print "%.2f\t\t\t\t\t\t%.2f\t(Simple Probability Similarity)" % (p, r)

print "-------------------------------------------------------------------------------"