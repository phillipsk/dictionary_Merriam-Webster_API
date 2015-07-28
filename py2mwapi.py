from urllib import quote_plus
from urllib import urlopen

import xml.etree.ElementTree as ET

ittag = str.encode('<it>')
itclose = str.encode('</it>')
empty = bytes('utf-8')

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
        if not len(first_entry):
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
