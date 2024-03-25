
import spacy
from spacy.matcher import Matcher
from python_main.scan_card.config import JOB_PATTERN, NAME_PATTERN, DIM_RESIZE_IMG, GUSSAIN_KIRNEL_ZISE
import cv2 as cv

class ImageHandler():
    
    @staticmethod
    def resize_img(image):
        image = cv.resize(image, DIM_RESIZE_IMG)
        return image
    
    @staticmethod
    def img_blurer(image):
        image = cv.blur(image, ksize=GUSSAIN_KIRNEL_ZISE)
        return image
    
    

class TextHandler():
    
    @staticmethod
    def text_extractor(reader, image):
        result = reader.readtext(image)
        text = []
        for i in result:
            text.append(i[-2])

        return '\t'.join(text)

    @staticmethod
    def names_extractor(matches, doc):
        names = []
        for match_id, start, end in matches:
            if doc.vocab.strings[match_id] == 'NAME':
                names.append(doc[start:end].text)

        return names
    
    @staticmethod
    def jobs_extractor(doc):
        job_titles = [ent.text for ent in doc.ents if ent.label_ == 'JOB_TITLE']
        return job_titles
    
    @staticmethod
    def match_creator(text, nlp):
        doc = nlp(text)
        matcher = Matcher(nlp.vocab)

        matcher.add('NAME', [NAME_PATTERN])

        matcher.add('JOB_TITLE', [JOB_PATTERN])

        matches = matcher(doc)
        return matches, doc
    
