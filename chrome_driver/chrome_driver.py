import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os, inspect


class ChromeDriver:

    def __init__(self):
        self.current_dir = os.path.dirname(inspect.getfile(self.__class__))
        self.options = webdriver.ChromeOptions()


    def get_chrome_driver_dir(self):
        # chrome_driver_dir = self.current_dir + os.sep + "driver" + os.sep + "chromedriver.exe"
        chrome_driver_dir = webdriver.Chrome(ChromeDriverManager().install())
        return chrome_driver_dir


    def prepare_options(self):
        #proxy_host = self.current_proxy()
        #proxy = proxy_host.get_proxies()
        #proxy_ip = proxy[0]
        print("Ad block extension path: ", self.current_dir + os.sep + 'extension' + os.sep + 'ublockextension.crx')
        self.options.add_argument("--log-level=3")
        self.options.add_argument('--deny-permission-prompts')
        self.options.add_argument("enable-automation")
        #self.options.add_argument('--headless')
        self.options.add_extension(self.current_dir + os.sep + 'extension' + os.sep + 'ublockextension.crx')
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--dns-prefetch-disable")
        self.options.add_argument("--disable-gpu")

        preferences = {"profile.default_content_setting_values.geolocation": 2}
        self.options.add_experimental_option("prefs", preferences)
        time.sleep(3)
        return self.options

    def add_expired_driver_proxy(self):
        proxy_host = self.current_proxy()
        proxy = proxy_host.get_proxies()
        proxy_ip = proxy[0]
        proxy_host.add_expired_proxy(proxy_ip)
        print("proxy forcefully added into the expired list. Address:",proxy_ip)

    def chrome_driver_no_validation(self):
        driver_dir = self.get_chrome_driver_dir()
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3")
        options.add_argument('--deny-permission-prompts')
        options.add_argument("enable-automation")
        # self.options.add_argument('--headless')
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--dns-prefetch-disable")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-site-isolation-trials")

        preferences = {"profile.default_content_setting_values.geolocation": 2}
        options.add_experimental_option("prefs", preferences)
        chrome_driver = webdriver.Chrome(options=options, executable_path=driver_dir)
        return chrome_driver

    def get_chrome_driver(self,):
        driver_dir = self.get_chrome_driver_dir()
        options = self.prepare_options()
        chrome_driver = webdriver.Chrome(options=options, executable_path=driver_dir)
        return chrome_driver



if __name__ == '__main__':
    print("works")