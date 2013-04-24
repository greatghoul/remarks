# coding: utf-8
from flask import Flask, abort, request, redirect, render_template, \
                  url_for, send_from_directory, Response
from log import log
import os
import re
import base64
import urlparse
from github import GitHub, ApiError, ApiNotFoundError

instance_path = os.path.dirname(__file__)
app = Flask(__name__)
app.config.from_pyfile(os.path.join(instance_path, 'config.cfg'), silent=True)
gh = GitHub(client_id=app.config['CLIENT_ID'], client_secret=app.config['CLIENT_SECRET'])

@app.route('/')
def home():
    bookmarklet = render_template('bookmarklet.js').replace('\n', '');  
    return render_template('index.html', bookmarklet=bookmarklet)


@app.route('/theme/<name>/<path:filename>')
def theme(name, filename):
    theme_dir = os.path.join(instance_path, 'themes', name)
    log.info('Theme file: %s/%s', theme_dir, filename)
    return send_from_directory(theme_dir, filename)


def _gist_slides(gist):
    slides = dict(title=u'Remarks Slides', theme=url_for('theme', name='default', filename='style.css'))
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
            is_style = filename.lower().endswith('.css')
            if request.args.get('raw') == '1' or is_style:
                raw_content = gist.get('files', {}).get('slides.md', {}).get('content', '')
                if is_style:
                    return Response(raw_content, mimetype='text/css')
                else:
                    return raw_content
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
    slides = dict(title=u'Remarks Slides', theme=url_for('theme', name='default', filename='style.css'))
    content = base64.b64decode(repo.get('content', '')).decode('utf-8')
    for line in re.sub(r'\s*^---.*$[\s\S]*', '', content, flags=re.M).split('\n'):
        key, val = re.split(r':\s*', line, maxsplit=1)
        slides[key] = val
    slides['content'] = content
    return slides

def _repo_attach(owner, repo, branch, path, filename):
    return 'https://raw.github.com/%s/%s/%s/%s/%s' % (owner, repo, branch, path, filename)
    
@app.route('/repo/<owner>/<repo>/<path>/', methods=['GET'])
@app.route('/repo/<owner>/<repo>/<path>/<path:filename>', methods=['GET'])
def repo_file(owner, repo, path, filename='slides.md'):
    try:
        repo_resp = gh.repos(owner)(repo).contents(path + '/' + filename)

        if 'raw' not in request.args and filename == 'slides.md':
            branch = request.args.get('branch', 'master')
            log.info('Fetching slides(%s): /%s/%s/%s/%s', branch, owner, repo, path, filename)
            repo_resp = repo_resp.get(ref=branch)
            slides = _repo_slides(repo_resp)
            return render_template('slideshow.html', slides=slides)
        else:
            # Fix branch in attachments
            query = urlparse.urlparse(request.referrer).query
            branch = urlparse.parse_qs(query).get('branch', ['master'])[0]

            log.info('Fetching attach(%s): /%s/%s/%s/%s', branch, owner, repo, path, filename)
            log.info('  Referrer: %s', request.referrer)
            repo_resp = repo_resp.get(ref=branch)
            is_style = filename.lower().endswith('.css')
            if request.args.get('raw') == '1' or is_style:
                raw_content = base64.b64decode(repo_resp.get('content', '')).decode('utf-8')
                if is_style:
                    return Response(raw_content, mimetype='text/css')
                else:
                    return raw_content
            else:
                return redirect(_repo_attach(owner, repo, branch, path, filename))

    except ApiNotFoundError, e:
        log.error(e.response)
    except ApiError, e:
        log.error(e.response)
    except Exception, e:
        log.error(e)

    return abort(404)

