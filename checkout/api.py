import hug
import checkout # local module
from db import init_db # local module

@hug.startup()
def start_api(api):
    ''' initial api process'''

    init_db()

@hug.get('/')
def hello():
    return 'hello!'


# Add CORS
api = hug.API(__name__)
api.http.add_middleware(hug.middleware.CORSMiddleware(api))

router = hug.route.API(__name__)
router.post('/checkout')(checkout.checkout)
