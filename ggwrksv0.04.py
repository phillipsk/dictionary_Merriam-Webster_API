from Tkinter import *
#import settings
import py2mwapi

APIKEY = 'f1778399-c8c8-48fd-b6d8-4afd40ce0530'
APIKEY_T = 'a39b602f-93d0-491f-b4e7-2730b9cea4c2'

#################################################

def copytext():
    #print entry_1.get()
    entry_2.delete(0, END)  #remove any previous contents
    entry_2.insert(0, entry_1.get())

def print_function():
    dictionary = py2mwapi.DictionaryAPI(APIKEY)
    thesaurus = py2mwapi.ThesaurusAPI(APIKEY_T)
    define_me = "zeus"

    definition = dictionary.get_definition(define_me)
    synonyms = thesaurus.get_synonyms(define_me)
    related_words = thesaurus.get_related_words(define_me)
    print define_me
#################################################

mw = Tk()
label_1 = Label(mw, text="Enter some text: ")
entry_1 = Entry(mw)
label_2 = Label(mw, text='Output: ')
entry_2 = Entry(mw)

button_1 = Button(mw, text="Submit", command=print_function())



label_1.grid(row=0, column=0, sticky=W)
entry_1.grid(row=0, column=1)
label_2.grid(row=1, column=0, sticky=W)
entry_2.grid(row=1, column=1)
button_1.grid(row=3, columnspan=2, sticky=E)


mainloop()

