import nltk
from nltk.corpus import wordnet as wn
from nltk.wsd import lesk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
import math
from nltk.book import text6

syns = wn.synsets('exercise')
print(syns)

# get def for the first noun synset
first_noun = wn.synset('exercise.n.01').definition()
print(first_noun)

# get a definition for the first verb synset
first_verb = wn.synset('exercise.v.01').definition()
print(first_verb)

# extract examples
ex = wn.synset('exercise.v.01').examples()
print(ex)

#extract lemmas
lemma = wn.synset('exercise.v.01').lemmas()
print(lemma)

# iterate over synsets
exercise_synsets = wn.synsets('exercise', pos=wn.VERB)
for sense in exercise_synsets:
    lemmas = [l.name() for l in sense.lemmas()]
    print("Synset: " + sense.name() + "(" +sense.definition() + ") \n\t Lemmas:" + str(lemmas))


# Print a hyponym/hypernym of ‘reptile.n.01’
reptile = wn.synset("reptile.n.01")
print("hypernym: ", reptile.hypernyms())
print("hyponym: ", reptile.hyponyms())

# Output the path_similarity of ‘shoot.v.01’ and ‘gun_down.v.01’
shoot = wn.synset('shoot.v.01')
gun_down = wn.synset('gun_down.v.01')
print(shoot.path_similarity(gun_down))

# Output the Wu-Palmer similarity of ‘shoot.v.01’ and ‘gun_down.v.01’
print(wn.wup_similarity(shoot, gun_down))

# look at the definitions for 'dwelling'
kitchen = wn.synset("kitchen.n.01")
print(kitchen.part_holonyms())

for ss in kitchen.part_holonyms():
    print(ss.definition())

# Find entailments of synset ‘snore.v.01’ using the “.entailments()” method
print(wn.synset("snore.v.01").entailments())

# morphy to find root form of "snoring"
print(wn.morphy('snoring', wn.VERB))

# Using the Lesk algorithm in NLTK, find the most likely synset of ‘arm’
# in the sentence below, and print the definition of that synset.
sentence = 'The soldier was convicted of selling arms in the war'
print(lesk(sentence, "arm", "n"))
for ss in wn.synsets('sleeve'):
    print(ss.definition())

# Using VADER sentiment analysis, print the polarity of the statement above.
analyzer = SentimentIntensityAnalyzer()
vs = analyzer.polarity_scores(sentence)
print(sentence, '\n\t', str(vs))

# 10.	Using NLTK Text object text6 Monty Python,
# calculate the pmi of ‘fire arrows’. Is this likely to be a collocation?hg = text.count('Holy Grail')/vocab
text = ' '.join(text6.tokens)
vocab = len(set(text6))
fire_arrows = text.count('Holy Grail')/vocab
fire = text.count('fire')/vocab
arrows = text.count('arrows')/vocab
pmi = math.log2(fire_arrows / (fire * arrows))
print('pmi = ', pmi)




