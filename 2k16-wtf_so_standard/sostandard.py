from cgi import parse_qsl, FieldStorage
from wsgiref.simple_server import make_server
import os
import jinja2
import json
import sqlite3

DB_PATH = "standard.db"
TPL_PATH = 'templates'
TPL_LOADER = jinja2.FileSystemLoader(searchpath=TPL_PATH)
TPL_ENV = jinja2.Environment(loader=TPL_LOADER )

def index(msg = ""):
    ret = '200 OK'
    ctype = 'text/html'
    tpl = TPL_ENV.get_template('/form.html.j2')
    tpl_data = {'msg': msg}
    content = tpl.render(tpl_data).encode('utf-8')
    return ret, ctype, content, []

def admin(data):
    ret = '200 OK'
    ctype = 'text/html'
    tpl = TPL_ENV.get_template('/admin.html.j2')
    content = tpl.render({'data': data}).encode('utf-8')
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
    if environ['REQUEST_METHOD'] == 'GET':
        url = environ['PATH_INFO'].split('/')[1:]
        ret, ctype, content, headers = index()
    elif environ['REQUEST_METHOD'] == 'POST':
        post_env = environ.copy()
        post_env['QUERY_STRING'] = ''
        fields = FieldStorage(fp=environ['wsgi.input'], environ=post_env, keep_blank_values=1)
        login = ""
        passwd = ""
        login = fields['login'].value
        passwd = fields['password'].value

        #open the db readonly
        fd = os.open(DB_PATH, os.O_RDONLY)
        conn = sqlite3.connect('/dev/fd/%d' % fd)
        c = conn.cursor()
        req = "SELECT * FROM users WHERE name='%s' and password='%s';" % (login, passwd)
        try:
            c.execute(req)
            user = c.fetchone()
        except:
            user = None
        if user:
            is_admin = user[3] == 1
            # Get all accessible data
            req = "SELECT * FROM items WHERE admin<=%i" % is_admin
            c.execute(req)
            data = c.fetchall()
            ret, ctype, content, headers = admin(data = data)
        else:
            ret, ctype, content, headers = index(msg="Bad login/password.")

        c.close()

    start_response(ret, [('Content-Type', ctype)]+headers)
    return content

if __name__=='__main__':
    httpd = make_server('', 8080, application)
    print("Serving on port 8080...")
    httpd.serve_forever()

