import threading
import time
import Settings

from ProxyInventory import ProxyInventory
from TestProxies import TestProxies

class UptimeManager(threading.Thread):
       
    def __init__(self, lock, inventory: ProxyInventory, eel):
        threading.Thread.__init__(self)
        self.demon = True
        self.stop = False
        self.lock = lock
        self.inventory = inventory
        self.eel = eel

    def kill(self):
        self.stop = True
        
    def run(self):
        while True:
            if self.stop: break
            with self.lock:
                proxy = self.inventory.get_proxy_alive()
            
            if proxy == None:
                time.sleep(5)
                continue  
              
            if Settings.DEBUG:
                print("[DEBUG] ", threading.__name__, ' testing proxy: ', str(proxy))   
         
            proxy.last_tested = start = time.time()                                           
                                                            
            
            if not TestProxies.test_proxy_proto(self, proxy, proxy.type):
                if Settings.DEBUG:
                    print("[DEBUG] ", threading.__name__, ' This proxy failed test: ', str(proxy))   
         
                proxy.uptime -= 1
                if proxy.uptime >= 0: proxy.uptime = -1   
                if proxy.uptime <= -3: 
                    proxy.alive = False
                    if Settings.AUTO_REMOVE:
                        TestProxies.remove_proxy(self, proxy)
                    continue           
            
            if self.stop: break
            with self.lock:          
                if not proxy.uptime <= 0:
                    proxy.uptime = int(proxy.last_tested - proxy.first_tested)    
                    
                if Settings.DEBUG:
                    print("[DEBUG] ", threading.__name__, ' updating proxy: ', str(proxy))   
                
                TestProxies.update_proxy_list(self, proxy, start, time.time(), update=True)
            
            # self.proxies = [proxy for proxy in listofproxies if proxy not in self.proxies]
