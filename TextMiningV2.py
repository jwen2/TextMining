"""
John Wen - Text Mining assignment

"""

import requests
#requests used to obtain text from urls.
import random
#random function used to generate sentences based on prefix-suffix

def gettext(url):
    """takes a url and returns the url as a long string"""
    return requests.get(url).text

"""Top 5 Charles Dickens Books as Text Files"""

Christmas = gettext('http://www.gutenberg.org/cache/epub/46/pg46.txt')
OliverTwist = gettext('http://www.gutenberg.org/ebooks/730.txt.utf-8')
DavidCopperfield = gettext('http://www.gutenberg.org/files/766/766-0.txt')
GreatExpectations = gettext('http://www.gutenberg.org/files/1400/1400-0.txt')
ATaleofTwoCities = gettext('http://www.gutenberg.org/files/98/98-0.txt')

def cleanuplist(textlist):
    """ takes a text as a string and returns a list of words
        without any of the symbols and lowercased

    >>> cleanuplist('This project is so hard!')
    ['this', 'project', 'is', 'so', 'hard']
    >>> cleanuplist('I need, a bunch, of !? doctest?')
    ['i', 'need', 'a', 'bunch', 'of', 'doctest']

    Functionality: iteratively go through the words in the list and if they are in the symbols
    it would replace the symbol with a space
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

def wordcounter(text):
    """ counts the text after it's cleaned up, ignoring symbols,
        by parsing through a list

    >>> wordcounter('This This This is is Another Docstring Test Test Is!!!!!!!!!')
    {'this': 3, 'is': 3, 'another': 1, 'docstring': 1, 'test': 2}
    >>> wordcounter('Test Test and way more test')
    {'test': 3, 'and': 1, 'way': 1, 'more': 1}

    Functionality: goes through the dictionary and uses the get function to change the values of each key
    """
    cleanlist = cleanuplist(text)
    d = dict()
    for words in cleanlist:
        d[words] = d.get(words,0) + 1
    return d


def highestfreqword(d):
    """ returns the highest value in the dictionary as a tuple pair

    >>> highestfreqword({'the': 5, 'apple': 2, 'is' : 3, 'large' : 15})
    ('large', 15)
    >>> highestfreqword({'the': 5, 'apple': 8, 'is' : 3, 'large' : 2})
    ('apple', 8)

    Functionality: Breaks down the dictionary down into lists of keys and values and
    picks the highest value and maps that index back to the key.
    """
    v=list(d.values())
    k=list(d.keys())
    return k[v.index(max(v))], d[k[v.index(max(v))]]


def topNvalues(d,n):
    """ returns the top N values of the text as tuples in a list

    >>> topNvalues({'the': 5, 'apple': 2, 'is' : 3, 'large' : 15}, 2)
    [('large', 15), ('the', 5)]
    >>> topNvalues({'cars': 51, 'bananas': 252, 'pies' : 33, 'bread' : 153}, 3)
    [('bananas', 252), ('bread', 153), ('cars', 51)]

    Functionality: Runs the highestfreqword function N times while popping out the
    selected value after each trial.

    """
    newdictionary = d
    listoftups = []
    while n > 0:
        listoftups.append(highestfreqword(newdictionary))
        newdictionary.pop(highestfreqword(newdictionary)[0])
        n = n - 1
        #runs through the function and adds the highest value tuple to the list and then
        #pops it from the original dictionary
    return listoftups

def uniquewordsused(s):
    """ returns the number of unique words in the string
    this function takes a lot of computational power LIKE A LOT

    >>> uniquewordsused('There should be six words used')
    6
    >>> uniquewordsused('There should be seven words used here')
    7

    Functionality: Takes a list of words, and runs two if functions through each word.
    The if functions check to see if the word appears before the index and after the index value.
    If it doesn't then it adds one to the counter.

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
    >>> dictionaryofprefixes('More docstring tests')
    {'more': [], 'docstring': [], 'tests': []}

    Functionality: Just returns each word as keys with empty values.
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
    >>> suffixdictionary('Maybe if I create more docstrings, I will get a 5')
    {'maybe': ['if'], 'if': ['i'], 'i': ['create', 'will'], 'create': ['more'], 'more': ['docstrings'], 'docstrings': ['i'], 'will': ['get'], 'get': ['a'], 'a': ['5'], '5': []}
    """
    d = dictionaryofprefixes(s)
    cleanlist = cleanuplist(s)
    index = 0
    while index < len(cleanlist) - 1:
        if cleanlist[index + 1] not in d[cleanlist[index]]:
            d[cleanlist[index]].append(cleanlist[index + 1])
        index = index + 1
    return d

def sentencegenerator(text,startword,length = 10):
    """ Takes a sentence generator that only takes one prefix
        and generates a random suffix from the dictionary and creates
        a setence of values

    >>> sentencegenerator(Christmas,'the',20)
    'the lock "ill give him as heartily sorry he wrote the foundations ein or using his steps towards you" returned the'
    Functionality: Starts with a word, and goes through the created prefix-suffix dictionary
    and randomly selects a element in that value list.
    """
    random.seed(1)
    #randomseed value for doctest, comment out to actually have the function run
    d = suffixdictionary(text)
    sentence = [startword]
    index = 0
    while index < length:
        sentence.append(random.choice(d[sentence[index]]))
        index = index + 1
    return ' '.join(sentence)

"""Results of sentence generator

print(sentencegenerator((Christmas),'the',20))
Results1: the shop but to express the upper portion of tank his feet observable beneath the habit with my dears god bless
Results2: the children in too well in carriages and lying down for" muttered with christmas past relenting" said so irresistibly contagious as
Results3: the burialplace of chestnuts on cornhill at midnight hark the quick wheels of addressing mr scrooges keyhole and tender and his
"""

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
