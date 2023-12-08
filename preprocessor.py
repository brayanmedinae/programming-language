import re

COMMENTARY = r'#.*'

def preprocess(text):
    text = re.sub(COMMENTARY, '', text)
    return text.strip()