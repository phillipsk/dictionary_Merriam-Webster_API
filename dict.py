from urllib.parse import quote_plus
from urllib.request import urlopen

import xml.etree.ElementTree as ET

ittag = str.encode('<it>')
itclose = str.encode('</it>')
empty = bytes('', 'utf-8')

class MerriamWebsterAPI:
    def __init__(self, key):
        self.key = key
        self.cachedXML = {}

    def _wrap_url(self, url):
         encoded_key = quote_plus(self.key)
         return url + "?key={}".format(encoded_key)
        
    def _retrieve_xml(self, word):
        if word in self.cachedXML:
            return self.cachedXML[word]
        endpoint_url = self._wrap_url(self.base_url + quote_plus(word))
        xmlre = urlopen(endpoint_url).read()
        #clean out the <it> tags which aren't completely compliant xml
        fullxml =  xmlre.replace(ittag, empty).replace(itclose, empty)
        self.cachedXML[word] = fullxml
        return fullxml

    def _get_xml_root(self, xml):
        root = ET.fromstring(xml)
        first_entry = root.find('entry')
        if not first_entry:
            raise MWApiException('No entries found')
        return first_entry
        

class ThesaurusAPI(MerriamWebsterAPI):
    base_url = 'http://www.dictionaryapi.com/api/v1/references/thesaurus/xml/'
    
    def _parse_xml_for_synonyms(self, xml):
        main_entry = self._get_xml_root(xml)
        senses = main_entry.find('sens')
        synonyms = senses.find('syn').text
        return synonyms.split(', ')

    def _parse_xml_for_antonyms(self, xml):
        main_entry = self._get_xml_root(xml)
        senses = main_entry.find('sens')
        antonyms = senses.find('ant').text
        return antonyms.split(', ')
    
    def _parse_xml_for_rel_words(self, xml):
        main_entry = self._get_xml_root(xml)
        senses = main_entry.find('sens')
        related_words = senses.find('rel').text.replace(';', ',')
        return related_words.split(', ')
        
    def get_synonyms(self, word):
        result = self._retrieve_xml(word)
        synonyms = self._parse_xml_for_synonyms(result)
        return synonyms

    def get_antonyms(self, word):
        result = self._retrieve_xml(word)
        antonyms = self._parse_xml_for_antonyms(result)
        return antonyms
    
    def get_related_words(self, word):
        result = self._retrieve_xml(word)
        related_words = self._parse_xml_for_rel_words(result)
        return related_words

class DictionaryAPI(MerriamWebsterAPI):
    base_url = 'http://www.dictionaryapi.com/api/v1/references/collegiate/xml/'
    
    def _parse_xml_for_def(self, xml):
        main_entry = self._get_xml_root(xml)
        deftag = main_entry.find('def')
        definition = deftag.find('dt').text.replace(':', '')
        return definition
        
    def _parse_xml_for_etym(self, xml):
        main_entry = self._get_xml_root(xml)
        etym = main_entry.find('et').text
        return etym
        
    def get_definition(self, word):
        result = self._retrieve_xml(word)
        definition = self._parse_xml_for_def(result)
        return definition
        
    def get_etymology(self, word):
        result = self._retrieve_xml(word)
        etym = self._parse_xml_for_etym(result)
        return etym
        

class MWApiException(Exception):
    pass

#######################################################################################################


import tkinter as tk

def center(win):
    """
    centers a tkinter window
    :param win: the root or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

calc = tk.Tk()
calc.title("God.Works")

FRONT_PAGE = ['Old Testament','New Testament']

buttons = [
'OT',  'NT']
"""
,  '9',  '*',  'C',
'4',  '5',  '6',  '/',  'Neg',
'1',  '2',  '3',  '-',  '$',
'0',  '.',  '=',  '+',  '@' ]
"""

# set up GUI
row = 1
col = 0
for i in FRONT_PAGE:
    button_style = 'raised'
    action = lambda x = i: click_event(x)
    tk.Button(calc, text = i, width = 17, height = 10, relief = button_style, command = action) \
    .grid(row = row, column = col, sticky = 'nesw')
    col += 1
    if col > 0: # if col > 4
        col = 0
        row += 1

display = tk.Entry(calc, width = 40, bg = "white")
display.grid(row = 0, column = 0, columnspan = 1) # columnspan = 5

def click_event(key):

    # = -> calculate results
    if key == '=':
        # safeguard against integer division
        if '/' in display.get() and '.' not in display.get():
            display.insert(tk.END, ".0")
            
        # attempt to evaluate results
        try:
            result = eval(display.get())
            display.insert(tk.END, " = " + str(result))
        except:
            display.insert(tk.END, "   Error, use only valid chars")
            
    # C -> clear display        
    elif key == 'C':
        display.delete(0, tk.END)
        
        
    # $ -> clear display        
    elif key == '$':
        display.delete(0, tk.END)
        display.insert(tk.END, "$$$$C.$R.$E.$A.$M.$$$$")
        

    # @ -> clear display        
    elif key == '@':
        display.delete(0, tk.END)
        display.insert(tk.END, "wwwwwwwwwwwwwwwwebsite")        

        
    # neg -> negate term
    elif key == 'neg':
        if '=' in display.get():
            display.delete(0, tk.END)
        try:
            if display.get()[0] == '-':
                display.delete(0)
            else:
                display.insert(0, '-')
        except IndexError:
            pass

    # clear display and start new input     
    else:
        if '=' in display.get():
            display.delete(0, tk.END)
        display.insert(tk.END, key)

# RUNTIME
center(calc)
calc.mainloop()

import tkinter  # Python 3

# if __name__ == '__main__':
#     root = tkinter.Tk()
#     root.attributes('-alpha', 0.0)
#     menubar = tkinter.Menu(root)
#     filemenu = tkinter.Menu(menubar, tearoff=0)
#     filemenu.add_command(label="Exit", command=root.destroy)
#     menubar.add_cascade(label="File", menu=filemenu)
#     root.config(menu=menubar)
#     frm = tkinter.Frame(root, bd=4, relief='raised')
#     frm.pack(fill='x')
#     lab = tkinter.Label(frm, text='Hello World!', bd=4, relief='sunken')
#     lab.pack(ipadx=4, padx=4, ipady=4, pady=4, fill='both')
#     center(root)
#     root.attributes('-alpha', 1.0)
#     root.mainloop()


dictionary = mwapi.DictionaryAPI(settings.APIKEY)
#definition = dictionary.get_definition(word)

Question_1 = "\n Define which word?\n"
define_me = input(Question_1)

print (dictionary.get_definition(define_me))