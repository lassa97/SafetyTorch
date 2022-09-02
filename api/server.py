from flask import Flask, jsonify, redirect, render_template
from utils import Checker, Utils

import iptools

app = Flask(__name__)

@app.route("/check/<resource>")
def check_resource(resource):
    url, base_url = Utils.parse_url(resource)
    ip_address = iptools.ipv4.validate_ip(base_url)

    if ip_address:
        details = Checker.check_ip(base_url)
    else:
        details = Checker.check_domain(base_url)

    response = jsonify(
        {
            "resource": base_url,
            "blocked": details[0],
            "blocklist": details[1],
            "category": details[2]
        }
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response