#!/usr/bin/env python
# -*- encoding: utf-8

from gevent import monkey; monkey.patch_all()

import base64
import datetime
import json
import os
import textwrap
from urllib.parse import parse_qsl, urlparse

from flask import Flask, Response, abort, request
from peewee import (
    CharField, DateTimeField, Model, SqliteDatabase, TextField
)


# 1 pixel GIF, base64-encoded.
BEACON = base64.b64decode(
    'R0lGODlhAQABAIAAANvf7wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=='
)

# Store the database file in the working directory.
DATABASE_NAME = os.path.join(os.curdir, 'analytics.db')
DOMAIN = 'https://alexwlchan.net/analytics'

# Simple JavaScript which will be included and executed on the client-side.
JAVASCRIPT = textwrap.dedent("""(function(){
    var d=document,i=new Image,e=encodeURIComponent;
    i.src='%s/a.gif?url='+e(d.location.href)+'&ref='+e(d.referrer)+'&t='+e(d.title);
    })()""".replace('\n', ''))

# Flask application settings.
DEBUG = bool(os.environ.get('DEBUG'))
SECRET_KEY = os.environ.get('SECRET_KEY')

app = Flask(__name__)
app.config.from_object(__name__)

database = SqliteDatabase(DATABASE_NAME)


class JSONField(TextField):
    """Store JSON data in a TextField."""
    def python_value(self, value):
        if value is not None:
            return json.loads(value)

    def db_value(self, value):
        if value is not None:
            return json.dumps(value)


class PageView(Model):
    domain = CharField()
    url = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now, index=True)
    title = TextField(default='')
    ip = CharField(default='')
    referrer = TextField(default='')
    headers = JSONField()
    params = JSONField()

    class Meta:
        database = database

    @classmethod
    def create_from_request(cls):
        parsed = urlparse(request.args['url'])
        params = dict(parse_qsl(parsed.query))

        return PageView.create(
            domain=parsed.netloc,
            url=parsed.path,
            title=request.args.get('t') or '',
            ip=request.headers.get('X-Forwarded-For', request.remote_addr),
            referrer=request.args.get('ref') or '',
            headers=dict(request.headers),
            params=params)


@app.route('/a.gif')
def analyze():
    if not request.args.get('url'):
        abort(404)

    with database.transaction():
        PageView.create_from_request()

    response = Response(app.config['BEACON'], mimetype='image/gif')
    response.headers['Cache-Control'] = 'private, no-cache'
    return response


@app.route('/a.js')
def script():
    return Response(
        app.config['JAVASCRIPT'] % (app.config['DOMAIN']),
        mimetype='text/javascript')


@app.errorhandler(404)
def not_found(e):
    return Response('Not found.')


if __name__ == '__main__':
    database.create_tables([PageView], safe=True)
    from gevent.wsgi import WSGIServer
    WSGIServer(('', 5000), app).serve_forever()
    database.close()
