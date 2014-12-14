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

# ------------------------------------------------------------------------------------

import htmlentitydefs


def normalize_twitter(text):
    """ normalization for twitter """
    text = re.sub(r'(@|#|https?:\/\/)[^ ]+', '', text)
    text = re.sub(r'(^| )[:;x]-?[\(\)dop]($| )', ' ', text)  # facemark
    text = re.sub(r'(^| )(rt[ :]+)*', ' ', text)
    text = re.sub(r'([hj])+([aieo])+(\1+\2+){1,}', r'\1\2\1\2', text, re.IGNORECASE)  # laugh
    text = re.sub(r' +(via|live on) *$', '', text)
    return text


# from http://www.programming-magic.com/20080820002254/
reference_regex = re.compile(u"&(#x?[0-9a-f]+|[a-z]+);", re.IGNORECASE)
num16_regex = re.compile(u"#x\d+", re.IGNORECASE)
num10_regex = re.compile(u"#\d+", re.IGNORECASE)


def htmlentity2unicode(text):
    result = u''
    i = 0
    while True:
        match = reference_regex.search(text, i)
        if match is None:
            result += text[i:]
            break

        result += text[i:match.start()]
        i = match.end()
        name = match.group(1)

        if name in htmlentitydefs.name2codepoint.keys():
            result += unichr(htmlentitydefs.name2codepoint[name])

        elif num16_regex.match(name):
            result += unichr(int(u'0'+name[1:], 16))

        elif num10_regex.match(name):
            result += unichr(int(name[1:]))

    return result

re_ignore_i = re.compile(r'[^I]')
re_latin_cont = re.compile(u"([a-z\u00e0-\u024f])\\1{2,}")
re_symbol_cont = re.compile(u"([^a-z\u00e0-\u024f])\\1{1,}")


def normalize_text(org):
    m = re.match(r'([-A-Za-z]+)\t(.+)', org)
    if m:
        label, org = m.groups()
    else:
        label = ""

    m = re.search(r'\t([^\t]+)$', org)

    if m:
        s = m.group(0)
    else:
        s = org

    s = htmlentity2unicode(s)
    s = re.sub(u'[\u2010-\u2015]', '-', s)
    s = re.sub(u'[0-9]+', '0', s)
    s = re.sub(u'[^\u0020-\u007e\u00a1-\u024f\u0300-\u036f\u1e00-\u1eff]+', ' ', s)
    s = re.sub(u'  +', ' ', s)

    # specific twitter normalization
    s = normalize_twitter(s)

    # asd
    s = re_latin_cont.sub(r'\1\1', s)

    # asd
    s = re_symbol_cont.sub(r'\1', s)

    return label, s.strip(), org

label, text, org_text = normalize_text(u'@l 200 hola $5.13 mundo!!!, :) este &gt; es &amp; un @kira tweet en español. ver http://www.google.com')

# print label
print text
print org_text
print ""

print u">" == u"&gt;"