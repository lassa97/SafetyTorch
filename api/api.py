from wrapper import Wrapper
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import base64
import iptools
import urllib.parse

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@api.get("/")
async def root():
    return {"ip": "Hello world", "blocked": False}

@api.get("/check/{resource}")
async def check_resource(resource):
    url, base_url = parse_url(resource)

    is_address = iptools.ipv4.validate_ip(base_url)

    if is_address:
        details = Wrapper.check_ip(base_url)
    else:
        details = Wrapper.check_domain(base_url)

    print(base_url)
    print(details)

    return {"resource": base_url, "blocked": details[0], "blocklist": details[1], "category": details[2]}

    # base_url = url.split('/')[2]
    #return {"url": url, "ip": iptools.ipv4.validate_ip(url)}

@api.get("/check/ip/{ip}")
async def check_ip(ip):
    details = Wrapper.check_ip(ip)
    return {"ip": ip, "blocked": details[0], "blocklist": details[1], "category": details[2]}

@api.get("/check/domain/{domain}")
async def check_domain(domain):
    details = Wrapper.check_domain(domain)
    return {"domain": domain, "blocked": details[0], "blocklist": details[1], "category": details[2]}

def decode_url(resource):
    url = base64.b64decode(urllib.parse.unquote(resource)).decode('utf-8')
    return url

def parse_url(resource):
    url = decode_url(resource)
    base_url = url.split('/')[2]
    # url = decode_url(resource).decode('utf-8')
    # url = url.split('/')[-1]
    # url = decode_url(url).decode('utf-8')
    return url, base_url