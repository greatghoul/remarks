# coding: utf-8
from flask import Flask, abort, request, redirect, render_template, url_for
from log import log
import util
import os
import re
import base64
from github import GitHub, ApiError, ApiNotFoundError

app = Flask(__name__)
app.config.from_pyfile(os.path.join(os.path.dirname(__file__), 'config.cfg'), silent=True)
gh = GitHub()

@app.route('/')
def home():
    log.info('Fetching demo gist.')
    gist_id = '5123482'
    gist = gh.gists(gist_id).get()
    source = util.get_slides_source_from_gist(gist)

    return render_template('index.html', gist_id=gist_id, source=source)

@app.route('/gist/', methods=['GET'])
@app.route('/gist/<gist_id>/', methods=['GET'])
def play_gist(gist_id=None):
    # Fix url to a restful style.
    if gist_id is None:
        if 'gist_id' in request.args:
            return redirect(url_for('play_gist', gist_id=request.args['gist_id']))
        else:
            abort(404)
    else:
        log.info('Creating slides from gist: %s' % gist_id)
        gist = gh.gists(gist_id).get()
        if gist is None:
            abort(404)
        
        title = gist.get('description', 'Remarks')
        source = util.get_slides_source_from_gist(gist)
        return render_template('slideshow.html', title=title, source=source)

def _repo_slides(resp):
    slides = dict(title=u'Remarks Slides')
    content = base64.b64decode(resp.get('content', '')).decode('utf-8')
    for line in re.sub(r'\s*^---.*$[\s\S]*', '', content, flags=re.M).split('\n'):
        key, val = re.split(r':\s*', line, maxsplit=1)
        slides[key] = val
    slides['content'] = content
    return slides

def _repo_attach(owner, repo, branch, path, filename):
    return 'https://raw.github.com/%s/%s/%s/%s/%s' % (owner, repo, 'master', path, filename)
    
@app.route('/repo/<owner>/<repo>/<path>/', methods=['GET'])
@app.route('/repo/<owner>/<repo>/<path>/<path:filename>', methods=['GET'])
def repo_file(owner, repo, path, filename='slides.md'):
    try:
        branch = request.args.get('branch', 'master')
        log.info('%s/%s/%s/%s', owner, repo, path, filename)
        if filename == 'slides.md':
            resp = gh.repos(owner)(repo).contents(path + '/' + filename).get(ref=branch)
            slides = _repo_slides(resp)
            return render_template('slideshow.html', slides=slides)
        else:
            return redirect(_repo_attach(owner, repo, branch, path, filename))

    except ApiNotFoundError, e:
        log.error(e.response)
    except ApiError, e:
        log.error(e.response)
    except Exception, e:
        log.error(e)

    return abort(404)

