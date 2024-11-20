'''Module for camoflauging your (probably malicious) domains as other domains. '''

import re
import sys
import os.path

import requests
import yaml

from flask  import Flask, request, redirect
from bs4 import BeautifulSoup
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
# Add in a fix for possible proxy stuff. In case you decide to run this behind nginx or something.
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_for=1, x_host=1, x_prefix=1)

# Set a user agent that isn't python requests since that gets blocked some times.
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

try:
    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1], 'r', encoding='UTF-8') as f:
            config = yaml.safe_load(f)
    else:
        sys.exit("Config file not found.")
except:
    if os.path.isfile('config.yml'):
        with open('config.yml', 'r', encoding='UTF-8') as f:
            config = yaml.safe_load(f)
    else:
        sys.exit("Config file not found.")

@app.route('/')
def get_index():
    '''Index of flask application.'''
    host = request.headers['Host']
    if host in config['Domains'].keys():
        target = config['Domains'][host]
        url = 'https://' + target + '/'
    else:
        return redirect('https://www.google.com')
    my_req = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(my_req.content.decode(), "html.parser")
    old_links = soup.findAll("a", href=True)
    target_regex = '^https?://' + target.replace(".", "\\.")
    print(target_regex)
    for a in old_links:
        if re.search(target_regex, a['href']):
            path = a['href'].split('/')[3:]
            a['href'] = 'https://' + request.headers['Host'] + '/' + '/'.join(path)
    return soup.prettify()

@app.route('/<path:pars>')
def get_path(pars):
    '''This is to properly process URLs of any length.'''
    host = request.headers['Host']
    if host in config['Domains'].keys():
        target = config['Domains'][host]
        base_url = 'https://' + target + '/'
    else:
        return redirect('https://www.google.com/')
    url = base_url + pars
    my_req = requests.get(url, headers=headers, timeout=10)
    if 'favicon' in my_req.url:
        return my_req.content
    soup = BeautifulSoup(my_req.content.decode(), "html.parser")
    old_links = soup.findAll("a", href=True)
    target_regex = '^https?://' + target.replace(".", "\\.")
    for a in old_links:
        if re.search(target_regex, a['href']):
            path = a['href'].split('/')[3:]
            a['href'] = 'https://' + request.headers['Host'] + '/' + '/'.join(path)
    return soup.prettify()

def Tarnung():
    '''Main function to do the magic.'''
    app.run(host=config['Listener']['listenIP'], port=config['Listener']['port'])
