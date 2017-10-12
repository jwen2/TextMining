"""
John Wen - Text Mining assignment

"""

import requests
import random

def gettext(url):
    """ maybe modify this to incorporate other websites
        if I have the time"""
    return requests.get(url).text

Christmas = gettext('http://www.gutenberg.org/cache/epub/46/pg46.txt')
#OliverTwist = gettext('http://www.gutenberg.org/ebooks/730.txt.utf-8')
#DavidCopperfield = gettext('http://www.gutenberg.org/files/766/766-0.txt')
#GreatExpectations = gettext('http://www.gutenberg.org/files/1400/1400-0.txt')
#ATaleofTwoCities = gettext('http://www.gutenberg.org/files/98/98-0.txt')

def cleanuplist(textlist):
    """ takes a text as a string and returns a list of words
        without any of the symbols and lowercased

    >>> cleanuplist('This project is so hard!')
    ['this', 'project', 'is', 'so', 'hard']
    >>> cleanuplist('I need, a bunch, of !? doctest?')
    ['i', 'need', 'a', 'bunch', 'of', 'doctest']

    """
    cleanedlist = []
    textlist = textlist.lower().split()
    for word in textlist:
        symbols = "-_=+[}{]:;?/.>,<?!@#$%^&*()|'"
        for i in range (0,len(symbols)):
            word = word.replace(symbols[i], '')
        if len(word) > 0:
            cleanedlist.append(word)
    return cleanedlist

#print(len(cleanuplist(ATaleofTwoCities)))


def wordcounter(text):
    """ counts the text after it's cleaned up, ignoring symbols,
        by parsing through a list

    >>> wordcounter('This This This is is Another Docstring Test Test Is!!!!!!!!!')
    {'this': 3, 'is': 3, 'another': 1, 'docstring': 1, 'test': 2}

    """
    cleanlist = cleanuplist(text)
    d = dict()
    for words in cleanlist:
        d[words] = d.get(words,0) + 1
    return d


def highestfreqword(d):
    """ a) create a list of the dict's keys and values;
        b) return the key and value with the max value as a tuple

    >>> highestfreqword({'the': 5, 'apple': 2, 'is' : 3, 'large' : 15})
    ('large', 15)

    """
    v=list(d.values())
    k=list(d.keys())
    return k[v.index(max(v))], d[k[v.index(max(v))]]


def topNvalues(d,n):
    """ returns the top N values of the text as tuples in a list

    >>> topNvalues({'the': 5, 'apple': 2, 'is' : 3, 'large' : 15},2)
    [('large', 15), ('the', 5)]

    """
    newdictionary = d
    listoftups = []
    while n > 0:
        listoftups.append(highestfreqword(newdictionary))
        newdictionary.pop(highestfreqword(newdictionary)[0])
        n = n - 1
    return listoftups

#print(topNvalues(wordcounter(ATaleofTwoCities),5))

def uniquewordsused(s):
    """ returns the number of unique words in the string
    this function takes a lot of computational power LIKE A LOT

    >>> uniquewordsused('There should be six words used')
    6
    >>> uniquewordsused('There should be seven words used here')
    7
    """
    cleanlist = cleanuplist(s)
    counter = 0
    index = 1
    while index < len(cleanlist) + 1:
        if cleanlist[index - 1] not in cleanlist[index:]:
            if cleanlist[index - 1] not in cleanlist[:index - 1]:
                counter = counter + 1
        index = index + 1
    return counter

def dictionaryofprefixes(s):
    """ Returns a dictionary with a list of words in the text as keys
        and empty list as values. Will be used as a prefix index for suffixdictionary function.
        Does not repeat words

    >>> dictionaryofprefixes('This This This is another doctring test')
    {'this': [], 'is': [], 'another': [], 'doctring': [], 'test': []}

    """
    cleanlist = cleanuplist(s)
    d = {}
    for words in cleanlist:
        if words not in d:
            d[words] = []
    return d



def suffixdictionary(s):
    """ Takes the premade dictionary key index and starts appending
        suffixes to the list of values for each key

    >>> suffixdictionary('This cat is this cars best friend. This docstring is this assignments')
    {'this': ['cat', 'cars', 'docstring', 'assignments'], 'cat': ['is'], 'is': ['this'], 'cars': ['best'], 'best': ['friend'], 'friend': ['this'], 'docstring': ['is'], 'assignments': []}

    """
    d = dictionaryofprefixes(s)
    cleanlist = cleanuplist(s)
    index = 0
    while index < len(cleanlist) - 1:
        if cleanlist[index + 1] not in d[cleanlist[index]]:
            d[cleanlist[index]].append(cleanlist[index + 1])
        index = index + 1
    return d

#print(suffixes('This is a practice for a dictionary prefixes example so a cat can compute this program!!!'))


def sentencegenerator(text,startword,length = 10):
    """ Takes a sentence generator that only takes one prefix
        and generates a random suffix from the dictionary and creates
        a setence of values"""
    d = suffixdictionary(text)
    sentence = [startword]
    index = 0
    while index < length:
        sentence.append(random.choice(d[sentence[index]]))
        index = index + 1
    return ' '.join(sentence)


print(sentencegenerator((Christmas),'the',20))


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
