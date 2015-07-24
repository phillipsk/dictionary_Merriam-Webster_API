import mwapi

import settings
dictionary = mwapi.DictionaryAPI(settings.APIKEY)
#definition = dictionary.get_definition(word)

Question_1 = "\n Define which word?\n"
define_me = input(Question_1)

print (dictionary.get_definition(define_me))