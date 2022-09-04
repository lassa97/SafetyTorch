import dns.resolver
import base64
import json

mail_ip_blocklists = [
    "spamsources.fabel.dk",
    "psbl.surriel.com",
    "rbl.schulte.org",
    "dnsbl.kempt.net",
    "bl.nordspam.com",
    "ix.dnsbl.manitu.de",
    "bl.spamcop.net",
    "truncate.gbudb.net",
    "dnsbl.zapbl.net"
]

mail_url_blocklists = [
    "dbl.nordspam.com",
    "rhsbl.zapbl.net"
]

class Utils:
    @staticmethod
    def parse_url(resource):
        url = base64.b64decode(resource).decode('utf-8')
        base_url = url.split('/')[2]
        return url, base_url

class Checker:
    @staticmethod
    def check_ip(ip):
        blocked = False
        for blocklist in mail_ip_blocklists:
            try:
                reverse_ip = '.'.join(ip.split('.')[::-1])
                dns.resolver.resolve("{IP}.{BLOCKLIST}".format(IP=reverse_ip, BLOCKLIST=blocklist), "A")
                blocked = True
                return (blocked, blocklist, 'spam')
            except dns.resolver.NXDOMAIN:
                continue
            except dns.resolver.NoAnswer:
                continue
        return (blocked, None, None)
    
    @staticmethod
    def check_domain(domain):
        blocked = False
        with open('blocklist.json', 'r') as file:
            blocklist = json.load(file)
            if domain in blocklist.keys():
                blocked = True
                return (blocked, 'blocklist.json', blocklist.get(domain))

        for blocklist in mail_url_blocklists:
            try:
                dns.resolver.resolve("{DOMAIN}.{BLOCKLIST}".format(DOMAIN=domain, BLOCKLIST=blocklist), "A")
                blocked = True
                return (blocked, blocklist, 'spam')
            except dns.resolver.NXDOMAIN:
                continue
            except dns.resolver.NoAnswer:
                continue
        return (blocked, None, None)

class Cache:
    def __init__(self):
        self.url = None
        self.category = None
        self.link = None
        self.threat = None
        self.blocklist = None
        self.queried = False

# check_ip("127.0.0.2")

"""
import dns.resolver
try:
    dns.resolver.resolve("2.0.0.127.spamsources.fabel.dk", "A")
    print("Listed")
except dns.resolver.NXDOMAIN:
    print("Not listed")
"""
