
def get_ngrams(text, n, pre_proc=True):
    """
    Computes the n-grams of a given text
    :rtype : list
    :param text: The text provided
    :param n: The n of n-grams
    :param pre_proc: Wether a text preprocessing is required
    :return: List of all the word's n-grams
    """

    # preprocessing text if required
    text = " %s " % text if pre_proc else text[0:]

    # returning the list of n-grams
    return [text[i:i+n] for i in range(len(text) - n + 1)]
