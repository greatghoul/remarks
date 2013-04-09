# coding: utf-8
from flask import Flask, abort, request, redirect, render_template, url_for
from log import log
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

    return render_template('index.html', gist_id=gist_id)


def _gist_slides(gist):
    slides = dict(title=u'Remarks Slides')
    content = gist.get('files', {}).get('slides.md', {}).get('content', '')
    for line in re.sub(r'\s*^---.*$[\s\S]*', '', content, flags=re.M).split('\n'):
        key, val = re.split(r':\s*', line, maxsplit=1)
        slides[key] = val
    slides['content'] = content
    return slides

@app.route('/gist/<gist_id>/', methods=['GET'])
@app.route('/gist/<gist_id>/<filename>', methods=['GET'])
def gist_file(gist_id, filename='slides.md'):
    try:
        log.info('Fetching gist %s content: %s', gist_id, filename)
        gist = gh.gists(gist_id).get()
        if 'raw' not in request.args and filename == 'slides.md':
            slides = _gist_slides(gist)
            return render_template('slideshow.html', slides=slides)
        else:
            if request.args.get('raw') == '1':
                return '<pre>' + gist.get('files', {}).get('slides.md', {}).get('content', '') + '</pre>'
            else:
                raw_url = gist.get('files', {}).get(filename, {}).get('raw_url')
                log.info('  Raw url: %s', raw_url)
                return redirect(raw_url)

    except ApiNotFoundError, e:
        log.error(e.response)
    except ApiError, e:
        log.error(e.response)
    except Exception, e:
        log.error(e)

    return abort(404)


def _repo_slides(repo):
    slides = dict(title=u'Remarks Slides')
    content = base64.b64decode(repo.get('content', '')).decode('utf-8')
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
        repo = gh.repos(owner)(repo).contents(path + '/' + filename).get(ref=branch)
        if 'raw' not in request.args and filename == 'slides.md':
            slides = _repo_slides(repo)
            return render_template('slideshow.html', slides=slides)
        else:
            if request.args.get('raw') == '1':
                return base64.b64decode(repo.get('content', '')).decode('utf-8')
            else:
                return redirect(_repo_attach(owner, repo, branch, path, filename))

    except ApiNotFoundError, e:
        log.error(e.response)
    except ApiError, e:
        log.error(e.response)
    except Exception, e:
        log.error(e)

    return abort(404)

