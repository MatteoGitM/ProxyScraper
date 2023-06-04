import eel
import json
import Settings


DEBUG = True
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0"
EZENV_URL = 'http://207.246.70.16/'
CERT_LOCATION = 'cacerts.pem'
MAX_RETRIES = 3
TIMEOUT = 10
VALIDATORS = {"https://www.twitch.tv": 'tw-root',
              "https://google.com": "Google"}
ELITE_TAGS = {"ACCPROXYWS", "Cdn-Src-Ip", "Client-IP", "client_ip", "CUDA_CLIIP", "Forwarded", "Forwarded-For",
              "REMOTE-HOST", "X-Client-Ip", "X-Coming-From", "X-Forwarded", "X-Forwarded-For", "X-Forwarded-For-IP",
              "X-Forwarded-Host", "X-Forwarded-Server", "X-Host", "X-Network-Info", "X-Nokia-RemoteSocket",
              "X-ProxyUser-IP", "X-QIHOO-IP", "X-Real-IP", "XCnool_forwarded_for", "XCnool_remote_addr",
              "Mt-Proxy-ID", "Proxy-agent", "Proxy-Connection", "Surrogate-Capability", "Via", "X-Accept-Encoding",
              "X-ARR-LOG-ID", "X-Authenticated-User", "X-BlueCoat-Via", "X-Cache", "X-CID-HASH", "X-Content-Opt",
              "X-D-Forwarder", "X-Fikker", "X-Forwarded-Port", "X-Forwarded-Proto", "X-IMForwards", "X-Loop-Control",
              "X-MATO-PARAM", "X-NAI-ID", "X-Nokia-Gateway-Id", "X-Nokia-LocalSocket", "X-Original-URL", "X-Proxy-ID",
              "X-Roaming", "x-teamsite-preremap", "X-Tinyproxy", "X-TurboPage", "X-Varnish", "X-Via", "X-WAP-Profile",
              "X-WrProxy-ID", "X-XFF-0", "Xroxy-Connection"}
HEADERS = {"User-Agent": USER_AGENT,
           "Accept-Encoding": "gzip, deflate",
           "Accept-Language": "en-US,en;q=0.9",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
           "Connection": "keep-alive"}
PROXY_LIST = {"https://buy.fineproxy.org/api/getproxy/?format=txt&type=socks_ip&login=USUWBZQVP&password=qMjNHvUg"}
THREADS_NUMBER = 250
UPTIME_TIMESTAMP = 30
SOCKS5_CHECK = True
SOCKS4_CHECK = True
HTTP_CHECK = True
AUTO_REMOVE = True
AUTO_EXPORT = True
MULTI_PORT = False

regex_string = r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b:\d{2,5}"
remote_ip = None
dbip = open('dbip.csv', 'rb', 0)

def serialize_sets(obj):
    if isinstance(obj, set):
        return list(obj)
    return obj

def save_settings(Settings):
    json_settings = {}
    for v in vars(Settings):
        if v.isupper():
            json_settings[v] = getattr(Settings, v)
    with open("settings.json", "w") as file:
        file.write(json.dumps(json_settings, default=serialize_sets, indent=4))

def load_settings():
    with open('settings.json', 'r') as file:
        json_settings = json.load(file)
    for s in json_settings:
        setattr(Settings, s, json_settings[s])

@eel.expose
def change_timeouts_setting(x):
    Settings.TIMEOUT = int(x)
    if DEBUG:
        print("[DEBUG] ", 'timeout seconds: ', x)

@eel.expose
def change_uptime_setting(x):
    Settings.UPTIME_TIMESTAMP = int(x)
    if DEBUG:
        print("[DEBUG] ", 'uptime: ', x)

@eel.expose
def max_retries_setting(x):
    Settings.MAX_RETRIES = int(x)
    if DEBUG:
        print("[DEBUG] ", 'max retries: ', x)

@eel.expose
def change_socks5_setting(x):
    Settings.SOCKS5_CHECK = x
    if DEBUG:
        print("[DEBUG] ", 'socks5 enabled: ', x)

@eel.expose
def change_socks4_setting(x):
    Settings.SOCKS4_CHECK = x
    if DEBUG:
        print("[DEBUG] ", 'socks4 enabled: ', x)

@eel.expose
def change_http_setting(x):
    Settings.HTTP_CHECK = x
    if DEBUG:
        print("[DEBUG] ", 'http proxy enabled: ', x)

@eel.expose
def change_remove_setting(x):
    Settings.AUTO_REMOVE = x
    if DEBUG:
        print("[DEBUG] ", 'auto remove proxies enabled: ', x)

@eel.expose
def multi_port_setting(x):
    Settings.MULTI_PORT = x
    if DEBUG:
        print("[DEBUG] ", 'multi-port: ', x)

@eel.expose
def change_export_setting(x):
    Settings.AUTO_EXPORT = x
    if DEBUG:
        print("[DEBUG] ", 'auto export enabled: ', x)

@eel.expose
def add_validator_setting(x, y):
    VALIDATORS.update({x: y})
    if DEBUG:
        print("[DEBUG] ", 'validators : ', ', '.join(list(VALIDATORS)))

@eel.expose
def remove_validator_setting(x):
    del VALIDATORS[x.split("\n")[0].replace(' ', '')]
    if DEBUG:
        print("[DEBUG] ", 'validators : ', ', '.join(list(VALIDATORS)))
