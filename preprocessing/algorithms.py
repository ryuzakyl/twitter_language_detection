# -*- coding: utf-8 -*-

import re
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