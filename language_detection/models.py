# -*- coding: utf-8 -*-

import os
import json
import codecs

import features
import normalization

# ----------------------------------------------------------------------

# german language code
GERMAN = 1

# english language code
ENGLISH = 2

# spanish language code
SPANISH = 4

# french language code
FRENCH = 8

# italian language code
ITALIAN = 16

# language codes for the chosen languages
language_id_to_code_mapper = {
    # german language code
    GERMAN:     'de',

    # english language code
    ENGLISH:    'en',

    # spanish language code
    SPANISH:    'es',

    # french language code
    FRENCH:     'fr',

    # italian language code
    ITALIAN:    'it'
}

# ----------------------------------------------------------------------

# smallwords model of 3rd party
MODEL_3RD_PARTY_3_GRAMS = 1

# simple 2-grams model
MODEL_2_GRAMS = 2

# simple 3-grams model
MODEL_3_GRAMS = 4

# combined 2-grams and 3-grams model
MODEL_2_3_GRAMS = 8

# simple smallwords model
MODEL_SMALLWORDS = 16

# mapper between language code and model name
model_type_to_name_mapper = {
    # smallwords model of 3rd party
    MODEL_3RD_PARTY_3_GRAMS: '3rdparty-3grams',

    # simple 2-grams model
    MODEL_2_GRAMS:      'vmml-2grams',

    # simple 3-grams model
    MODEL_3_GRAMS:      'vmml-3grams',

    # combined 2-grams and 3-grams model
    MODEL_2_3_GRAMS:    'vmml-23grams',

    # simple smallwords model
    MODEL_SMALLWORDS:   'vmml-smallwords'
}

# ----------------------------------------------------------------------

# model generator functions for the available model types
model_generator_mapper = {
    # simple 2-grams model
    MODEL_2_GRAMS: lambda text: features.get_n_grams(text, 2),

    # simple 3-grams model
    MODEL_3_GRAMS: lambda text: features.get_n_grams(text, 3),

    # combined 2-grams and 3-grams model
    MODEL_2_3_GRAMS: lambda text: features.get_n_grams(text, 2) + features.get_n_grams(text, 3),

    # simple smallwords model
    MODEL_SMALLWORDS: lambda text: features.get_smallwords(text)
}

# ----------------------------------------------------------------------

# the base path where the models are stored
models_base_path = './models'

# the base path where the training data is stored
training_base_path = './train'

# ----------------------------------------------------------------------


def build_models_for_each_language(model_type=MODEL_3_GRAMS):
    """
    Builds the models of all supported languages of certain model type

    :rtype : None
    :param model_type: Type of model to build
    """

    # for each language for training
    for lang_id in language_id_to_code_mapper:
        # if the model is defined by me
        if not is_3rd_party_model(model_type):
            # build the corresponding model
            build_model(lang_id, model_type)


def build_model(language_id, model_type):
    """
    Builds a model for a specific language

    :rtype : None
    :param language_id: Language id to build the model for
    :param model_type: Type of model to build
    """

    # getting the language code from it's id
    language_code = get_language_code(language_id)

    # getting the model name from it's type
    model_name = get_model_name(model_type)

    # getting the training data
    training_data_path = "%s/%s/" % (training_base_path, language_code)
    training_data_handles = get_training_data_handles(training_data_path)

    # computing the model data depending on the selected model type
    model_data = compute_model_data(training_data_handles, model_type)

    # building the model's full path
    model_path = "%s/%s/%s.txt" % (models_base_path, language_code, model_name)

    # writing the model data to file
    with codecs.open(model_path, 'w') as f:
        f.write(model_data)


def compute_model_data(training_data_handles, model_type):
    """
    Computes the model data from training samples

    :rtype : str
    :param training_data_handles: Handles to the files containing the model data
    :param model_type: Type of model to build
    :return: The model data as a json string
    """

    # if the selected model type is not supported
    if model_type not in model_generator_mapper:
        raise Exception('Unknown model type provided.')

    # getting the model data generator
    model_data_generator = model_generator_mapper[model_type]

    # trying to compute the model data
    try:
        # structure that will store the model features
        model_features = dict()

        # for each file of training data
        for f in training_data_handles:
            # reading all the file content (decoded in utf8 format)
            file_content = f.read().decode('utf8')

            # cleaning the text
            cleaned_text = normalization.clean_text(file_content)

            # getting the features from that text
            text_features = model_data_generator(cleaned_text)

            # counting frequency of features
            for feat in text_features:
                # incrementing frequency
                if feat in model_features:
                    model_features[feat] += 1

                # adding the feature to the dictionary
                else:
                    model_features[feat] = 1

        # converting and returning the model data as json string format
        return json.dumps(model_features)

    # in case of an exception
    except Exception, e:
        # printing exception message
        print e.message

        raise Exception('Exception thrown in model generation process.')


def get_training_data_handles(training_data_path):
    """
    Gets the valid handles to the all the files in the training data path

    :rtype : list
    :param training_data_path: The folder where all the training data is located
    :return: The handles to the training data files
    """

    # getting the paths of the files in the given directory (assuming all elements are files)
    files_paths = [os.path.join(training_data_path, f_path) for f_path in os.listdir(training_data_path)]

    # creating the file handles
    handles = [open(f_path, 'r') for f_path in files_paths]

    # returning only the valid handles
    return filter(lambda x: x is not None, handles)


def get_language_code(language_id):
    """
    Gets the language code from the associated id

    :rtype : str
    :param language_id: The id of the language
    :return: The language code corresponding to the provided id
    """

    # mapping language id to it's code
    if language_id in language_id_to_code_mapper:
        return language_id_to_code_mapper[language_id]

    raise Exception('Unknown language id received.')


def get_model_name(model_type):
    """
    Gets the model name from the associated type

    :rtype : string
    :param model_type: The type of the model
    :return: The model name corresponding to the provided type
    """

    # mapping model type to it's name
    if model_type in model_type_to_name_mapper:
        return model_type_to_name_mapper[model_type]

    # raising an exception for unknown model type
    raise Exception('Unknown model type received.')


def is_3rd_party_model(model_type):
    """
    Determines if a model type is a 3rdparty model

    :rtype : bool
    :param model_type: The model type to analyze
    :return: True if it is 3rdparty, False otherwise
    """

    # only MODEL_3RD_PARTY_3_GRAMS is a 3rdparty model
    return model_type == MODEL_3RD_PARTY_3_GRAMS

# ----------------------------------------------------------------------


def load_models_by_language(language_id):
    """
    Loads all the models built for a specific language

    :rtype : list
    :param language_id: Language id of the language of interest
    :return: All the models built for a specific language
    """

    # loading all the models of a specific language
    return [load_model(language_id, model_type) for model_type in model_type_to_name_mapper]


def load_models_by_type(model_type):
    """
    Loads all the models of a specific model type

    :rtype : list
    :param model_type: Model type lo load
    :return: All the models of certain type
    """

    # loading the models for each language supported
    return [load_model(lang_id, model_type) for lang_id in language_id_to_code_mapper]


def load_model(language_id, model_type):
    """
    Loads a model of certain language and a specific type

    :rtype : dict
    :param language_id: Language id of the model to load
    :param model_type: Type of the model to load
    :return: The model required
    """

    # getting the language code from it's id
    language_code = get_language_code(language_id)

    # getting the model name from it's type
    model_name = get_model_name(model_type)

    # building the model's full path
    model_full_path = "%s/%s/%s.txt" % (models_base_path, language_code, model_name)

    # returning the model loaded directly from file
    return load_model_from_file(model_full_path)


def load_model_from_file(model_full_path):
    """
    Loads a model from file

    :rtype : dict
    :param model_full_path: Path to the file that holds the model data
    :return: The model information
    """

    # trying to load the model from file
    try:
        # opening the file that has the model data
        with codecs.open(model_full_path, 'r') as f:
            # reading the model data
            model_data = u"%s" % f.read()

            # escaping unicode characters (\u00fb, etc.)
            model_data = model_data.decode('unicode_escape')

            # building the model features
            model_features = eval(model_data)

            # returning the model fatures
            return model_features

    # in case of an exception
    except Exception, e:
        # printing exception message
        print str(e)

        # retuning None
        return None