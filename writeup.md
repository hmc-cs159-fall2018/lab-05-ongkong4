# Lab 5

## 1. In Writeup.md, explain how Laplace smoothing works in general and how it is implemented in the EditDistance.py file. Why is Laplace smoothing needed in order to make the prob method work? In other words, the prob method wouldn’t work properly without smoothing – why?
Laplace smoothing is needed to increase the probabilities of very low probability
events (according to the training data). In doing so, smoothing decreases
probabilities of high probability events. In EditDistance, it is implemented in
the train_cost function. Before any counting of characters happen, all
characters get their counts increased by 0.1. Laplace smoothing is needed
because any characters not seen in the training set will be reppresented by
'unk'. Laplace smoothing is used so 'unk' has greater than 0 probability or else
any character not in the training set will result in 0 probability which will
result in infinite log probability when we compute prob.

## 2. Describe the command-line interface for EditDistance.py. What command should you run to generate a model from /data/spelling/wikipedia_misspellings.txt and save it to ed.pkl?
For the command-line interface, you specify the source file to train on denoted
by --source flag and you specify the file that you want to store the
probabilities using the --store flag.
python3 EditDistance.py --source ../data/Data/spelling/wikipedia_misspellings.txt --store ed.pkl

## 3. What n-gram orders are supported by the given LanguageModel class?
The unigram and bigram orders are supported.

## 4. How does the given LanguageModel class deal with the problem of 0-counts?
The LanuageModel class deals with the problem of 0-counts by doing laplace
smoothing with the value given by alpha. It is done in set_prob function.

## 5. What behavior does the “__contains__()” method of the LanguageModel class provide?
The __contains__ method in LanguageModel class is what's called when the "in"
keyword is used on an instance of the class. It checks if a word is in the
vocabulary class.

## 6. Spacy uses a lot of memory if it tries to load a very large document. To avoid that problem, LanguageModel limits the amount of text that’s processed at once with the get_chunks method. Explain how that method works.
The "get_chunks" method outputs an iterator whose elements are text from the
docuemnts, around 100000 bytes at a time. This is done by the line
"fp.readline(100000)".

## 7. Describe the command-line interface for LanguageModel.py. What command should you run to generate a model from /data/gutenberg/*.txt and save it to lm.pkl if you want an alpha value of 0.1 and a vocabulary size of 40000?
The store flag indicates the file to save the pickled file that contains
information about the trained lanuage model. The alpha flag indicates the alpha
to use for laplace smoothing. The vocab flag indicates the max size of the
vocabulary. Both the alpha and vocab flags are optional flags with default
values. There is also positional arguments that are training files, which is stored as a
list in variable name source.

python3 LanguageModel.py --store lm.pkl ../data/Data/gutenberg/*.txt --alpha 0.1 --vocab 40000

## 8.How often did your spell checker do a better job of correcting than ispell? Conversely, how often did ispell do a better job than your spell checker?

For words that are actually misspelled, I never found an instance where my spell
checker performed convincingly better than ispell. It was either as good or
worse than ispell. The only iffy instance was the following: the incorrectly
spelled phrase was "int he", but ispell changed it to "dint he" and my spell
checker changed it to "in he". The correct change was to change "int he" to "in
the", but spell checker got closer than ispell.

## 9.Can you characterize the type of errors your spell checker tended to best at, and the type of errors ispell tended to do best at?

ispell is good at replacing words with transposition, which my spellchecker
tends to get wrong. They both are bad at words that sound like they should be
valid words, but actually aren't. For example, "recoccur" is not a word and both
spell checkers miss that. The actual word is "recurs". What I found was that a
huge limitation of the spell checker I built was the size of the vocab. There
are some words that are completely valid, but aren't part of its vocabularly so
it will try to correct the word to a similar word/same word but with different
forms. Some examples are of plural
words will be corrected to singular form or vice versa.

## 10.Comment on anything else you notice that is interesting about spell checking – either for your model or for ispell.
ispell is more aggressive with corrections which leads to a ton of false
positives on errors. For example, ispell will correct and
will correct internet lingo (xD) agressively. My
spell checker also suffers from this false positive problem because its
vocabulary is limited. If it sees a word that is right, but its never accounted before,
it will try to correct that word.

My spellchecker also has weird interactions with words that contain "'" because
of the way the language model parses it. For example, can't will be parsed into
tokens "can" and "'t" which my spell checker will receive and turn into "can"
"not". This is technically not wrong, but is aggressive correction of
contractions. Another consequence is that it will mess up on possession
indications as the "'s" will be turned into "as" (Bob's => Bob as).

# I chose TRANSPOSITIONS
## 11.Describe your approach.
To consider transpositions, I modified the edit distance model to also consider
adjacent letter transpositions. I had to do laplace smoothing on different
possible letter switches. Then, in the edit distance algorithm, I considered
what if we switched the character we were currently on (the intended word) with
the character before it. I only considered it if it was a helpful switch
(switching the characters would match the last two characters of the observed
words). I had to introduce special representations for indicate characters
switching in the edit distance model. Also I had to edit spell checker to
consider transpositions as "1 change away" when generating suggestions.

## 12.Give examples of how your approach works, including specific sentences where your new model gives a different (hopefully better!) result than the baseline model.
The new model does well on transposition corrections which are quite common.
This new model was able to successfully correct the example sentence of "they
did not yb any menas", which is an improvement because the previous model was
not able to. Some other words that the model is able to correct are
"recieved" => "receieved" and "relief" => "releif" that the previous model
wasn't able to. There are still some transpositions that the model still isn't
able to correct, but most of them are because the original word isn't in the
vocabulary of the word

## 13.Discuss any challenges you ran into, design decisions you made, etc.
There were some challenges and design challenges that I ran into. First, I had
to decide how to define a transposition. I decided to only worry about adjacent
characters as non adjacent characters are less likely to happen as a typo
and would increase the representation complexity. Then I had to decide on the
exact representation and how to smoothly fit it into the edit distance
algorithm. I found that I needed to create a new token to represent swaps. After
this, everything fell into place as I just needed to modify backtracking and the
spell checker to suggest transpositions after that.
