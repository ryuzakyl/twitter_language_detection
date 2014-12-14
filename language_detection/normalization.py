# -*- coding: utf-8 -*-

import re

# unwanted characters in a text for language detection
unwanted_chars = u'.,;:¡!¿?1234567890-_+-=()[]<>{}\|/""*@#$%&~' + u"'"


def clean_text(text, cvt_to_lowercase=True, norm_whitespaces=True):
    """
    Cleans a text for language detection by transforming it to lowercase, removing unwanted
    characters and replacing whitespace characters for a simple space.

    :rtype : string
    :param text: Text to clean
    """

    # converting text to lowercase (if required)
    cleaned_text = text.lower() if cvt_to_lowercase else text

    # removing unwanted characters
    cleaned_text = filter(lambda c: c not in unwanted_chars, cleaned_text)

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
    norm_tweet = tweet_text .lower()

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