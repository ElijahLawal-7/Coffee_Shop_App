import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks')
@requires_auth("get:drinks")
def get_drinks():
    # Getting all available drinks from the database
    all_drinks = Drink.query.all()

    # Formatting all available drinks
    formatted_drinks = [drink.short() for drink in all_drinks]

    # Checking if there is/are drinks
    if len(all_drinks) == 0:
        abort(404)

    return jsonify({
        'sucess': True,
        'drinks': formatted_drinks,
    })


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth("get:drinks-detail")
def get_drinks_detail():
    # Getting all drinks from the database
    all_drinks = Drink.query.all()
 
    # Formatting all drinks to what the frontend is expecting
    formatted_drinks = [drink.long() for drink in all_drinks]

    # Checking if there is/are drinks
    if len(all_drinks) == 0:
        abort(401)

    return jsonify({
        'sucess': True,
        'drinks': formatted_drinks,
    })


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink():
    # Getting the body from the request
    body = request.get_json()

    title = body.get('title', None)
    recipe = body.get('recipe', None)

    formatted_recipe = json.dumps(recipe)

    # Checking if body contain expected details
    if not title and recipe:
        abort(400)

    # Creating a new drink using the request body.
    drink = Drink(title=title, recipe=formatted_recipe)
    drink.insert()

    # # Getting the newly created drink
    all_drinks = Drink.query.filter_by(title=title).all()
    formatted_drinks = [drink.long() for drink in all_drinks]

    return jsonify({
        'sucess': True,
        'drinks': formatted_drinks,
    })


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:update_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(update_id):
    # Getting the row of the given ID.
    drink = Drink.query.filter(Drink.id == update_id).one_or_none()

    # Checking if the id exist in the table
    if not drink:
        abort(404)

    # Getting the request body since the id exist and we can update the row.
    body = request.get_json()

    title = body.get('title', None)
    recipe = body.get('recipe', None)

    # Checking if body contains all expected details
    if not title and recipe:
        abort(400)

    if title:
        drink.title = title
    if recipe:
        drink.recipe = json.dumps(recipe)
    
    drink.update()

    # Getting the updated drink
    all_drinks = Drink.query.filter_by(title=title).all()
    formatted_drinks = [drink.long() for drink in all_drinks]

    return jsonify({
        'sucess': True,
        'drinks': formatted_drinks,
    })


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:delete_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(delete_id):

    # Checking if the id exist in the table
    drink = Drink.query.filter(Drink.id == delete_id).one_or_none()
    if not drink:
        abort(404)

    drink.delete()

    return jsonify({
        'sucess': True,
        'id': delete_id,
    })


# Error Handling
'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': "Resource(s) not found"
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': "Request unprocessable"
    }), 422


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': "Bad Request"
    }), 400


@app.errorhandler(405)
def false_methods(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': "Method(s) not allowed"
    }), 405


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def auth_error_handler(e):
    return jsonify(e.to_dict()), e.status_code


# if __name__ == "__main__":
#     app.debug = True
#     app.run(host="0.0.0.0")
