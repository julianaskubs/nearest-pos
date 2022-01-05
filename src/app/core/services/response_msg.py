# -*- coding: utf-8 -*-
from flask import jsonify

def response_message_ok(message, status):
    response = jsonify({'message': message})
    response.status_code = status
    return response

def response_message_not_ok_500():
    response = jsonify({
        'message': 'An internal server error has occurred'
    })
    response.status_code = 500
    return response

def response_message_not_ok_400(message):
    response = jsonify({
        'message': message
    })
    response.status_code = 400
    return response

def response_message_not_ok_404(message):
    response = jsonify({
        'message': message
    })
    response.status_code = 404
    return response