import re 
import spacy
from spacy.matcher import Matcher
import json


from python_main.scan_card.config import PHONE_PATTERN, EMAIL_PATTERN, URL_PATTERN
from .util import TextHandler

class ScanCardReader():
    def __init__(self) -> None:
        self.nlp = spacy.load("en_core_web_sm")
    
    def extract_entities(self,text):
        
        matches, doc = TextHandler.match_creator(text, self.nlp)

        names = TextHandler.names_extractor(matches, doc)

        phone_numbers = re.findall(PHONE_PATTERN, text)

        emails = re.findall(EMAIL_PATTERN, text)

        url = re.findall(URL_PATTERN, text)

        job_titles = TextHandler.jobs_extractor(doc)

        self.data = {
            'name':names[0] if names else None,
            'phone_number':phone_numbers[0] if phone_numbers else  None,
            'email': emails[0] if emails else None,
            'url': url[-1] if url else None,
            'job_title': job_titles[0] if  job_titles else None
        }
    
    def to_json(self): 
        return json.dumps(self.data)
