__author__ = 'Christian'
# a mini server whose sole purpose is to count url submissions

from bottle import run, route, post, request, default_app
import os
import funcs

@post("/submit/")
def hit():
    try:
        funcs.insert_url(request.remote_addr, "http://%s" % request.forms.get("url"))
    except funcs.SpamProtectionStop:
        pass
    return  u'ok'

@route("/")
def index():
    return u'nothing to see here (yet)'

run(host='localhost', server='gunicorn', port=os.environ.get('PORT', 5000))
