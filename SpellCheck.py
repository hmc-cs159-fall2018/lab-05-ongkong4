import spacy
import argparse
from LanguageModel import LanguageModel
from EditDistance import EditDistanceFinder
import string
import re

class SpellChecker():
    def __init__(self, max_distance=1, channel_model=None, language_model=None):
        self.nlp = spacy.load("en", pipeline=["tagger", "parser"])
        self.channel_model = channel_model
        self.language_model = language_model
        self.max_distance = max_distance

    def load_channel_model(self, fp):
        self.channel_model = EditDistanceFinder()
        self.channel_model.load(fp)

    def load_language_model(self, fp):
        self.language_model = LanguageModel()
        self.language_model.load(fp)

    def bigram_score(self, prev_word, focus_word, next_word):
        if self.language_model:
            return (self.language_model.bigram_prob(prev_word, focus_word) +\
                    self.language_model.bigram_prob(focus_word, next_word))/2

    def unigram_score(self, word):
        if self.language_model:
            return self.language_model.unigram_prob(word)

    def cm_score(self, error_word, corrected_word):
        if self.channel_model:
            return self.channel_model.prob(error_word, corrected_word)

    def inserts(self, word):
        words = []
        for letter in string.ascii_lowercase:
            for i in range(len(word)+1):
                pos = word[:i] + letter + word[i:]
                if pos in self.language_model.vocabulary:
                    words.append(pos)
        return words

    def deletes(self, word):
        words = []
        for i in range(len(word)):
            pos = word[:i] + word[i+1:]
            if pos in self.language_model.vocabulary:
                words.append(pos)
        return words

    def substitutions(self, word):
        words = []
        for letter in string.ascii_lowercase:
            for i in range(len(word)):
                pos = word[:i] + letter +  word[i+1:]
                if pos in self.language_model.vocabulary:
                    words.append(pos)
        return words

    def transpositions(self, word):
        words = []
        for i in range(1, len(word)):
            pos = word[:i-1] + word[i] + word[i-1] + word[i+1:]
            if pos in self.language_model.vocabulary:
                words.append(pos)
        return words

    def generate_candidates(self, word):
        candidates = set()
        candidates.update(self.inserts(word))
        candidates.update(self.deletes(word))
        candidates.update(self.substitutions(word))
        d = self.max_distance - 1
        while d > 0:
            for word in candidates.copy():
                candidates.update(self.inserts(word))
                candidates.update(self.deletes(word))
                candidates.update(self.substitutions(word))
            d -= 1
        return list(candidates)

    def generate_candidates_optimized(self, word):
        return self.optimized_finder(word, self.max_distance)

    def score(self, prev_word, focus_word, next_word, observed_word):
        lang_score = 0.2*self.unigram_score(focus_word) + 0.8*self.bigram_score(prev_word, focus_word, next_word)
        return 0.7*lang_score + 0.3*self.cm_score(observed_word, focus_word)

    def check_sentence(self, sentence, fallback=False):
        suggestion = []
        for i in range(len(sentence)):
            observed_word = sentence[i]
            if observed_word.lower() in self.language_model or (len(observed_word) == 1 and observed_word not in string.ascii_lowercase):
                suggestion.append([observed_word])
                continue
            prev_word = None
            next_word = None
            if i == 0:
                prev_word = '<s>'
            else:
                prev_word = sentence[i-1]
            if i == len(sentence) - 1:
                next_word = '</s>'
            else:
                next_word = sentence[i+1]

            suggested = self.generate_candidates(observed_word)
            if fallback and len(suggested) == 0:
                suggested.append(observed_word)
            suggestion.append(
                sorted(
                    suggested,
                    key=lambda e: self.score(prev_word, e, next_word,
                        observed_word),
                    reverse=True
                )
            )
        return suggestion

    def get_tokens(self, sentence):
        return [x.text for x in sentence]

    def check_text(self, text, fallback=False):
        doc = self.nlp(text)
        result = []
        for sentence in doc.sents:
            tokens = self.get_tokens(sentence)
            result.append(self.check_sentence(tokens))
        return result

    def autocorrect_sentence(self, sentence):
        temp = self.check_sentence(sentence, True)
        result = []
        for token in temp:
            result.append(token[0])
        return result

    def autocorrect_line(self, line):
        doc = self.nlp(line)
        result = []
        for sentence in doc.sents:
            tokens = self.get_tokens(sentence)
            result.append(self.autocorrect_sentence(tokens))
        return '\n'.join([' '.join(sentence) for sentence in result])

    def suggest_sentence(self, sentence, max_suggestions):
        temp = self.check_sentence(sentence, True)
        result = []
        for token in temp:
            result.append(token[:max_suggestions])
        return result

    def suggest_text(self, text, max_suggestions):
        doc = self.nlp(text)
        result = []
        for sentence in doc.sents:
            tokens = self.get_tokens(sentence)
            result.append(self.suggest_sentence(tokens, max_suggestions))
        return result
