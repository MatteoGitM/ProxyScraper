import threading
import time
import requests
import Settings

from urllib.parse import urlparse
from ProxyUtilits import ProxyUtilits
from ProxyInventory import Proxy, ProxyInventory
from TwitchViewBot import TwitchViewBot

class TestProxies(threading.Thread):
    def __init__(self, lock, inventory: ProxyInventory, eel):
        threading.Thread.__init__(self)
        self.demon = True
        self.stop = False
        self.lock = lock
        self.inventory = inventory
        self.eel = eel

    def kill(self):
        self.stop = True
        if Settings.DEBUG:
            print("[DEBUG] TestProxies", threading.get_ident(), 'Thread got stop order')     
          
    def auto_export(self):
        if Settings.AUTO_EXPORT:
            proxy_list = self.inventory.export_list()
            with open('proxies.txt', 'w') as file:
                    file.write(proxy_list)
    
    def test_proxy_proto(self, proxy: Proxy, protocol):
        if ProxyUtilits.protocol_allowed(protocol):
            proxy.type = protocol
            test_result = False
            
            for val_url, val_str in Settings.VALIDATORS.copy().items():
                domain = urlparse(val_url).netloc
                html = ProxyUtilits.connection(val_url, proxy)
                if val_str in html:
                    test_result = True
                    if not domain in proxy.validators:
                        proxy.validators.append(domain)
                # elif Settings.DEBUG:
                #     if proxy.last_tested:        
                #        print("[DEBUG] TestProxies", threading.get_ident(), str(proxy),' error response: ' , html[0:100])          
            return test_result     
        return False
    
    def test_proxy(self, proxy: Proxy):
         for protocol in ["http", "https", "socks4", "socks5"]:
             if self.test_proxy_proto(proxy, protocol):
                 return True
         return False 

    def run(self):
        while self.inventory:
            if self.stop: break             
            with self.lock:
                proxy = self.inventory.get_proxy()
                self.update_status_label()

            if proxy == None:
                return

            start = time.time()
            if not self.test_proxy(proxy): continue
            end = time.time()
            
            self.azenv_elite_test(proxy)

            if self.stop: break
            with self.lock:
                proxy.uptime = 1
                proxy.first_tested = proxy.last_tested = end
                self.update_proxy_list(proxy, start, end)

    def azenv_elite_test(self, proxy):
        html = ProxyUtilits.connection("http://207.246.70.16/", proxy)
        
        if not html.find('REMOTE_ADDR') == -1:
            if not any(x in html for x in Settings.ELITE_TAGS):
                proxy.iselite = True
        
        if not Settings.remote_ip:
            Settings.remote_ip = requests.get('http://icanhazip.com/', headers=Settings.HEADERS, timeout=5).text
            
        if Settings.remote_ip in html:
            proxy.istrasp = True
        
        #if not proxy.istrasp:
            #thread = TwitchViewBot(proxy=proxy, user="kilimakinafa")
            #thread.start()   

    def update_proxy_list(self, proxy: Proxy, start, end, update = False):
        TestProxies.auto_export(self)
        
        if proxy.country == "N/A":
            proxy.country= ProxyUtilits.ip2country(proxy.host)
        if proxy.spamhaus == "N/A":
            proxy.spamhaus = ProxyUtilits.check_spamhaus(proxy.host)
                
        anonymity = 'ELITE' if proxy.iselite else 'ANON'
        if proxy.istrasp: anonymity = "TRASP"
     
        data = {'Proxy': str(proxy),
                'Country': proxy.country,
                'Type': proxy.type.upper(),
                'Spamhaus': proxy.spamhaus,
                'HSTS': str(proxy.hsts).upper(),
                'Tests': ', '.join(proxy.validators),
                'Anonymity': anonymity,
                'Speed': int(end - start),
                'Uptime': proxy.uptime,
                }
        self.eel.updateData(data) if update else self.eel.addData(data)
    
    def remove_proxy(self, proxy: Proxy):
        self.eel.removeData({'Proxy': str(proxy)})
        
    def update_status_label(self):
        self.eel.updateLabel("Testing: %d/%d | Alive: %d | Elite: %d | Anon: %d | Trasp: %d" %
                             (self.inventory.tested_count, len(self.inventory),
                              self.inventory.count_alives(),
                              self.inventory.count_elites(), 
                              self.inventory.count_anons(), 
                              self.inventory.count_trasps()))