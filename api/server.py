from flask import Flask, jsonify, render_template
from utils import Cache, Checker, Utils

import iptools

cache = Cache()

app = Flask(__name__)

@app.route("/")
def root():
    """
    if cache.queried:
        cache.queried = False
        return render_template('index.html', url=cache.url, category=cache.category, link=cache.link, threat=cache.threat, blocklist=cache.blocklist)
    else:
        return render_template('error.html', code=404), 404
    """
    return render_template('index.html', url=cache.url, category=cache.category, link=cache.link, threat=cache.threat, blocklist=cache.blocklist)

@app.route("/check/<resource>")
def check_resource(resource):
    url, base_url = Utils.parse_url(resource)
    ip_address = iptools.ipv4.validate_ip(base_url)

    """
    Comprueba la dirección IP de un dominio, siempre que el nombre de dominio no se haya identificado antes
    if ip_address:
        details = Checker.check_ip(base_url)
    else:
        details = Checker.check_domain(base_url)
        if not details[0]: # details[0] == blocked
            base_url = Checker.get_ip(base_url)
            details = Checker.check_ip(base_url)
    """

    if ip_address:
        details = Checker.check_ip(base_url)
    else:
        details = Checker.check_domain(base_url)

    response = jsonify(
        {
            "resource": base_url,
            "blocked": details[0],
            "blocklist": details[1],
            "category": details[2],
            "safe_url": "http://127.0.0.1:5000/"
        }
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    cache.url = base_url
    cache.category = details[2]
    cache.link = "https://www.youtube.com/watch?v=kP4sVszgC_c&list=PLr5GsywSn9d8pUMODmSqxtJ27fGH6N4Z-&index=21"
    cache.threat = "adware"
    cache.blocklist = "Ads"
    cache.queried = True
    return response

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', code=404), 404