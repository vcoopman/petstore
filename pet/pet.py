"""
    Pet microservice
    Created on Monday June 24 12:34:00 2021

    @author: vcoopman
"""

from db import get_db
from falcon import HTTP_404, HTTP_400, HTTP_503

def filter_search(pet_family:str=None, pet_species:str=None, available:bool=None):
    ''' search pets using filters '''

    db = get_db()
    # get all pets
    with db:
        with db.cursor() as cur:
            sql = "SELECT * FROM pet"
            cur.execute(sql)

            result = cur.fetchall()

    # if no filters
    if not available and not pet_species and not pet_family:
        return { 'result': result }

    # filter pets
    for pet in result:
        if pet_family and pet['pet_family'] != pet_family:
            result.remove(pet)
            continue

        if pet_species and pet['pet_species'] != pet_species:
            result.remove(pet)
            continue

        if available and pet['available'] <= 0:
            result.remove(pet)
            continue

    return { 'result': result }


def get_pet(response, pet_id: int):
    ''' returns a specific pet's information '''

    db = get_db()
    with db:
        with db.cursor() as cur:
            sql = "SELECT * FROM pet WHERE pet_id = %s"
            cur.execute(sql, (pet_id , ))
            result = cur.fetchone()

            if not result:
                response.status = HTTP_404
                return { 'errors': "Pet not found" }

            return { 'pet': result }


def add_pet(
    pet_family:str,
    pet_species:str,
    price:int,
    available:int,

    age:int=None,
    color:str=None,
    diet:str=None,
    comment:str=None,
    size:str=None,
    weight:int=None,

    body=None # hug response body
    ):
    ''' adds a pet to the store '''

    db = get_db()
    with db:
        with db.cursor() as cur:
            sql = '''INSERT INTO pet(
                                pet_family, 
                                pet_species,
                                age, 
                                size, 
                                weight, 
                                color, 
                                diet, 
                                comment, 
                                price, 
                                available) 
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''


            cur.execute(sql, (
                            pet_family,
                            pet_species,
                            age,
                            size,
                            weight,
                            color,
                            diet,
                            comment,
                            price,
                            available)
            )

            # save pet_id
            body['pet_id'] = cur.lastrowid

            db.commit()

    return { 'pet': body }


def update_pet(response, pet_id: int, body):
    ''' updates a pet information '''

    def generate_update_sql(pet_id, body):
        ''' generates a update sql query from request body parameters '''

        sql = "UPDATE pet SET"

        # add parameters and values
        for key in body.keys():
            if isinstance(body[key], str):
                sql = f"{sql} {key}='{body[key]}',"

            else:
                sql = f"{sql} {key}={body[key]},"

        # remove ending comma
        sql = sql[:-1]

        # add WHERE clause
        sql = f"{sql} WHERE pet_id={pet_id};"

        return sql

    sql = generate_update_sql(pet_id, body)

    db = get_db()
    with db:
        with db.cursor() as cur:
            row_count = cur.execute(sql)

        db.commit()

    if row_count == 0:
        response.status = HTTP_404
        return { 'errors': "Pet not found" }

    return { 'status': 'Updated!' }


def delete_pet(response, pet_id: int):
    ''' deletes a pet '''

    sql = "DELETE FROM pet WHERE pet_id=%s;"

    db = get_db()
    with db:
        with db.cursor() as cur:
            row_count = cur.execute(sql, (pet_id, ))

        db.commit()

    if row_count == 0:
        response.status = HTTP_404
        return { 'errors': "Pet not found" }

    return { 'status': 'Deleted!' }


def is_available(response, pet_id: int, amount:int=1):
    ''' checks if there is enough pets, pets >= amount '''

    result = get_pet(response, pet_id)

    # check if errors
    if 'errors' in result:
        response.status = HTTP_404
        return { 'errors': result['errors'] }

    pet = result['pet']

    # check if enough pets
    if pet['available'] >= amount:
        return { 'available': True }

    return { 'available': False }


def buy(response, transaction_id:str ,pet_id: int, amount:int=1):
    ''' used for buying 'amount' number of pets '''

    # check if transaction was made before
    db =  get_db()
    with db:
        with db.cursor() as cur:
            sql = "SELECT 1 FROM transaction WHERE transaction_id = %s"
            result = cur.execute(sql, (transaction_id, ))

            # secure idempotency
            if result != 0:
                return { 'transaction_id': transaction_id, 'status': 'Pet(s) bought!' }

    result = get_pet(response, pet_id)

    # check if errors
    if 'errors' in result:
        response.status = HTTP_404
        return { 'errors': result['errors'] }

    pet = result['pet']

    # check available consistency
    if pet['available'] < amount:
        response.status = HTTP_400
        return { 'errors': 'Not enough pets' }

    # update number of pets
    pet['available'] = pet['available'] - amount

    result = update_pet(response, pet_id, pet)

    # check if errors
    if 'errors' in result:
        response.status = HTTP_503
        return { 'errors': result['errors'] }

    # calculate total price
    total_price = pet['price'] * amount

    # write transaction
    db = get_db()
    with db:
        with db.cursor() as cur:
            sql = '''INSERT INTO transaction(
                                transaction_id,
                                pet_id,
                                total_price,
                                pet_amount
                                ) 
                    VALUES(%s, %s, %s, %s);'''


            cur.execute(sql, (
                            transaction_id,
                            pet_id,
                            total_price,
                            amount
                            )
            )

            db.commit()

    return { 'transaction_id': transaction_id, 'status': 'Pet(s) bought!' }
