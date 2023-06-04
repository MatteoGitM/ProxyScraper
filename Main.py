import os, signal
import threading
import time
import eel
import psutil
import json
import eel.browsers
import Settings
import Server

from TestProxies import TestProxies
from FetchProxies import FetchProxies
from ProxyInventory import ProxyInventory, Proxy
from TwitchViewBot import TwitchViewBot
from UptimeManager import UptimeManager
      
locker = threading.Lock()
proxies = ProxyInventory()
threads = []
      
def test_threads(proxies, locker, i=0):
    threads_i = i if i > 0 else Settings.THREADS_NUMBER
    
    if Settings.DEBUG:
        print("[DEBUG] ", "threads used for testing: ", threads_i)
    
    for i in range(threads_i):
        thread = TestProxies(lock=locker, inventory=proxies, eel=eel)
        thread.start()
        threads.append(thread)

def uptime_threads(proxies, locker):
    for i in range(100):
        thread = UptimeManager(lock=locker, inventory=proxies, eel=eel)
        thread.name = f"Uptime-{i}"
        thread.start()
        threads.append(thread)

def fetch_threads(proxies, locker):
    p_list = Settings.PROXY_LIST.copy()
    for i in range(30):
        thread = FetchProxies(urls=p_list, lock=locker, inventory=proxies)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def start_http_server():
    server = Server.SimpleHttpServer('', 8998, proxies)
    server.start()

def resources_log(lock):
    while True:
        with lock:
            RAM = psutil.Process(os.getpid()).memory_info()[0] / float(2 ** 20)
            CPU = psutil.Process(os.getpid()).cpu_percent(interval=1) 
            eel.updateRightLabel(f'CPU: {str(CPU)}% | RAM: {str(RAM)[:5]}MB')
            time.sleep(1)
            
def close_callback(route, websockets):
    if not websockets:
        print('Exiting...', route)
        Settings.save_settings(Settings)
        os.kill(os.getpid(), signal.SIGSTOP)
            
@eel.expose
def start_bot():
    start_http_server()
    
    if not len(Settings.VALIDATORS) >= 1:
        eel.updateLabel("Please add atleast one validator")
        return
    
    threads.clear()
        
    fetch_threads(proxies, locker)      
    
    proxies.proxies = list(set(proxies.proxies))
    
    if Settings.DEBUG:
        print("[DEBUG] ", 'scraped ', len(proxies), ' proxies from sources')
        
    uptime_threads(proxies, locker)               
    test_threads(proxies, locker)
         
@eel.expose
def stop_bot():
    proxies.tested_count = 0
    for thread in threads:
        thread.kill()
        
@eel.expose        
def change_threads_setting(x):
    if Settings.DEBUG:
        print("[DEBUG] ", 'threads number: ', x)
    
    old_threads_number = Settings.THREADS_NUMBER
    Settings.THREADS_NUMBER = int(x)
    
    if Settings.THREADS_NUMBER < old_threads_number:
        threads_to_kill = old_threads_number - Settings.THREADS_NUMBER 
        for i in range(threads_to_kill):
            for thread in threads:
                if 'TestProxies' in str(thread):
                    thread.kill()
                    threads.remove(thread)
                    break           
    elif Settings.THREADS_NUMBER > old_threads_number:
        threads_to_start = Settings.THREADS_NUMBER - old_threads_number 
        test_threads(proxies, locker, threads_to_start)
    
@eel.expose
def get_settings():
    json_dump = json.dumps(Settings.VALIDATORS)
    eel.updateVal(str(json_dump))
    eel.updateSettingsUI(int(Settings.THREADS_NUMBER),
                         int(Settings.TIMEOUT),
                         int(Settings.UPTIME_TIMESTAMP),
                         int(Settings.MAX_RETRIES),
                         Settings.SOCKS5_CHECK,
                         Settings.SOCKS4_CHECK,
                         Settings.HTTP_CHECK,
                         Settings.AUTO_REMOVE,
                         Settings.AUTO_EXPORT,
                         Settings.MULTI_PORT)

@eel.expose
def remove_proxy(x):
    if Settings.DEBUG:
         print("[DEBUG] ", 'removed proxy : ', x)             
    proxies.remove(x)

def main():  
    #thread = TwitchViewBot(Proxy("127.0.0.1", "8889", "socks5"), user="fondazionepaceebene")
    #thread.start()
    #exit()
    Settings.load_settings()
     
    thread = threading.Thread(target = resources_log, args = (threading.Lock(),))
    thread.start()
        
    Settings.PROXY_LIST = []
    
    with open('proxy_sources.txt', 'r', encoding='UTF-8') as file:
        while (line := file.readline().rstrip()):
            Settings.PROXY_LIST.append(line)  
    
    #eel.browsers.set_path('chrome', str(pathlib.Path().resolve()) + '/Chromium.app/Contents/MacOS/Chromium')
    eel.start('index.html', mode='default',  close_callback=close_callback, cmdline_args=["--test-type"])
   
if __name__ == '__main__':
    eel.init('web')
    main()