##
 # Harvey Mudd College, CS159
 # Swarthmore College, CS65
 # Copyright (c) 2018 Harvey Mudd College Computer Science Department, Claremont, CA
 # Copyright (c) 2018 Swarthmore College Computer Science Department, Swarthmore, PA
##


import argparse
import sys
from SpellCheck import SpellChecker
from LanguageModel import LanguageModel
from EditDistance import EditDistanceFinder

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--languagemodel", "-l", type=argparse.FileType('rb'), required=True)
    parser.add_argument("--editmodel", "-e", type=argparse.FileType('rb'), required=True)
    parser.add_argument("--corpus", "-c", type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument("--icorpus", type=argparse.FileType('r'))
    args = parser.parse_args()

    s=SpellChecker(max_distance=2)
    s.load_language_model(args.languagemodel)
    s.load_channel_model(args.editmodel)
    corpus = args.corpus.readlines()
    icorpus = args.icorpus.readlines()

    for i in range(len(corpus)):
        if icorpus[i] != corpus[i]:
            print("LINE: ", corpus[i])
            corrected = s.autocorrect_line(corpus[i])
            print("CORRECTED: ", corrected)
            print("ISPELL: ", icorpus[i])

