import json
import requests
import backoff
import order_queue # local module (not 100% implemented)
from falcon import HTTP_404, HTTP_400, HTTP_503
from db import get_db # local module

# max exponential backoff retrie time
MAX_TIME = 20

## for order urls
ORDER_URL = 'http://petstoreorder.appspot.com/create/order'

## for pet urls
PET_URL = 'http://54.236.27.52:5000/pet/'

## for customer urls
def generate_customer_pay_url(customer_id, amount):
    customer_pay_url = f'http://petstorecustomer.appspot.com/pay/{amount}/by-customer-with-phone/{customer_id}'
    return customer_pay_url

def generate_customer_read_url(customer_id):
    customer_read_url = f'http://petstorecustomer.appspot.com/list/byphone/{customer_id}'
    return customer_read_url

## for shopping cart urls
# - creating and addings pets are out of the scope of checkout
def generate_sc_delete_url(cart_id):
    url = f'http://petstorecart.appspot.com/delete/cart/{cart_id}'
    return url

def generate_sc_read_url(cart_id):
    return f'http://petstorecart.appspot.com/list/pets/in/{cart_id}'


# def check_error(result, transaction_id):
#     ''' check if there is an error in result '''

#     if 'error' in result:
#         # update transaction status
#         update_transaction_status(transaction_id, 'fail')
#         return { 'error': result['error'] }

#     return None


@backoff.on_exception(backoff.expo, Exception, max_time=MAX_TIME) # retries for any Exception
def update_transaction_status(transaction_id, status):
    ''' updates a transaction status '''

    db = get_db()
    cur = db.cursor()
    sql = "UPDATE transaction_registry SET status = ? WHERE id = ?"
    cur.execute(sql, (status, transaction_id))
    db.commit()


@backoff.on_exception(backoff.expo, Exception, max_time=MAX_TIME)
def check_transaction(transaction_id):
    ''' check if transaction was is already in process/done, if not adds the transaction '''

    db = get_db()

    # check if transaction is already in process/done
    cur = db.cursor()
    sql = "SELECT * FROM transaction_registry WHERE id = ?"
    result = cur.execute(sql, (transaction_id, )).fetchone()

    if result is not None:
        return { 'error': "this transactions was already done" }

    # save transaction
    sql = "INSERT INTO transaction_registry (id, status) VALUES (?, ?)"
    cur.execute(sql, (transaction_id, 'processing'))
    db.commit()

    return { 'msg': "transaction registered" }


@backoff.on_exception(backoff.expo, Exception, max_time=MAX_TIME)
def sc_total_price(customer_id):
    ''' check if pets are available, if yes it calculates total price '''

    # 1. read customer shopping cart
    url = generate_sc_read_url(customer_id)
    shopping_cart = requests.get(url).json()

    # 2. get all pets
    pets = requests.get(PET_URL + 'search').json()
    pets = pets['result']


    # 3. check if there are enough pets, adding prices
    total_price = 0
    result_pets = [] # stores pets data from pet microservice

    for pet in shopping_cart:
        pet_species = pet['pet_species']

        for pet_data in pets:
            if pet_species == pet_data['pet_species']: # pet found

                if pet['pet_amount'] > pet_data['available']:
                    return { 'error': f"Not enough {pet_species}" }

                # add price
                print('price found for: ' + pet_species)
                total_price += pet_data['price']

                # save price
                pet['pet_price'] = pet_data['price']

                # store pets data
                pet_data['buy_amount'] = pet['pet_amount']
                result_pets.append(pet_data)
                break

    result = {
        'pets': result_pets,
        'shopping_cart': shopping_cart,
        'total_price': total_price
    }

    return result


@backoff.on_exception(backoff.expo, Exception, max_time=MAX_TIME)
def check_customer(customer_id, total_price):
    ''' check if customer has enough money to pay for items in shoppin cart '''

    url = generate_customer_read_url(customer_id)
    customer = requests.get(url).json()[0]

    if customer['credit'] < total_price:
        return { 'error': "Not enough credit" }

    return { 'msg': "Customer has enough credit", 'customer': customer }


@backoff.on_exception(backoff.expo, Exception, max_time=MAX_TIME)
def grab_pets(transaction_id, pets):
    ''' updates pets availabilty storage data '''

    for index,pet in enumerate(pets):

        data = {
            'transaction_id': transaction_id + f'_{index}',
            'pet_id': pet['pet_id'],
            'amount': pet['buy_amount']
        }

        response = requests.post(PET_URL + 'buy', data=data)

        if 'errors' in response:
            return { 'error': response['errors'] }

    return { 'msg': "Pets grabbed" }


@backoff.on_exception(backoff.expo, Exception, max_time=MAX_TIME)
def take_money(customer_id, total_price):
    ''' takes customer money '''

    url = generate_customer_pay_url(customer_id, total_price)
    response = requests.get(url)

    if response.status_code != 200:
        return { 'error': "Error charging money to customer!"}

    return { 'msg': 'total price charged' }


@backoff.on_exception(backoff.expo, Exception, max_time=MAX_TIME)
def clean_sc(customer_id):
    ''' deletes customer shopping cart, easy clean '''

    url = generate_sc_delete_url(customer_id)
    response = requests.get(url)

    if response.status_code != 200:
        return { 'error': "Error cleaning customer shopping cart!"}

    return { 'msg': "Customer shopping cart cleaned"}


@backoff.on_exception(backoff.expo, Exception, max_time=MAX_TIME)
def make_order(request_data):
    ''' makes an order '''

    customer = request_data['customer']
    data = {
        'address': customer['address'],
        'name': customer['name'],
        'phone': customer['phone'],
        'pets': request_data['shopping_cart']
    }

    response = requests.post(ORDER_URL, headers={ "Content-Type": "application/json" }, data=json.dumps(data))

    if response.status_code != 200:
        return { 'error': "Error creating order" }

    return { 'msg': "Order Created" }


@backoff.on_exception(backoff.expo, Exception, max_time=MAX_TIME)
def restore_amount_of_pets(request_data):
    ''' restore the amount of pets, in case of failure '''

    for pet in request_data['pets']:
        pet_id = pet['pet_id']

        # if this fails, i guess we cry.
        requests.put(PET_URL + f'{pet_id}', data={ 'available': pet['available'] })


@backoff.on_exception(backoff.expo, Exception, max_time=MAX_TIME)
def restore_customer_credit(request_data):
    ''' restores credits to customer, in case of failure '''

    ## THIS IS NOT IMPLEMENTED DUE TO API NOT BEING WELL DESCRIBED ENOUGH
    ## (i don't know how to use it, and don't wanna know)


def checkout(response, transaction_id:str, customer_id:str): # customer_id == customer_phone
    '''
        Main process of the checkout operation.

        Part 1:
            This part is done first.
            It involves the actions that don't affect storaged data.
            In case of failure, it will try to fail as soon as posible, focusing on saving time.
            After failure is does inform the user that the system has experience some dificulties.

        Part 2:
            It involves the actions that affect storaged data.
            In case of failure, it will try to undo the changes.
            It informes that there is failure.
            This approach focus on saving time. better to fail fast.

        Part 3:
            queue up the Order creation for later async processing. (Eventual Consistency)
            It informs the user that the payment is done, and that the order will be asap.
            This approach focus more on UX.

    '''

    ### == PART 1 == ###

    # check if valid transaction
    result = check_transaction(transaction_id)

    if 'error' in result:
        update_transaction_status(transaction_id, 'fail')
        response.status = HTTP_400
        return { 'error': result['error'] }

    # get shopping cart total price (+ pet availability check)
    result = sc_total_price(customer_id)

    if 'error' in result:
        update_transaction_status(transaction_id, 'fail')
        response.status = HTTP_400
        return { 'error': result['error'] }

    # keep useful data 4 later processing
    request_data = result
    print('total price for checkout: ', request_data['total_price'])

    # check if customer has enough money
    result = check_customer(customer_id, request_data['total_price'])

    if 'error' in result:
        update_transaction_status(transaction_id, 'fail')
        response.status = HTTP_400
        return { 'error': result['error'] }

    # keep useful data 4 later processing
    request_data['customer'] = result['customer']

    ### == PART 2 == ###

    # buy pet/s in shopping cart
    result = grab_pets(transaction_id, request_data['pets'])

    if 'error' in result:
        update_transaction_status(transaction_id, 'fail')
        response.status = HTTP_400
        return { 'error': result['error'] }

    result = take_money(customer_id, request_data['total_price'])

    if 'error' in result:
        # restore critical data
        restore_amount_of_pets(request_data)

        update_transaction_status(transaction_id, 'fail')
        response.status = HTTP_400
        return { 'error': result['error'] }

    # clear customer shopping cart
    result = clean_sc(customer_id)

    if 'error' in result:
        # restore critical data
        restore_amount_of_pets(request_data)
        restore_customer_credit(request_data)

        update_transaction_status(transaction_id, 'fail')
        response.status = HTTP_400
        return { 'error': result['error'] }

    ### == PART 3 == ###

    # make an order
    result = make_order(request_data)

    if 'error' in result:
        update_transaction_status(transaction_id, 'queued')

        response.status = HTTP_400
        return { 'error': result['error'] }

    # tell client
    update_transaction_status(transaction_id, 'success')
    return { 'msg': "Checkout Done!" }


    ## TO DO:
    ## implementar queue para order
