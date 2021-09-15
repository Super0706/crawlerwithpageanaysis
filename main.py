import time
from selenium.common.exceptions import TimeoutException, WebDriverException
from chrome_driver.chrome_driver import ChromeDriver
from component.file_processor.file_handler import FileHandler
from component.metrics_worker.word_counter import WordCounter
from component.metrics_worker.tag_finder import TagFinder
from internal_util import web_util
from component.img_similarity.check_pop_similarity import PopSimilarity
import traceback


def main():
    data_file_name = 'crawler-sampleurls.csv'
    cta_keywords_file_name = 'cta-keywords.csv'

    chrome_driver = ChromeDriver()
    file_worker = FileHandler()
    similarity_check = PopSimilarity()

    url_data_df = file_worker.file_reader(data_file_name)
    cta_keywords_df = file_worker.file_reader(cta_keywords_file_name)

    cta_keywords = cta_keywords_df['keywords'].tolist()
    urls = url_data_df['URL'].tolist()

    chrome_browser = chrome_driver.get_chrome_driver()
    count = 1

    for url in urls:
        try:

            chrome_browser.get(url)
            chrome_browser.set_page_load_timeout(60)
            source_code = chrome_browser.page_source
            img_name_first = web_util.get_temp_img_data_path() + 'onload-first.png'
            chrome_browser.save_screenshot(img_name_first)
            total_words = WordCounter(source_code).find_word_count()
            number_list_available, total_numbered_list = TagFinder('ol', source_code).find_availability()
            bullet_points_available, total_bullet_points = TagFinder('ul', source_code).find_availability()
            total_hyper_link = TagFinder('a', source_code).find_hyperlinks()
            ctas = TagFinder('cta', source_code).find_cta(cta_keywords)
            img_points_available, total_img = TagFinder('img', source_code).find_availability()
            price_on_page = TagFinder('prices', source_code).find_prices()
            button_available, total_buttons_tags = TagFinder('button', source_code).find_availability()
            total_div_buttons = chrome_browser.find_elements_by_xpath("//div[contains(@class, 'button')]")
            total_div_buttons = len(set([i.text for i in total_div_buttons]))
            pop_up_on_page = TagFinder('popup', source_code).find_pop_up()
            video_status = TagFinder('video_status', source_code).find_video_status()
            time.sleep(10)
            img_name_two = web_util.get_temp_img_data_path() +'after-onload-delay.png'
            chrome_browser.save_screenshot(img_name_two)

            similar = similarity_check.check_popup(img_name_first, img_name_two)
            if similar:
                entry_popup = "Yes"
            else:
                entry_popup = "No"

            exit_popup = pop_up_on_page

            new_row = [url,
                       total_words,
                       number_list_available,
                       total_numbered_list,
                       bullet_points_available,
                       total_bullet_points,
                       total_hyper_link,
                       ctas,
                       total_img,
                       pop_up_on_page,
                       entry_popup,
                       exit_popup,
                       price_on_page,
                       str(total_div_buttons + total_buttons_tags),
                       video_status]

            print(count, new_row)
            file_worker.apppend_csv_data_file(new_row)
            count = count + 1


        except TimeoutException as ex:
            print("Time out exception: ", ex)
            row = [url, str(ex)]
            file_worker.append_error_url(row)
            count = count + 1
            error = True

        except WebDriverException as ex:
            print("Web Driver Exception: ", ex)
            row = [url, str(ex)]
            file_worker.append_error_url(row)
            count = count + 1
            error = True

        except Exception as ex:
            print("An exception occurred for this url", url + " " + str(ex))
            row = [url, str(ex)]
            print(traceback.format_exc())
            file_worker.append_error_url(row)
            count = count + 1

    chrome_browser.quit()


if __name__ == '__main__':
    main()
