import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from operator import itemgetter
import os, inspect
import traceback

class Proxy:

    def __init__(self):
        self.source_one = "https://cagriari.com/fresh_proxy.txt"
        self.current_dir = os.path.dirname(inspect.getfile(self.__class__))
        self.expired_proxies_file_name = self.current_dir + os.sep + "expired" + os.sep + "expired_proxies.csv"

    def get_proxies_from_source(self):
        r = requests.get(self.source_one)
        soup = bs(r.content, "html.parser")
        proxies_data = soup.text.split('\n')
        proxies_data.remove(proxies_data[0])
        proxies_data.remove(proxies_data[1])
        proxies_data.remove(proxies_data[2])
        proxies_data.remove('# HTTPS, 5-second timeout')
        extracted_proxies = filter(None, proxies_data)
        proxies = []
        for proxy in extracted_proxies:
            proxies.append(proxy)
        return proxies

    def sort_source_one_proxy(self):
        try:
            source_one_proxies = self.get_proxies_from_source()
            if len(source_one_proxies) > 0:
                sorted_proxies = dict()
                for ip in source_one_proxies:
                    proxy_data = ip.split('|')
                    proxy_ip = proxy_data[0]
                    proxy_ping_rate = proxy_data[2][:-1]
                    sorted_proxies[proxy_ip] = proxy_ping_rate
                sorted_proxies = sorted(sorted_proxies.items(), key=itemgetter(1))
                return sorted_proxies

        except Exception as e:
            print(e)


    def get_expired_proxies(self):
        expired_proxy = pd.read_csv(self.expired_proxies_file_name)
        expired_proxy_list = expired_proxy['Expired'].tolist()
        return expired_proxy_list

    def add_expired_proxy(self, proxy):
        expired_proxy_df = pd.read_csv(self.expired_proxies_file_name)
        expired_proxy_df.loc[len(expired_proxy_df)] = [proxy, itu.get_current_timestamp()]
        expired_proxy_df.to_csv(self.expired_proxies_file_name, index=False)

    def get_proxies(self):
        try:
            filtered_proxies = []
            expired_proxies = self.get_expired_proxies()
            sorted_proxies = self.sort_source_one_proxy()
            for ip in sorted_proxies:
                ip = ip[0]
                if ip not in expired_proxies:
                    filtered_proxies.append(ip)

            if len(filtered_proxies) > 0:
                print("Fresh proxy loaded. Total loaded Proxies ==> ", str(len(filtered_proxies)))
                return filtered_proxies
            else:
                print("Reattempting to new fetch new Proxies ===> ", str(len(filtered_proxies)))
                print("If this issue persist, please stop the program and restart it.")

        except Exception as e:
            print("Exception occurred while proxy allocation ==> ", e)
            traceback.print_exc()

