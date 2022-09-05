import dns.resolver
import base64
import json

class Utils:
    @staticmethod
    def parse_url(resource):
        url = base64.b64decode(resource).decode('utf-8')
        base_url = url.split('/')[2]
        return url, base_url

class Cache:
    def __init__(self):
        self.blocked = False
        self.url = None
        self.category = None
        self.link = None
        self.blocklist = None

class Checker:
    @staticmethod
    def check_ip(ip):
        blocked = False
        with open('resources.json', 'r') as file:
            links = json.load(file)

        with open('dnsbl.json', 'r') as file:
            dnsbl = json.load(file)

        for blocklist in dnsbl:
            try:
                reverse_ip = '.'.join(ip.split('.')[::-1])
                response = dns.resolver.resolve("{IP}.{BLOCKLIST}".format(IP=reverse_ip, BLOCKLIST=blocklist), "A")
                ip = response.response.answer[0].to_text().split('A')[1].split('\n')[0][1:]
                blocked = True
                return (blocked, blocklist, dnsbl.get(blocklist).get(ip), links.get(dnsbl.get(blocklist).get(ip)))
            except dns.resolver.NXDOMAIN:
                continue
            except dns.resolver.NoAnswer:
                continue
        return (blocked, None, None, None)
    
    @staticmethod
    def check_domain(domain):
        blocked = False
        with open('resources.json', 'r') as file:
            links = json.load(file)

        with open('blocklist.json', 'r') as file:
            blocklist = json.load(file)
            if domain in blocklist.keys():
                blocked = True
                return (blocked, 'blocklist.json', blocklist.get(domain), links.get(blocklist.get(domain)))

        with open('uridnsbl.json', 'r') as file:
            uridnsbl = json.load(file)            

        for blocklist in uridnsbl:
            try:
                response = dns.resolver.resolve("{DOMAIN}.{BLOCKLIST}".format(DOMAIN=domain, BLOCKLIST=blocklist), "A")
                blocked = True
                ip = response.response.answer[0].to_text().split('A')[1].split('\n')[0][1:]
                return (blocked, blocklist, uridnsbl.get(blocklist).get(ip), links.get(uridnsbl.get(blocklist).get(ip)))
            except dns.resolver.NXDOMAIN:
                continue
            except dns.resolver.NoAnswer:
                continue
        return (blocked, None, None)