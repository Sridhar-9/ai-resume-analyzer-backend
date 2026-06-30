import re
from bs4 import BeautifulSoup
import neattext.functions as nfx
import contractions

def clean_text(raw_text):

    text = BeautifulSoup(raw_text, 'html.parser').get_text()
    text = contractions.fix(text)

    text = nfx.replace_emails(text, replace_with="[EMAIL_HIDDEN]")
    text = nfx.replace_phone_numbers(text, replace_with="[PHONE_HIDDEN]")
    text = nfx.replace_urls(text, replace_with="[URL_HIDDEN]")

    text = re.sub(r'[•▪◦■🗹*-]', '', text)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()