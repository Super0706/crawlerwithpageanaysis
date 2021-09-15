from bs4 import BeautifulSoup
from bs4.element import Comment
import re


class WordCounter:

    def __init__(self, source_code):
        self.source_code = source_code

    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def extract_words(self, ):
        soup = BeautifulSoup(self.source_code, 'lxml')
        texts = soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts)
        visible_text = u" ".join(t.strip() for t in visible_texts)
        visible_text = re.sub('<[^<]+?>', '', visible_text)
        punctuations = "!@#$%^&*()_-=+:;{}[]<>,.?/\''"
        visible_text = ''.join(c for c in visible_text if c not in punctuations)

        return visible_text

    def find_word_count(self):
        clean_text = self.extract_words()
        clean_text = clean_text.split(' ')
        clean_text = list(filter(None, clean_text))
        return len(clean_text)


if __name__ == '__main__':
    print("works")