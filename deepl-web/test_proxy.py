from proxy_requests import ProxyRequests
import pprint

r = ProxyRequests('https://www.whatismyip.com/')
pprint.pprint(r.get())

