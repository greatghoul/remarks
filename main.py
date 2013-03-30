# coding: utf-8
from flask import Flask, abort, request, redirect, render_template, url_for
from log import log
import util
import os
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

@app.route('/repo/<owner>/<repo>/<path:path>/', methods=['GET'])
def play_repo(owner, repo, path):
    print owner, repo, path
    try:
        print '--------' 
        content = gh.repos(owner)(repo).contents(path + 'slides.md').get()
        print 'END: --------' 
        print content
    except ApiNotFoundError, e:
        print e, e.request, e.response
    except ApiError, e:
        print e, e.request, e.response
    except Exception, e:
        print e
    # log.info(content)

    return ''

