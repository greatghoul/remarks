# coding: utf-8
from flask import Flask, abort, request, redirect, render_template, \
                  url_for, send_from_directory, Response
import os
import sys
import re
import base64
import urlparse
from werkzeug.routing import BaseConverter
from remarks.models import Slideshow
from remarks.logger import logger

app = Flask(__name__, static_url_path='/_static')

root = os.path.dirname(__file__)
config = os.path.join(os.path.dirname(root), 'config.cfg')
app.config.from_pyfile(config, silent=True)

def theme_url(theme):
    if theme in ['default', 'dark', 'gdg']:
        filename = 'themes/%s/style.css' % theme
        return url_for('static', filename=filename)
    else:
        return theme

app.jinja_env.globals['theme_url'] = theme_url

class PubConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(PubConverter, self).__init__(url_map)
        self.regex = r'[^_][^\/]*'

app.url_map.converters['pub'] = PubConverter

@app.route('/')
def home():
    bookmarklet = render_template('bookmarklet.js').replace('\n', '');
    return render_template('index.html', bookmarklet=bookmarklet)

@app.route('/theme/<name>/<path:filename>')
def theme(name, filename):
    theme_dir = os.path.join(instance_path, 'themes', name)
    logger.info('Theme file: %s/%s', theme_dir, filename)
    return send_from_directory(theme_dir, filename)

def _render_asset(slide, filename):
    name = filename.lower()
    if name.endswith('.css'):
        content = slide.file_content(filename)
        return Response(content, mimetype='text/css')
    elif name.endswith('.js'):
        content = slide.file_content(filename)
        return Response(content, mimetype='text/javascript')
    else:
        return redirect(slide.file_url(filename))

def _render_slide(slide, filename):
    if filename:
        return _render_asset(slide, filename)
    else:
        return render_template('slideshow.html', slide=slide)

@app.route('/gist/<gist_id>/', methods=['GET'])
@app.route('/gist/<gist_id>/<filename>', methods=['GET'])
def gist(gist_id, filename=None):
    slide = Slideshow.gist(gist_id)
    return _render_slide(slide, filename)

@app.route('/<pub:user>/<slug>/', methods=['GET'])
@app.route('/<pub:user>/<slug>/<path:filename>', methods=['GET'])
def repo(user, slug, filename=None):
    slide = Slideshow.repo(user, slug)
    return _render_slide(slide, filename)


def _repo_asset(user, slug, filename):
    return 'https://raw.github.com/%s/%s/%s/%s/%s' % (user, 'slides', 'master', slug, filename)