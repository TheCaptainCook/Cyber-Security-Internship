from nltk.parse.generate import generate, demo_grammar
from nltk import CFG

#https://www.nltk.org/howto.html

#An example grammar:

grammar = CFG.fromstring(demo_grammar)
print(grammar)


#All sentences of max depth 4:

for sentences in generate(grammar, depth=4):
    print(' '.join(sentences))