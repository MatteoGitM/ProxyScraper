import socket
import mmap
import requests
import Settings

from requests.adapters import HTTPAdapter, Retry
from ProxyInventory import Proxy

class ProxyUtilits():  
    requests.packages.urllib3.disable_warnings()
    
    def connection(uri, proxy: Proxy, hsts=Settings.CERT_LOCATION):
        try:
            prxy = f"{proxy.type}://{proxy.host}:{proxy.port}"
            s = requests.Session()
            retries = Retry(total=Settings.MAX_RETRIES, backoff_factor=0.0)

            s.mount('https://', HTTPAdapter(max_retries=retries))
            s.mount('http://', HTTPAdapter(max_retries=retries))

            r = s.get(uri,
                      headers=Settings.HEADERS,
                      proxies={"http": prxy, "https": prxy},
                      verify=hsts if proxy.hsts else False,
                      timeout=Settings.TIMEOUT)

            s.close()  # close session !!
            r.close()  # close response !!

            return r.text        
        except Exception as e:
            # print(str(e))
            if 'CERTIFICATE' in str(e):
                proxy.hsts = False
                return ProxyUtilits.connection(uri, proxy)
            return str(e)
     
    def protocol_allowed(protocol):
        match protocol.lower():
            case 'http':
                return Settings.HTTP_CHECK
            case 'https':
                return Settings.HTTP_CHECK
            case 'socks4':
                return Settings.SOCKS4_CHECK
            case 'socks5':
                return Settings.SOCKS5_CHECK
               
    def check_spamhaus(ip):
        hostname = ".".join(ip.split(".")[::-1]) + ".zen.spamhaus.org"
        try:
            result = socket.gethostbyname(hostname)
        except socket.error:
            result = 0

        rdict = {"127.0.0.2": "SBL",
                "127.0.0.3": "SBL CSS",
                "127.0.0.4": "XBL",
                "127.0.0.6": "XBL",
                "127.0.0.7": "XBL",
                "127.0.0.9": "SBL",
                "127.0.0.10": "PBL",
                "127.0.0.11": "PBL",
                0: "Not Found"}
        
        return rdict[result]    
    
    def ip2country(ip):
        try:
            data = mmap.mmap(Settings.dbip.fileno(), 0, access=mmap.ACCESS_READ)
            raw_ip = '\n' + ip.split('.')[0] + '.' + ip.split('.')[1]
            search_index = data.find(str.encode(raw_ip))
            search_result = data[search_index:search_index + 100000].decode()
            for line in search_result.split('\n'):
                if ',' in line:
                    proxy_range = line.split(",")[1]
                    country = line.split(",")[2]          
                    if ip.split('.')[0] <= proxy_range.split('.')[0] \
                            and ip.split('.')[1] <= proxy_range.split('.')[1] \
                            and ip.split('.')[2] <= proxy_range.split('.')[2] \
                            and ip.split('.')[3] <= proxy_range.split('.')[3]:
                        return country
            return 'UNK'
        except Exception as e:
            return 'UNK'
