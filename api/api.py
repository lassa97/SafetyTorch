from unicodedata import category
from wrapper import Wrapper
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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

@api.get("/check/ip/{ip}")
async def check_ip(ip):
    details = Wrapper.check_ip(ip)
    return {"ip": ip, "blocked": details[0], "blocklist": details[1], "category": details[2]}

@api.get("/check/url/{url}")
async def check_url(url):
    details = Wrapper.check_url(url)
    return {"url": url, "blocked": details[0], "blocklist": details[1], "category": details[2]}