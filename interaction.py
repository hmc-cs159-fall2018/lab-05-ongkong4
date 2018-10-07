##
 # Harvey Mudd College, CS159
 # Swarthmore College, CS65
 # Copyright (c) 2018 Harvey Mudd College Computer Science Department, Claremont, CA
 # Copyright (c) 2018 Swarthmore College Computer Science Department, Swarthmore, PA
##


from SpellCheck import SpellChecker
from LanguageModel import LanguageModel
from EditDistance import EditDistanceFinder
import argparse
import pickle
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--languagemodel", "-l", type=argparse.FileType('rb'), required=True)
    parser.add_argument("--editmodel", "-e", type=argparse.FileType('rb'), required=True)
    args = parser.parse_args()

    s=SpellChecker(max_distance=2)
    s.load_language_model(args.languagemodel)
    s.load_channel_model(args.editmodel)

    #print(s.channel_model.prob("hello", "hello"))
    #print(s.channel_model.prob("hellp", "hello"))
    #print(s.channel_model.prob("hllp", "hello"))

    #print(s.check_text("they did not yb any menas"))
    """
    >>> [['they'], ['did'], ['not'], ['by', 'b', 'ye', 'y', 'yo', 'ob', 'ya', 'ab'], ['any'], 
    >>>  ['means', 'mens', 'mena', 'zenas', 'menan', 'mends']]
    """

    sting = "they did not yb any menas"
    print(sting)
    print(s.autocorrect_line(sting))
    """
    >>> ['they', 'did', 'not', 'by', 'any', 'means']
    """
    sting = "I merely underlienes"
    print(sting)
    print(s.suggest_text(sting, 2))

    sting = "pronounce the foreing names"
    print(sting)
    print(s.suggest_text(sting, 2))

    sting = "One in hawiyei"
    print(sting)
    print(s.suggest_text(sting, 2))

    sting = "medeival period"
    print(s.suggest_text(sting, 2))

    sting = "recieve period"
    print(s.suggest_text(sting, 3))
    #print(s.suggest_text("they did not yb any menas", max_suggestions=2))
    """
    >>> ['they', 'did', 'not', ['by', 'b'], 'any', ['means', 'mens']]
    """
    #print(s.autocorrect_line("Why the edits made under my username Hardcore Metallica Fan were reverted? They weren't vandalisms, just closure on some GAs after I voted at"))

