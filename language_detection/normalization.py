# -*- coding: utf-8 -*-

import re

# ------------------------------------------------------------------------------

# method to clean a standard text
CLEAN_STANDARD_TEXT = 1

# method to clean a tweet
CLEAN_TWEET = 2

# cleans nothing
NO_CLEAN = 4

# functions for the available cleaning text methods
clean_text_method_mapper = {
    # method to clean a standard text
    CLEAN_STANDARD_TEXT: lambda text: clean_text(text),

    # method to clean a tweet
    CLEAN_TWEET: lambda text: clean_tweet(text),

    # cleans nothing
    NO_CLEAN: lambda text: text
}

# ------------------------------------------------------------------------------

# unwanted characters in a text for language detection
unwanted_chars = u'.,;:¡!¿?1234567890-_+-=()[]<>{}\|/""*@#$%&~' + u"'"


def clean_text(text, cvt_to_lowercase=True, norm_whitespaces=True):
    """
    Cleans a text for language detection by transforming it to lowercase, removing unwanted
    characters and replacing whitespace characters for a simple space.

    :rtype : string
    
    :param text: Text to clean
    :param cvt_to_lowercase: Convert text to lowercase
    :param norm_whitespaces: Normalize whitespaces
    """

    # converting text to lowercase (if required)
    cleaned_text = text.lower() if cvt_to_lowercase else text

    # removing unwanted characters
    cleaned_text = ''.join([
        c for c in cleaned_text
        if c not in unwanted_chars
    ])

    # normalizing whitespaces
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text) if norm_whitespaces else cleaned_text

    # returning the cleaned text
    return cleaned_text


def clean_tweet(tweet_text):
    """
    Cleans a tweet for language detection

    :rtype : str
    :param tweet_text: Tweet of interest
    :return: The cleaned or normalized tweet
    """

    # converting tweet to lowercase
    norm_tweet = tweet_text.lower()

    # removing links to urls, usernames (@name) and hashtags (#name)
    norm_tweet = re.sub(r'(@|#|https?://)[^ ]+', '', norm_tweet)

    # removing laughter
    norm_tweet = re.sub(r'(([hj])+([aieo])+)+[ hj]', r' ', norm_tweet)

    # removing the famous rt characters
    norm_tweet = re.sub(r'(^| )(rt[ :]+)*', ' ', norm_tweet)

    # removing the classic emoticons
    norm_tweet = re.sub(r'(^| )?[:;x]-?[\(\)dop]', '', norm_tweet)

    # naive solution to eliminate html characters like (&gt;, &amp;, &quote;, etc.)
    norm_tweet = re.sub(r'&[a-z]+;', ' ', norm_tweet)

    # changing all the whitespace characters for a single one
    norm_tweet = re.sub(r'\s+', ' ', norm_tweet)

    # finally applying classic text cleaning
    norm_tweet = clean_text(norm_tweet, cvt_to_lowercase=False, norm_whitespaces=False)

    # removing possible starting and tailing whitespace
    norm_tweet = re.sub(r'(^\s+|\s+$)', '', norm_tweet)

    # returning the normalized tweet
    return norm_tweet


def insert_pad(text, pad_left=True, pad_right=True, pad_symbol=' '):
    """
    Inserts pads to the given text (at the start and at the end)

    :rtype : string
    :param text: Text to insert pads to
    :param pad_left: Whether to insert or not a pad to the left
    :param pad_right: Whether to insert or not a pad to the left
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


def clean_data_set(data_set, clean_method=CLEAN_TWEET):
    """
    Cleans certain data set making a difference if data are tweets or not

    :rtype : list
    :param data_set: The data set of interest
    :param clean_method: Type of method to clean text
    :return: The cleaned (normalized) data set
    """

    # validating the clean method
    if clean_method not in clean_text_method_mapper:
        raise Exception('Unknown clean method received.')

    # getting the text cleaner method
    text_cleaner = clean_text_method_mapper[clean_method]

    # returning the cleaned data set
    return [(lang_code, text_cleaner(text)) for lang_code, text in data_set]
