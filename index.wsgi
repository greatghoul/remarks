import sys
root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, 'lib'))

import sae
from remarks import app

application = sae.create_wsgi_app(app)