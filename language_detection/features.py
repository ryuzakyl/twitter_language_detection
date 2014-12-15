# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------

# simple probability distance
DISTANCE_PROBABILITY = 1

# simple normalized probability distance
DISTANCE_PROBABILITY_NORMALIZED = 2

# simple out of place distance
DISTANCE_OUT_OF_PLACE = 4

# distance between model and query mapper
distance_mapper = {
    # simple probability distance
    DISTANCE_PROBABILITY: lambda m, q: probabilistic_similarity(m, q),

    # simple normalized probability distance
    DISTANCE_PROBABILITY_NORMALIZED: lambda m, q: normalized_probabilistic_similarity(m, q),

    # simple out of place distance
    DISTANCE_OUT_OF_PLACE: lambda m, q: out_of_place_similarity(m, q)
}

# -------------------------------------------------------------------------


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

# -------------------------------------------------------------------------


def probabilistic_similarity(lang_model, query_model):
    """
    Returns the probability (invented by me) of a query text belongs to a language model

    :rtype : float
    :param lang_model: The model of a language (usually a dictionary of features and it's values)
    :param query_model: The query text (usually a dictionary of features and it's values)
    :return: The probability that the given query belongs to the provided language model
    """

    # computing all the features appearances in the language model
    lang_features_total = float(sum(lang_model.values()))

    # computing appearances of query features in the language model
    query_features_total = float(sum([lang_model[f] for f in query_model if f in lang_model]))

    # returning the normalization (probability that the query belongs to that language)
    return query_features_total / lang_features_total


def normalized_probabilistic_similarity(lang_model, query_model):
    """
    Returns the 'normalized probability' (invented by me) of a query text belongs to a language model

    :rtype : float
    :param lang_model: The model of a language (usually a dictionary of features and it's values)
    :param query_model: The query text (usually a dictionary of features and it's values)
    :return: The normalized probability that the given query belongs to the provided language model
    """

    # computing total of the features appearances in the language model
    lang_total = float(sum(lang_model.values()))

    # computing total of the features appearances in the query
    query_total = float(sum(query_model.values()))

    # lambda function to compute distance
    d = lambda x: 1.0 if x not in lang_model else abs(query_model[x] / query_total - lang_model[x] / lang_total)

    # computing the total distance of the query to the model
    query_total_distance = float(sum([d(f) for f in query_model]))

    # returning the normalized probability
    return 1.0 - query_total_distance / len(query_model)


def out_of_place_similarity(lang_model, query_model):
    """
    Returns the out-of-place similarity of a query text and a language model

    :rtype : int
    :param lang_model: The model of a language (usually a dictionary of features and it's values)
    :param query_model: The query text (usually a dictionary of features and it's values)
    """

    # computing the amount of features for analysis
    features_count = min(len(lang_model), len(query_model))

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
    similarity = 0.0
    for i in xrange(features_count):
        # getting the current feature
        feature = query_model_sorted[i]

        # getting the index of the current feature
        idx = get_index_of_feature(lang_model_sorted, feature[0])

        # adding the 'feature_count' if the feature doesn't exists, the index difference if it does
        similarity += features_count if idx == -1 else abs(i - idx)

    # returning the computed similarity (normalized in [0, 1])
    return similarity / features_count


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

# ------------------------------------------------------------------------------


def categorize_text(category_models, query_model, distance=DISTANCE_PROBABILITY):
    """
    Assigns a category among some category models to the given query model

    :rtype : object
    :param category_models: The category models to take into account
    :param query_model: The query model of interest
    :param distance: The type of distance to employ
    :return: The assigned category (most likely)
    """

    # computing the pertinence probabilities
    pertinence_probabilities = compute_pertinence_probabilities(category_models, query_model, distance)

    # returning the category with the highest probability of pertinence
    return get_most_likely_category(pertinence_probabilities)


def compute_pertinence_probabilities(category_models, query_model, distance=DISTANCE_PROBABILITY):
    """
    Computes the pertinence probabilities of the query model to each of the provided category models

    :rtype : list
    :param category_models: The provided category models
    :param query_model: The query model of interest
    :param distance: The distance to employ
    :return: The list of pertinence probabilities to each category model
    """

    # raising exception if distance not in mapper
    if distance not in distance_mapper:
        raise Exception('Unknown distance received.')

    # getting the proper distance method
    d = distance_mapper[distance]

    # returning the probability (for each model) that the query belongs to the model
    return [(model_key, d(lang_model, query_model)) for model_key, lang_model in category_models]


def get_most_likely_category(pertinence_probabilities, use_similarity_concept=True):
    """
    Gets the most likely category among the provided pertinence probabilities per model

    :rtype : object
    :param pertinence_probabilities: The pertinence probabilities per model
    :return: The most likely category
    """

    # sorting by model pertinence
    sorted_by_pertinence = sorted(pertinence_probabilities, key=lambda t: t[1], reverse=use_similarity_concept)

    # returning the model key for the model with highest probability of pertinence
    return sorted_by_pertinence[0][0]

# ------------------------------------------------------------------------------


def precision_single_class(correctly_assigned, total_assigned):
    """
    Computes the precision for a single class

    :rtype : float
    :param correctly_assigned: Samples correctly assigned to the class
    :param total_assigned: Total samples assigned to the class
    :return: The precision value
    """

    # simply returning the precision value
    return float(correctly_assigned) / float(total_assigned)


def precision_set_of_classes(classes_data):
    """
    Computes the precision for a set of classes

    :rtype : float
    :param classes_data: Data associated for the classes
    :return: The precision value
    """

    # getting the total number of classes
    n = float(len(classes_data))

    # returning the precision for the set of classes
    return sum([precision_single_class(ca, ta) for ca, ta in classes_data]) / n


def recall_single_class(correctly_assigned, total_belonging):
    """
    Computes the recall for a single class

    :rtype : float
    :param correctly_assigned: Samples correctly assigned to the class
    :param total_belonging: Total samples assigned to the class
    :return: The recall value
    """

    # simply returning the recall value
    return float(correctly_assigned) / float(total_belonging)


def recall_set_of_classes(classes_data):
    """
    Computes the recall for a set of classes

    :rtype : float
    :param classes_data: Data associated for the classes
    :return: The recall value
    """

    # getting the total number of classes
    n = float(len(classes_data))

    # returning the recall for the set of classes
    return sum([recall_single_class(ca, tb) for ca, tb in classes_data]) / n