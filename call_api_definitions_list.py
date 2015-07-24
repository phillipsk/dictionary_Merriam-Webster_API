import re

file = open('vocab.txt', 'r')
# .lower() returns a version with all upper case characters replaced with lower case characters.
text = file.read().lower()
file.close()
# replaces anything that is not a lowercase letter, a space, or an apostrophe with a space:
text = re.sub('[^a-z\ \']+', " ", text)
words = list(text.split())
#print (words)

import mwapi
import settings

dictionary = mwapi.DictionaryAPI(settings.APIKEY)
thesaurus = mwapi.ThesaurusAPI(settings.APIKEY_T)
#definition = dictionary.get_definition(word)

#Question_1 = "\n Define which word?\n"
#define_me = input(Question_1)

#print (dictionary.get_definition(define_me))

for i in words:
	definition = dictionary.get_definition(i)
	synonyms = thesaurus.get_synonyms(i)
	related_words = thesaurus.get_related_words(i)
	print ('\n',i)
	print ('Definition:',definition,'\n')
	print('Synonyms',synonyms,'\n')
	print ('Related Words:',related_words,'\n')

	