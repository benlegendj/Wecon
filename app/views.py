import os
import random
from app import app
from flask import abort, jsonify, make_response, request, json
from .app_class import myDatabase

weconnect = myDatabase()


@app.route('/api/v1/auth/register', methods=['POST'])
def register_user():
    # if not request.json or 'email' not in request.json:
    #     abort(400)
    data = json.loads(request.data)
    email = data['email']
    first_name = data['first_name']
    last_name = data['email']
    password = data['password']
    new_user = weconnect.register_user(random.randint(1, 500),
                                       first_name, last_name, email, password)
    if new_user:
        return jsonify({'message': 'Successfully created user'}), 200


@app.route('/api/v1/auth/login', methods=['POST'])
def login_user():
    # if not request.json or 'email' not in request.json:
    #     abort(400)
    data = data = json.loads(request.data)
    email = data['email']
    password = data['password']
    user = weconnect.login_user(email, password)
    if user:
        # Generate a token
        return jsonify({'message': 'Successfully logged in'}), 200


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    pass


@app.route('/api/v1/auth/reset-password', methods=['POST'])
def reset_password():
    # if not request.json or 'email' not in request.json:
    #     abort(400)
    data = request.get_json()
    email = data['email']
    password = data['password']
    new_password = data['new_password']
    user = weconnect.reset_password(email, password, new_password)
    if user:
        return jsonify({'message': 'Successfully updated password'}), 200


@app.route('/api/v1/businesses', methods=['GET'])
def get_businesses():
    """Returns all businesses"""
    businesses = weconnect.get_businesses()
    return jsonify({'businesses': businesses})


@app.route('/api/v1/businesses/<businessId>', methods=['GET'])
def get_business(businessId):
    """Returns a specific business"""
    business = weconnect.get_business(int(businessId))
    if business is None:
        abort(404)
    return jsonify({'business': business})


@app.route('/api/v1/businesses', methods=['POST'])
def register_business():
    """Registers a business"""

    name = request.json['name']
    location = request.json['location']
    description = request.json['description']
    category = request.json['category']
    emptyString = ""
    if name is not None or description is not None or location is not None or category is not None:
        if name != emptyString or description != emptyString or location != emptyString or category != emptyString:
            new_business = weconnect.create_business(
                random.randint(1, 500), name, location, category, description)
            return jsonify({'business': new_business}), 201
        return jsonify({"response": "Empty value entered"})
    return abort(400)


@app.route('/api/v1/businesses/<businessId>', methods=['PUT'])
def update_business(businessId):
    """Updates a business"""
    if int(businessId) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and isinstance(
            (request.json['name']), str) == False:
        abort(400)
    if 'description' in request.json and isinstance(
            (request.json['description']), str) == False:
        abort(400)
    if 'location' in request.json and isinstance(
            (request.json['location']), str) == False:
        abort(400)
    if 'category' in request.json and isinstance(
            (request.json['category']), str) == False:
        abort(400)

    name = request.json['name']
    description = request.json['description']
    location = request.json['location']
    category = request.json['category']

    if name is not None or description is not None or location is not None or category is not None:
        business = weconnect.update_business(
            int(businessId), name, location, description, category)
        return jsonify(business)


@app.route('/api/v1/businesses/<businessId>', methods=['DELETE'])
def delete_business(businessId):
    """Deletes a business"""
    print(businessId)
    if int(businessId) == 0:
        abort(404)

    # if not request.json:
    # abort(400)
    delete_business = weconnect.delete_business(int(businessId))
    if delete_business:
        return jsonify({'message': 'Business deleted'})


@app.route('/api/v1/businesses/<businessId>/reviews', methods=['POST'])
def set_review(businessId):
    """Adds a review to a business"""
    if not request.json or 'review' not in request.json:
        abort(400)
    review = request.json['review']
    business_id = int(businessId)
    new_review = weconnect.add_review(business_id, random.randint(1, 300),
                                      review)
    if new_review is None:
        abort(404)
    return jsonify(new_review), 201


@app.route('/api/v1/businesses/<businessId>/reviews', methods=['GET'])
def get_reviews(businessId):
    """Returns reviews for the specified business"""
    reviews = weconnect.get_reviews(int(businessId))
    print(reviews)
    return jsonify({'business': reviews})


@app.errorhandler(404)
def not_found(error):
    """This is the error handler"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
