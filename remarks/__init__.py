# coding: utf-8
from flask import Flask, abort, request, redirect, render_template, \
                  url_for, send_from_directory, Response
from log import log
import os
import sys
import re
import base64
import urlparse
from remarks.helpers.slide_helper import source_info
from remarks.models import Slideshow
from remarks.logger import logger

app = Flask(__name__)

root = os.path.dirname(os.path.dirname(__file__))
app.config.from_pyfile(os.path.join(root, 'config.cfg'), silent=True)

@app.route('/')
def home():
    bookmarklet = render_template('bookmarklet.js').replace('\n', '');
    return render_template('index.html', bookmarklet=bookmarklet)

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file(os.path.join(root, 'remarks', 'favicon.ico'))

@app.route('/theme/<name>/<path:filename>')
def theme(name, filename):
    theme_dir = os.path.join(instance_path, 'themes', name)
    log.info('Theme file: %s/%s', theme_dir, filename)
    return send_from_directory(theme_dir, filename)

@app.route('/<path:path>', methods=['GET'])
@app.route('/<path:path>/', methods=['GET'])
def slideshow(path):
    if request.referrer:
        refer = urlparse.urlparse(request.referrer)
        logger.info('%s -> %s', refer.path, path)

    logger.info('%s -> %s', path, request.referrer)
    info = source_info(path)
    slide = Slideshow.load(info)
    return render_template('slideshow.html', slide=slide)
    

def _repo_attach(owner, repo, branch, path, filename):
    return 'https://raw.github.com/%s/%s/%s/%s/%s' % (owner, repo, branch, path, filename)