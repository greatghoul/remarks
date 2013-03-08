# coding: utf-8
from flask import Flask, request, render_template
from log import log
import util

app = Flask(__name__)
app.debug = True # Always enable debug mode

@app.route('/')
def home():
    log.info('Access home page')
    return render_template('index.html')

@app.route('/preview/', methods=['GET'])
def preview():
    source = request.args['source']
    log.info('Creating slides from gist: %s' % source)
    slides_source = util.get_slides_source(source)
    return render_template('preview.html', slides_source=slides_source)
