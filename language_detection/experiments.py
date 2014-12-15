# -*- coding: utf-8 -*-

import models as mdls
import features as ftrs

# -------------------------------------------------------------------------



# -------------------------------------------------------------------------


def analyze_language(language_id):
    # loading models for the specified language
    lang_models = mdls.load_models_by_language(language_id)

    # loading the test set for the specified language
    test_set = mdls.load_test_set_by_language(language_id, clean_data_set=True)

    k = 0

    # for each model
        # evaluate the test set for that language (compute precision and recall)


# -------------------------------------------------------------------------




# -------------------------------------------------------------------------

# -------------------------------------------------------------------------