# -*- coding: utf-8 -*-
from .services.partner_util import *


def create_partners(payload):
    try:
        partners = []

        if type(payload) == dict:
            if payload.get('partners'):
                partners = payload['partners']
            else:
                partners.append(payload)

        else if type(payload) == list:
            partners = payload

        validation_error_msg = validate_payload(partners)
        if validation_error_msg:
            return validation_error_msg

        is_created = create_partner_batch(partners)
        if not is_created:
            return response_message_not_ok_500()

        return response_message_ok('created', 201)

    except Exception as e:
        print(e)
        return response_message_not_ok_500()


def update_partner(payload, id):
    try:
        partners = []

        if payload:
            if str(payload['id']) != str(id):
                return response_message_not_ok_400(
                    "Path 'id' is not equal payload 'id'. Take a look."
                )
            partners.append(payload)

            validation_error_msg = validate_payload(partners)
            if validation_error_msg:
                return validation_error_msg

            partner_not_exist_msg = validate_registered_partner(id)
            if partner_not_exist_msg:
                return partner_not_exist_msg

            is_updated = update_partner_by_id(partners[0], id)
            if not is_updated:
                return response_message_not_ok_500()

            return response_message_ok('accepted', 202)

    except Exception as e:
        print(e)
        return response_message_not_ok_500()


def get_partners():
    try:
        return get_all_partners()

    except Exception as e:
        print(e)
        return response_message_not_ok_500()


def get_partner_by_id(id):
    try:
        return get_partner_id(id)

    except Exception as e:
        print(e)
        return response_message_not_ok_500()

