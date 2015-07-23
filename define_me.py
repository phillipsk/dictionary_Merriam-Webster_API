import mwapi

APIKEY = 'f1778399-c8c8-48fd-b6d8-4afd40ce0530'
dictionary = mwapi.DictionaryAPI(APIKEY)
#definition = dictionary.get_definition(word)

Question_1 = "\n Define which word?\n"
define_me = input(Question_1)

print (dictionary.get_definition(define_me))