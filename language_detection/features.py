# -*- coding: utf-8 -*-


def get_n_grams(text, n):
    """
    Computes the n-grams of a given text

    :rtype : list
    :param text: The text provided
    :param n: The n of n-grams
    :return: List of all the word's n-grams
    """

    # returning the list of n-grams
    return [text[i:i+n] for i in xrange(len(text) - n + 1)]


def get_smallwords(text, min_length=1, max_length=5):
    """
    Computes the smallwords of a given text

    :rtype : list
    :param text: The text provided
    :param min_length: The minimum length of the smallwords
    :param max_length: The maximum length of the smallwords
    :return: The list of all the smallwords
    """

    # returning the list of smallwords
    return [word for word in text.split(' ') if min_length <= len(word) <= max_length]


def probabilistic_similarity(lang_model, query_model):
    """
    Returns the probability (invented by me) of a query text belongs to a language model

    :rtype : float
    :param lang_model: The model of a language (usually a dictionary of features and it's values)
    :param query_model: The query text (usually a dictionary of features and it's values)
    :return: The probability that the given query belongs to the provided language model
    """

    # computing all the features appearances in the language model
    lang_features_total = sum(lang_model.values())

    # computing appearances of query features in the language model
    query_features_total = [lang_model[f] for f in query_model if f in lang_model]

    # returning the normalization (probability that the query belongs to that language)
    return float(query_features_total) / float(lang_features_total)


def out_of_place_similarity(lang_model, query_model, tob_best_features=100):
    """
    Returns the out-of-place similarity of a query text and a language model

    :rtype : int
    :param lang_model: The model of a language (usually a dictionary of features and it's values)
    :param query_model: The query text (usually a dictionary of features and it's values)
    :param tob_best_features: The out-of-place similarity between the query and the model
    """

    # computing the amount of features for analysis
    features_count = min(len(lang_model), len(query_model), tob_best_features)

    # sorting the language model in decreasing order of feature frequencies
    lang_model_sorted = sorted(
        lang_model.iteritems(),                 # dictionary iterator
        key=lambda dict_item: dict_item[1],     # sorting by frequencies
        reverse=True                            # reversing the list
    )[0:features_count]                         # taking the top 'features_count' features

    # sorting the query in decreasing order of feature frequencies
    query_model_sorted = sorted(
        query_model.iteritems(),                # dictionary iterator
        key=lambda dict_item: dict_item[1],     # sorting by frequencies
        reverse=True                            # reversing the list
    )[0:features_count]                         # taking the top 'features_count' features

    # computing distance of the query model to the language model
    similarity = 0
    for i in xrange(features_count):
        # getting the current feature
        feature = query_model_sorted[i]

        # getting the index of the current feature
        idx = get_index_of_feature(lang_model_sorted, feature[0])

        # adding the 'feature_count' if the feature doesn't exists, the index difference if it does
        similarity += features_count if idx == -1 else abs(i - idx)

    # returning the computed similarity
    return similarity


def get_index_of_feature(feature_list, item):
    """
    Gets the index of the feature in the provided feature list

    :rtype : int
    :param feature_list: List of features to search from
    :param item: The feature to search
    :return: The index where the feature was founded, -1 otherwise
    """

    # getting the indexes where 'item' occurs
    idxs = [k for k in xrange(len(feature_list)) if feature_list[k][0] == item]

    # counting the indexes
    idxs_count = len(idxs)

    # if the feature appears more than one time
    if idxs_count > 1:
        raise Exception("""
        There was a problem in the feature extraction process.\r\n
        The feature is counted more than one time.""")

    # the index if any, -1 if the feature doesn't appear
    return idxs[0] if idxs_count == 1 else -1