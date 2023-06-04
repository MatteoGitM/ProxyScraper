import time
import Settings

from dataclasses import dataclass, field
from typing import List, Optional

@dataclass(eq=True)
class Proxy:
    host: str
    port: str
    type: str
    iselite: Optional[bool] = False
    istrasp: Optional[bool] = False
    hsts: Optional[bool] = True
    spamhaus: Optional[str] = 'N/A'
    country: Optional[str] = 'N/A'
    last_tested: Optional[str] = None
    first_tested: Optional[str] = None
    uptime: Optional[int] = 0
    alive: Optional[bool] = True
    validators: Optional[List] = field(default_factory=list)

    
    def __str__(self):
        return f"{self.host}:{self.port}"
    
    def __eq__(self, other):
        if type(other) is type(self):
            return self.__hash__() == other.__hash__()
        else:
            return False
        
    def __hash__(self):
        if Settings.MULTI_PORT:
            return hash(f"{self.host}:{self.port}")
        return hash(self.host)
    
@dataclass
class ProxyInventory:
    proxies: List[Proxy] = field(default_factory=list)
    recently_tested = []
    tested_count = 0
    
    def add(self, proxy):
        #if not f"host='{proxy.host}', port='{proxy.port}'" in str(self):
        self.proxies.append(Proxy(proxy.host, proxy.port, proxy.type))
      
    def remove(self, prxy: str):
        for p in self.proxies:
            if prxy in str(p):
                print(p, "removed from inventory")
                self.proxies.remove(p)
    
    def get_proxy(self):
        for proxy in self.proxies:
            if proxy.type == "uknown":
                proxy.type = "testing"
                self.tested_count += 1
                return proxy
    
    def get_proxy_alive(self):
        for proxy in self.proxies:
            if not proxy.alive: continue
            if not proxy.last_tested: continue          
            if str(proxy) in self.recently_tested: continue
            self.recently_tested.append(str(proxy))
            timestamp = int(time.time() - proxy.last_tested)            
            if timestamp > Settings.UPTIME_TIMESTAMP:
                return proxy
            
        self.recently_tested = []
        return None
    
    
    def count_alives(self):
        i = 0
        for p in self.proxies:
            if p.uptime >= 1:
                i +=1
        return i
    
    def count_elites(self):
        i = 0
        for p in self.proxies:
            if p.iselite:
                i +=1
        return i
    
    def count_anons(self):
        i = 0
        for p in self.proxies:
            if p.last_tested:
                if p.alive and not p.istrasp and not p.iselite:
                    i +=1
        return i
    
    def count_trasps(self):
        i = 0
        for p in self.proxies:
            if p.istrasp:
                i +=1
        return i
    
    def export_list(self):
        result = []
        for p in self.proxies:
            if p.last_tested:
                if p.alive and not p.istrasp:
                    result.append(str(p))
        return '\r\n'.join(result)
    
    def __str__(self):
        return str(self.proxies)
        #return ','.join(str(Proxy) for Proxy in self.proxies)
    
    def __len__(self):
        return len(self.proxies)
    
    def __getitem__(self, i):
         return self.proxies[i]
     
        