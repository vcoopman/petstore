''' Pet Microservice API '''

import hug
import pet # local module
from db import init_db

@hug.startup()
def start_api(api):
    ''' initial api process'''

    init_db()


@hug.get('/')
def hello():
    return "Hello from the Pet Microservice!!"


@hug.get('/pet/hello')
def pet_hello():
    ''' two-phase commit (2PC) '''

    # this could be bettter if it checks if db is working correctly!
    return { 'msg': 'hello!'}


router = hug.route.API(__name__)

router.get('/pet/search')(pet.filter_search)

router.get('/pet/available')(pet.is_available)

router.post('/pet/buy')(pet.buy)

router.post('/pet')(pet.add_pet)

router.get('/pet/{pet_id}')(pet.get_pet)

router.put('/pet/{pet_id}')(pet.update_pet)

router.delete('/pet/{pet_id}')(pet.delete_pet)
