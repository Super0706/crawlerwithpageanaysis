from bs4 import BeautifulSoup as BS, SoupStrainer
from bs4.element import Comment
from lxml import etree
import re
from chrome_driver.chrome_driver import ChromeDriver
from component.file_processor.file_handler import FileHandler


class TagFinder:

    def __init__(self, query_tag: str, source_code: str):
        self.query_tag = query_tag
        self.source_code = source_code

    def find_availability(self):
        soup = BS(self.source_code, "lxml")
        total_found_length = len(soup.find_all(self.query_tag))
        if len(soup.find_all(self.query_tag)) == 0:
            available = "No"
            return available, total_found_length
        else:
            available = "Yes"
            return available, total_found_length

    def find_hyperlinks(self):
        count = 0
        for link in BS(self.source_code, "lxml", parse_only=SoupStrainer('a')):
            if link.has_attr('href'):
                count = count + 1
        return count

    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def find_prices(self):
        soup = BS(self.source_code, 'lxml')
        texts = soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts)
        visible_text = u" ".join(t.strip() for t in visible_texts)
        prices = re.findall(r'\s?(USD|EUR|€|£|\$)(?<!\d\.)(?:\d{1,3}(?:,\d{3})*|\d+)(?:\.\d{1,2})?(?!\.?\d)',
                            visible_text)
        if len(prices) > 0:
            return "Yes"
        return "No"

    def find_cta(self, cta_keyword):
        soup = BS(self.source_code, 'lxml')
        buttons = soup.findAll('button')
        a_tags_ctas = soup.findAll('a')
        div_buttons = [element for element in
                       soup.select('div[class*="button"]')]  ###checks div class which contains button
        div_buttons_short = [element for element in
                             soup.select('div[class*="btn"]')]  ##checks div class which contains button

        buttons_button_text = [i.text.strip() for i in buttons]
        atags_text = [atags.text.strip() for atags in a_tags_ctas]
        div_button_text = [i.text.strip() for i in div_buttons]
        div_buttons_short_text = [i.text.strip() for i in div_buttons_short]
        all_button_text = div_button_text + buttons_button_text + div_buttons_short_text + atags_text
        all_button_text = list(filter(None, all_button_text))

        cta_count = 0
        for button_text in all_button_text:
            for keyword in cta_keyword:
                if keyword.lower() in button_text.lower():
                    cta_count = cta_count + 1
        # print(all_button_text)
        # print("cta count ", str(cta_count))
        return cta_count

    def find_video_status(self):
        soup = BS(self.source_code, 'lxml')
        video_tags = soup.findAll('video')
        if len(video_tags) > 0:
            return "Yes"
        else:
            iframe_src = [iframe for iframe in soup.find_all('iframe')]
            if len(iframe_src) > 0:
                for iframe in iframe_src:
                    if iframe.has_attr('src'):
                        if 'youtube' in iframe['src']:
                            print("youtube")
                            return "Yes"
                        elif 'vimeo' in iframe['src']:
                            return "Yes"

        video_tags = [element for element in soup.select('div[class*="video"]')]
        if len(video_tags) > 0:
            return "Yes"
        return "No"

    def find_pop_up(self):
        soup = BS(self.source_code, 'lxml')
        page_modal_class = [element for element in soup.select('div[class*="modal"]')]
        page_popup_class = [element for element in soup.select('div[class*="popup"]')]
        page_modal_id = [element for element in soup.select('div[id*="modal"]')]
        page_popup_id = [element for element in soup.select('div[id*="popup"]')]
        popup = page_modal_class + page_popup_class + page_modal_id + page_popup_id
        if len(popup) > 0:
            return "Yes"
        return "No"


if __name__ == '__main__':
    cta_keywords_file_name = 'cta-keywords.csv'
    file_worker = FileHandler()
    cta_keywords_df = file_worker.file_reader(cta_keywords_file_name)
    cta_keywords = cta_keywords_df['keywords'].tolist()
    url = "https://www.dkawellness.com/dka--bb-fruitadv-tba/?time_elapsed=1&tab_comp=1&noplay=1&controls=1"
    # chrome_driver = ChromeDriver()
    # chrome_browser = chrome_driver.get_chrome_driver()
    # chrome_browser.get(url)
    # source_code = chrome_browser.page_source
    # TagFinder('', source_code).find_cta(cta_keywords)
    TagFinder('', "").find_video_status()
