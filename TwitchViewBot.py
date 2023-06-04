import threading
import uuid
import requests
import Settings
import json
import urllib.parse
import random

from requests.adapters import HTTPAdapter, Retry
from ProxyInventory import Proxy


def USER_AGENT():
    UA = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
          "Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0",
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
          "Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0",
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:104.0) Gecko/20100101 Firefox/104.0",
          "Mozilla/5.0 (Windows NT 10.0; rv:104.0) Gecko/20100101 Firefox/104.0",
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15",
          "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
          "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33",
          "Mozilla/5.0 (Windows NT 10.0; rv:103.0) Gecko/20100101 Firefox/103.0",
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36",
          "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0",
          "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
          "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27",
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:103.0) Gecko/20100101 Firefox/103.0",
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15",
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15",
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.63",
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42",
          "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70",
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
          "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
          "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",
          "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
          "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
          "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36",
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0",
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36",
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.100",
          "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
          "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36",
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.84",
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
          "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0",
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36",
          "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0"]
    return random.choice(UA)

USERAGENT = USER_AGENT()

def connection(uri, proxy: Proxy, headers, method="GET", data="", cookies=False):
    try:
        prxy = f"{proxy.type}://{proxy.host}:{proxy.port}"
        s = requests.Session()
        retries = Retry(total=15, backoff_factor=0.0)

        s.mount('https://', HTTPAdapter(max_retries=retries))
        s.mount('http://', HTTPAdapter(max_retries=retries))

        if method == "GET":
            r = s.get(uri,
                      headers=headers,
                      proxies={"http": prxy, "https": prxy},
                      verify=False,
                      timeout=300)
        else:
            r = s.post(uri, data,
                      headers=headers,
                      proxies={"http": prxy, "https": prxy},
                      verify=False,
                      timeout=300)

        s.close()  # close session !!
        r.close()  # close response !!

        if not cookies:
            return r.text
        else:
            return r.cookies
    except Exception as e:
        return str(e)


class TwitchViewBot(threading.Thread):
    HEADERS_GET = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
           'Accept-Language': 'en-US',
           'Accept-Encoding': 'gzip',
           'Upgrade-Insecure-Requests': '1',
           'Sec-Fetch-Dest': 'document',
           'Sec-Fetch-Mode': 'navigate',
           'Sec-Fetch-Site': 'none',
           'Sec-Fetch-User': '?1'}
    
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
           'Accept': '*/*',
           'Accept-Language': 'en-US',
           'Accept-Encoding': 'gzip',
           'Referer': 'https://www.twitch.tv/',
           'Authorization': 'undefined',
           'Client-ID': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
           'Content-Type': 'text/plain; charset=UTF-8',
           'Device-ID': 'QOaGnY0CcHXnNv3XZp5jggQrV0KVRjr8',
           'Origin': 'https://www.twitch.tv',
           'Connection': 'keep-alive',
           'Sec-Fetch-Dest': 'empty',
           'Sec-Fetch-Mode': 'cors',
           'Sec-Fetch-Site': 'same-site'}
    HEADERS_PLAYLIST = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
           'Accept': 'application/x-mpegURL, application/vnd.apple.mpegurl, application/json, text/plain',
           'Accept-Language': 'en-US',
           'Accept-Encoding': 'gzip, deflate, br',
           'Referer': 'https://www.twitch.tv/',
           'Origin': 'https://www.twitch.tv',
           'Connection': 'keep-alive',
           'Sec-Fetch-Dest': 'empty',
           'Sec-Fetch-Mode': 'cors',
           'Sec-Fetch-Site': 'cross-site'}
    HEADERS_SEGMENT = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
           'Accept': '*/*',
           'Accept-Language': 'en-US',
           'Accept-Encoding': 'gzip',
           'Referer': 'https://www.twitch.tv/',
           'Origin': 'https://www.twitch.tv',
           'Connection': 'keep-alive',
           'Sec-Fetch-Dest': 'empty',
           'Sec-Fetch-Mode': 'cors',
           'Sec-Fetch-Site': 'cross-site'}

    def __init__(self, proxy, user):
        threading.Thread.__init__(self)
        self.demon = True
        self.proxy = proxy
        self.username = user
    
    def run(self):
        try:  
            USERAGENT = USER_AGENT()
            
            HEADERS = TwitchViewBot.HEADERS.copy()
            HEADERS_GET = TwitchViewBot.HEADERS_GET.copy()
            HEADERS_PLAYLIST = TwitchViewBot.HEADERS_PLAYLIST.copy()
            HEADERS_SEGMENT = TwitchViewBot.HEADERS_SEGMENT.copy()
            
            HEADERS['User-Agent'] = USERAGENT
            HEADERS_GET['User-Agent'] = USERAGENT
            HEADERS_PLAYLIST['User-Agent'] = USERAGENT
            HEADERS_SEGMENT['User-Agent'] = USERAGENT
            
            cookies = connection(f'https://www.twitch.tv/{self.username}', self.proxy, HEADERS_GET, cookies=True)
            for c in cookies:
                if 'unique_id' in c.name:
                    unique_id = c.value

            HEADERS['Device-ID'] = unique_id

            with open('twitchdata/gqljson.json', 'r') as file:
                 j = file.read()

            j = j.replace("$username", self.username)
            html = connection("https://gql.twitch.tv/gql",
                              self.proxy, HEADERS, method="POST", data=j)
            
            j = json.loads(html)
            
            from random import randrange

            p = randrange(1000000, 9000000)
            play_session_id = str(uuid.uuid4().hex)

            token = urllib.parse.quote_plus(
                str(j["data"]["streamPlaybackAccessToken"]["value"]))
                        
            sig = j["data"]["streamPlaybackAccessToken"]["signature"]
                        
            html = connection(f"https://usher.ttvnw.net/api/channel/hls/{self.username}.m3u8?allow_source=true&fast_bread=true&p={p}&play_session_id={play_session_id}&player_backend=mediaplayer&playlist_include_framerate=true&reassignments_supported=true&sig={sig}&supported_codecs=avc1&token={token}&cdm=wv&player_version=1.14.0", self.proxy, HEADERS_PLAYLIST)
            for line in html.splitlines()[::-1]:
                if "https" in line and ".m3u8" in line:
                    playlist_url = line
                    break
                        
            loops_i = 0
            while True:
                if loops_i >= 1:
                    print(self.proxy.host, " downloading loop ", loops_i, " ", HEADERS['User-Agent'][:30], "...")
                if loops_i >= 8:
                    self.run()                    
                    
                loops_i += 1
                html = connection(playlist_url, self.proxy, HEADERS_PLAYLIST)
                if not '#EXT' in html:
                    print(self.proxy.host, " died ", html[:50])
                    break
                download_i = 1
                for line in html.splitlines()[::-1]:
                    if "https" in line:
                        if download_i >= 3:
                            break
                        url = f'https{line.split("https")[1]}'
                        html = connection(url, self.proxy, HEADERS_SEGMENT)
                        download_i += 1
        except Exception as e:
            print(str(e))
            pass