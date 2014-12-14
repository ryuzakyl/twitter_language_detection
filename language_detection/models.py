# -*- coding: utf-8 -*-

import os
import json
import codecs

import features
import normalization

# ----------------------------------------------------------------------

# german language code
GERMAN = 0

# english language code
ENGLISH = 1

# spanish language code
SPANISH = 2

# french language code
FRENCH = 3

# italian language code
ITALIAN = 4

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

# simple 2-grams model
MODEL_2_GRAMS = 0

# simple 3-grams model
MODEL_3_GRAMS = 1

# combined 2-grams and 3-grams model
MODEL_2_3_GRAMS = 2

# simple smallwords model
MODEL_SMALLWORDS = 3

# mapper between language code and model name
model_type_to_name_mapper = {
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


def build_models(model_type=MODEL_3_GRAMS):
    # for each language for training
    for lang_id in language_id_to_code_mapper:
        # build the corresponding model
        build_model_for_language(lang_id, model_type)


def build_model_for_language(language_id, model_type):
    # getting the language code from it's id
    language_code = get_language_code(language_id)

    # getting the model name from it's type
    model_name = get_model_name(model_type)

    # getting the training data
    training_data_path = "%s/%s/" % (training_base_path, language_code)
    training_data_handles = get_training_data_handles(training_data_path)

    # computing the model data depending on the selected model type
    model_data = compute_model(training_data_handles, model_type)

    # building the model's full path
    model_path = "%s/%s/%s.txt" % (models_base_path, language_code, model_name)

    # writing the model data to file
    with codecs.open(model_path, 'w') as f:
        f.write(model_data)


def compute_model(training_data_handles, model_type):
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

    :rtype : string
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