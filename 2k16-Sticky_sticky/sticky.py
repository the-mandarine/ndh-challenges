from cgi import parse_qsl, FieldStorage
from wsgiref.simple_server import make_server
import os
import jinja2
from socket import inet_aton, inet_ntoa
from base64 import b32encode, b32decode
import dns.resolver
from random import randint
from Cookie import SimpleCookie
import json
import requests

FLAG="ndh2k16_the-flag-goes-here"
TPL_PATH = 'templates'
TPL_LOADER = jinja2.FileSystemLoader(searchpath=TPL_PATH)
TPL_ENV = jinja2.Environment(loader=TPL_LOADER )
COOKIE_NAME = "user_id"
DEFAULT_DNS = "8.8.8.8"
#DEFAULT_WWW = "sessionvalidator.ndh"
DEFAULT_WWW = "admin.us-robotics.net"
DEFAULT_PORT = "8888"
DNS = b32encode(inet_aton(DEFAULT_DNS))

def index(msg = "", user=""):
    ret = '200 OK'
    ctype = 'text/html'
    tpl = TPL_ENV.get_template('/form.html.j2')
    tpl_data = {'msg': msg, 'user': user}
    content = tpl.render(tpl_data).encode('utf-8')
    return ret, ctype, content, []

def redirect(url):
    ret = "302 Temporary Redirect"
    ctype = "text/plain"
    headers = [("Location", url)]
    content = ""
    return ret, ctype, content, headers

def application(environ, start_response):
    """Main WSGI entry point"""
    value = ""
    msg = ""

    if 'HTTP_COOKIE' in environ:
        cookie = SimpleCookie(environ['HTTP_COOKIE'])
    else:
        cookie = SimpleCookie()
    sess_id = str(randint(100000, 900000))
    validator = DEFAULT_WWW
    resolver = DNS
    dns_server = DEFAULT_DNS
    if "user_id" in cookie:
        sess_id = cookie['user_id'].value
    if "validator" in cookie:
        if cookie['validator'].value != DEFAULT_WWW:
            msg = "ERROR: Validator has been hijacked. Used default: %s:%s." % (DEFAULT_WWW, DEFAULT_PORT)
        else:
            validator = cookie['validator'].value

    if "resolution" in cookie:
        try:
            dns_server = inet_ntoa(b32decode(cookie['resolution'].value))
        except TypeError:
            msg = "ERROR: Invalid resolver. Used default: %s." % (DNS)
        else:
            resolver = cookie['resolution'].value

    c_user_id = SimpleCookie()
    c_user_id['user_id'] = sess_id
    c_validator = SimpleCookie()
    c_validator['validator'] = validator
    c_resolution = SimpleCookie()
    c_resolution['resolution'] = resolver

    cookieheaders = []
    cookieheaders.append(('Set-Cookie', c_user_id.output(header='')+'; httponly'))
    cookieheaders.append(('Set-Cookie', c_validator.output(header='')+'; httponly'))
    cookieheaders.append(('Set-Cookie', c_resolution.output(header='', attrs=["httponly"])+'; httponly'))


    user = {}
    # Resolve backend
    q_res = dns.resolver.Resolver()
    q_res.nameservers = [dns_server]
    val_host = "127.0.0.1"
    try:
        a_res = q_res.query(validator)
        b_res = a_res.response.answer[-1]
        c_res = b_res.items[-1]
        val_host = c_res.address.encode()
    except:
        msg="ERROR: Wrong DNS resolution for %s from %s." % (validator, dns_server)

    if environ['REQUEST_METHOD'] == 'POST':
        post_env = environ.copy()
        post_env['QUERY_STRING'] = ''
        fields = FieldStorage(fp=environ['wsgi.input'], environ=post_env, keep_blank_values=1)
        name = ""
        if 'name' in fields:
            name = fields['name'].value

        headers = {'Host': validator}
        try:
            requests.post('http://%s:%s/%s' % (val_host, DEFAULT_PORT, sess_id), headers=headers, data={'name': name}, timeout=2)
        except:
            msg = "ERROR: validator %s:%s does not answer rightly." % (val_host, DEFAULT_PORT)

    headers = {'Host': validator, 'Flag': FLAG}
    try:
        user_json = requests.get('http://%s:%s/%s' % (val_host, DEFAULT_PORT, sess_id), headers=headers, timeout=2).text
        user = json.loads(user_json)
    except:
        msg = "ERROR: validator %s:%s does not answer rightly." % (val_host, DEFAULT_PORT)

    username = user.get('name', "")
    ret, ctype, content, headers = index(msg, username)
    start_response(ret, [('Content-Type', ctype)]+headers+cookieheaders)
    return content

if __name__=='__main__':
    httpd = make_server('', 8080, application)
    print("Serving on port 8080...")
    httpd.serve_forever()
