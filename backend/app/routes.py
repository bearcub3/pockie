from flask import request, jsonify, abort, flash, redirect, url_for
import requests
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.models import User, Finance, Income, Expense


@app.route('/')
def index():
    return "Hello Pockie!"


'''
user : creation, deletion, reception
'''
@app.route('/api/user', methods=['GET', 'POST'])
def user():
    errors = []

    if request.method == 'POST':
        body = request.get_json()

        try:
            first_name = body['first_name']
            last_name = body['last_name']
            email = body['email']
            password = body['password']
            dbpassword = body['dbpassword']
            participants = body['participants']
            joint = body['joint']
            currency = body['currency']

            duplicate = User.query.filter(User.email == email).first()

            if duplicate:
                errors.append('The email is already in use.')
                return jsonify({
                    'success': False,
                    'messages': 'The email is already in use.'
                }), 406

            elif duplicate is None:
                user = User(first_name=first_name, last_name=last_name, email=email,
                            joint=joint, participants=participants, currency=currency)

                user.set_password(password)
                user.check_password(dbpassword)
                user.insert()

                # print(user)

                return jsonify({
                    'success': True,
                    'messages': 'A new user is successfully registered.'
                }), 200

        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
            print(errors)

    elif request.method == 'GET':
        users = User.query.order_by(User.id).all()

        if len(users) == 0:
            abort(404)

        # print(users)

        return jsonify({
            'users': [user.format() for user in users],
            'total_users': len(users)
        }), 200

    else:
        abort(500)


@app.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter(User.id == user_id).one_or_none()

    if user is None:
        abort(404)

    if user:
        user.delete()

        return jsonify({
            'success': True,
            'id': user_id
        }), 200

    else:
        abort(500)


'''
log in & log out
'''
@app.route('/api/login', methods=['POST'])
def login():
    body = request.get_json()

    email = body['email']
    password = body['password']

    user = User.query.filter_by(email=email).first()

    if user is None or not user.check_password(password):
            return jsonify({
                'success': False,
                'message': 'Email or Password is not valid'
            }), 200

    if user:
        login_user(user)
        return jsonify({
                'success': True,
                'data': {
                    'first_name': user.first_name,
                    'joint': user.joint,
                    'participants': user.participatns,
                    'currency': user.currency
                }
            }), 200



