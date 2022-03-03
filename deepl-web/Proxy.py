import requests


class Proxy(object):
    proxy_url = 'https://proxylist.geonode.com/api/proxy-list?limit=250&page=1&sort_by=lastChecked&sort_type=desc'
    proxy_data = []
    proxy_list = []

    def __init__(self):
        resp_http = requests.get(self.proxy_url)
        self.proxy_data.append(resp_http)
        self.append_all_to_list()

    def append_all_to_list(self):
        for proxy_data in self.proxy_data:
            for proxy in proxy_data.json()['data_to_translate']:
                if proxy['speed'] is None or proxy['speed'] > 2000:
                    continue
                protocol_var = proxy['protocols'][0]
                ip_var = proxy['ip']
                port_var = proxy['port']
                self.proxy_list.append({protocol_var: protocol_var + '://' + ip_var + ":" + port_var})

    def get_proxy(self, url_local):
        proxies = {}
        for proxy_data in self.proxy_data:
            for proxy in proxy_data.json()['data_to_translate']:
                protocol_var = proxy['protocols'][0]
                if proxy['speed'] is None or proxy['speed'] > 2000:
                    continue
                elif proxies[protocol_var] != "":
                    break
                ip_var = proxy['ip']
                port_var = proxy['port']
                url_local = protocol_var + '://' + ip_var + ":" + port_var
                try:
                    print({protocol_var: url_local})
                    response = requests.get(
                        url=url_local,
                        proxies={protocol_var: url_local},
                        timeout=15.0)
                    if response.status_code == 200:
                        proxies[protocol_var] = url_local
                except requests.exceptions.ConnectionError:
                    continue
        return proxies

    def generator_function(self) -> dict:
        for it in self.proxy_list:
            # yield says, just pause the function, just yield i
            # give i and when you tell me to keep going again, then i'll keep going
            yield it
