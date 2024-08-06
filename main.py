import requests
import re
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

with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

@app.route('/')
def get_index():
    host = request.headers['Host']
    if host in config['Domains'].keys():
        target = config['Domains'][host]
        url = 'https://' + target + '/'
    else:
        return redirect('https://www.google.com')
    myReq = requests.get(url, headers=headers)
    soup = BeautifulSoup(myReq.content.decode(), "html.parser")
    old_links = soup.findAll("a", href=True)
    targetRegex = '^https?://' + target.replace(".", "\\.")
    print(targetRegex)
    for a in old_links:
        if re.search(targetRegex, a['href']):
            path = a['href'].split('/')[3:]
            a['href'] = 'https://' + request.headers['Host'] + '/' + '/'.join(path)
    return soup.prettify()

@app.route('/<path:pars>')
def get_path(pars):
    host = request.headers['Host']
    if host in config['Domains'].keys():
        target = config['Domains'][host]
        baseUrl = 'https://' + target + '/'
    else:
        return redirect('https://www.google.com/')
    url = baseUrl + pars
    myReq = requests.get(url, headers=headers)
    if 'favicon' in myReq.url:
        return myReq.content
    soup = BeautifulSoup(myReq.content.decode(), "html.parser")
    old_links = soup.findAll("a", href=True)
    targetRegex = '^https?://' + target.replace(".", "\\.")
    for a in old_links:
        if re.search(targetRegex, a['href']):
            path = a['href'].split('/')[3:]
            a['href'] = 'https://' + request.headers['Host'] + '/' + '/'.join(path)
    return soup.prettify()

def main():
    app.run(host='127.0.0.1', port=8000)

main()