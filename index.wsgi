import sae

from main import app

application = sae.create_wsgi_app(app)
