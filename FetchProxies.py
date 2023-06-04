import re
import threading
import requests
import Settings

from ProxyInventory import Proxy


class FetchProxies(threading.Thread):
    def __init__(self, lock, urls, inventory):
        threading.Thread.__init__(self)
        self.demon = True
        self.stop = False
        self.urls = urls
        self.lock = lock
        self.inventory = inventory
        
    def kill(self):
        self.stop = True
        
    def scrape(self, url):
        try:
            html = requests.get(url, headers=Settings.HEADERS, timeout=5).text
            if not html is None:
                return re.findall(Settings.regex_string, html)
            return ''
        except Exception as e:
            return str(e)

    def run(self):
        while self.urls:
            if self.stop: break
            with self.lock: url = self.urls.pop()
                
            raw_list = self.scrape(url)
            for proxy_line in raw_list:
                if not ':' in proxy_line: continue
                with self.lock:
                    self.inventory.add(Proxy(host=proxy_line.split(":")[0],
                                             port=proxy_line.split(":")[1],
                                             type='uknown'))

            print(f'{url} yield {len(self.inventory)}')
