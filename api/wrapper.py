import dns.resolver
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

class Wrapper:
    def __init__(self) -> None:
        pass
    
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
    def check_url(url):
        blocked = False
        with open('blocklist.json', 'r') as file:
            blocklist = json.load(file)
            if url in blocklist.keys():
                blocked = True
                return (blocked, 'blocklist.json', blocklist.get(url))

        for blocklist in mail_url_blocklists:
            try:
                dns.resolver.resolve("{URL}.{BLOCKLIST}".format(URL=url, BLOCKLIST=blocklist), "A")
                blocked = True
                return (blocked, blocklist, 'spam')
            except dns.resolver.NXDOMAIN:
                continue
            except dns.resolver.NoAnswer:
                continue
        return (blocked, None, None)



# check_ip("127.0.0.2")

"""
import dns.resolver
try:
    dns.resolver.resolve("2.0.0.127.spamsources.fabel.dk", "A")
    print("Listed")
except dns.resolver.NXDOMAIN:
    print("Not listed")
"""