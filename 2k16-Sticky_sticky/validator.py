from cgi import parse_qsl, FieldStorage
from wsgiref.simple_server import make_server
import os
from random import randint
import json

BACKEND={}

def application(environ, start_response):
    """Main WSGI entry point"""
    value = ""
    msg = ""
    url = environ['PATH_INFO'].split('/')[1:]
    sess_id = url[-1]
    user = {}
    if environ['REQUEST_METHOD'] == 'GET':
        username = BACKEND.get(sess_id, "")
        user = {}
        if username:
            user = {"name": username, "admin": 0}

    elif environ['REQUEST_METHOD'] == 'POST':
        post_env = environ.copy()
        post_env['QUERY_STRING'] = ''
        fields = FieldStorage(fp=environ['wsgi.input'], environ=post_env, keep_blank_values=1)
        name = ""
        if 'name' in fields:
            name = fields['name'].value

        if name:
            BACKEND.update({sess_id: name})
            user = {"name": name, "admin": 0}

    ret = '200 OK'
    ctype = 'text/plain'
    content = json.dumps(user)
    headers = []

    start_response(ret, [('Content-Type', ctype)]+headers)
    return content

if __name__=='__main__':
    httpd = make_server('', 8080, application)
    print("Serving on port 8080...")
    httpd.serve_forever()
