# -*- coding: utf-8 -*-

from . import models as mod
from . import features as feat
from . import normalization as norm

# -------------------------------------------------------------------------


def test_language_detector(model_type=mod.MODEL_3_GRAMS, distance=feat.DIST_PROB_NORM):
    # loading models of specific type
    lang_models = mod.load_models_by_type(model_type)

    # loading the test set for the specified language
    test_set = mod.load_test_set_for_all_languages(clean_method=norm.NO_CLEAN)

    # variables for 'precision' and 'recall'
    samples_per_class = 50
    right = {
        mod.GERMAN: 0,
        mod.ENGLISH: 0,
        mod.SPANISH: 0,
        mod.FRENCH: 0,
        mod.ITALIAN: 0
    }
    wrong = {
        mod.GERMAN: 0,
        mod.ENGLISH: 0,
        mod.SPANISH: 0,
        mod.FRENCH: 0,
        mod.ITALIAN: 0
    }

    # for each tweet
    for q_text_class, q_text in test_set:
        # compute the representation for the query text
        query_model = mod.compute_model_for_text(q_text, model_type, norm.CLEAN_TWEET)

        # computing the text class
        q_text_class_key = feat.categorize_text(lang_models, query_model, distance)

        # registering the classification result
        if q_text_class_key == q_text_class:
            right[q_text_class_key] += 1
        else:
            wrong[q_text_class_key] += 1

    # computing total precision
    precision_classes_data = [(right[k], right[k] + wrong[k]) for k in right]
    precision_total = feat.precision_set_of_classes(precision_classes_data)

    # computing total recall
    recall_classes_data = [(right[k], samples_per_class) for k in right]
    recall_total = feat.recall_set_of_classes(recall_classes_data)

    # returning the precision and the recall
    return precision_total, recall_total
