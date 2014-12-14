# -*- coding: utf-8 -*-

import re

# unwanted characters in a text for language detection
unwanted_chars = u'.,;:¡!¿?1234567890-_+-=()[]<>{}\|/""*@#$%&~' + u"'"


def clean_text(text):
    """
    Cleans a text for language detection by transforming it to lowercase, removing unwanted
    characters and replacing whitespace characters for a simple space.

    :rtype : string
    :param text: Text to clean
    """

    # converting text to lowercase
    lowercase_text = text[0:].lower()

    # removing unwanted characters
    text_without_unwanted_chars = filter(lambda c: c not in unwanted_chars, lowercase_text)

    # normalizing whitespaces
    cleaned_text = re.sub(r'\s+', ' ', text_without_unwanted_chars)

    # returning the cleaned text
    return cleaned_text


def clean_tweet(tweet_text):
    pass


def insert_pad(text, pad_left=True, pad_right=True, pad_symbol=' '):
    """
    Inserts pads to the given text (at the start and at the end)

    :rtype : string
    :param text: Text to insert pads to
    :param pad_left: Wether to insert or not a pad to the left
    :param pad_right: Wether to insert or not a pad to the left
    :param pad_symbol: The symbol to insert as pad
    :return: The text with the corresponding pads

    """

    # validating 'pad_symbol'
    if pad_symbol is None or len(pad_symbol) != 1:
        raise Exception('The pad symbol must be a single character')

    # computing pad_left text
    pad_left_str = pad_symbol if pad_left else ''

    # computing pad_right text
    pad_right_str = pad_symbol if pad_right else ''

    # returning the string with pads
    return "%s%s%s" % (pad_left_str, text, pad_right_str)