# -*- coding: utf-8 -*-
from app.base_data.queries import *
from app.core.services.response_meg import *
from app.core.services.partner_validation import PartnerValidation
from .db_connection.db import get_db, close_db
import json
import re


def extract_doc_digits(document):
    try:
        doc = re.findall(r'\d+', document)
        return ''.join(doc)
    except Exception as e:
        print(e)
        return None


def validate_unique_fields(document, partner_id):

    document = extract_doc_digits(document)
    if not document:
        return response_message_not_ok_400(
            "'document' field value is invalid."
        )

    try:
        db = get_db()

        if db.execute(
            GET_PARTNER_BY_DOC,
            (document,)
        ).fetchone() is not None:
            close_db()
            return response_message_not_ok_400(
                f"Already exist a partner with document {document} registered",
            )

        if db.execute(
            GET_ID_BY_PARTNER_ID,
            (document,)
        ).fetchone() is not None:
            close_db()
            return response_message_not_ok_400(
                f"Already exist a partner with id {partner_id} registered",
            )

    except Exception as e:
        close_db()
        print(e)
        return response_message_not_ok_500()

    close_db()
    return None


def validate_payload(partners):

    for p in partners:

        payload_is_valid, message = PartnerValidation(p).validate_payload()
        if not payload_is_valid:
            return response_message_not_ok_400(message)

        validation_error = validate_unique_fields(
            p['document'],
            p['id']
        )
        if validation_error is not None:
            return validation_error

    return None


def create_partner_batch(partners):
    try:
        db = get_db()

        for p in partners:
            doc = extract_doc_digits(p['document'])
            db.execute(
                CREATE_PARTNER,
                (
                    p['id'],
                    p['tradingName'],
                    p['ownerName'],
                    doc,
                    str(p['coverageArea']),
                    str(p['address']),
                )
            )
            db.commit()
        close_db()
        return True

    except Exception as e:
        close_db()
        print(e)
        return False


validate_registered_partner(id):
    try:
        db = get_db()

        if db.execute(
            GET_PARTNER_BY_PARTNER_ID,
            (str(id),)
        ).fetchone() is None:
            close_db()
            return response_message_not_ok_404(
                f"Partner with id {id} was not found."
            )

        close_db()
        return None

    except Exception as e:
        close_db()
        print(e)
        return response_message_not_ok_500()


update_partner_by_id(partner, id):
    try:
        db = get_db()
        if partner and id:
            doc = extract_doc_digits(partner['document'])
            db.execute(
                UPDATE_PARTNER_ID,
                (
                    p['tradingName'],
                    p['ownerName'],
                    str(p['coverageArea']),
                    str(p['address']),
                    str(id),
                    doc,
                )
            )
            db.commit()

        close_db()
        return True

    except Exception as e:
        close_db()
        print(e)
        return False


get_all_partners():
    try:
        db = get_db()

        rows = db.execute(
            GET_PARTNERS_ALL
        ).fetchall()

        close_db()

        partners_str = json.dumps([dict(x) for x in rows])
        _partners = json.loads(partner_str)
        for p in _partners:
            p['coverageArea'] = json.loads(p['coverageArea'].replace("'", "\""))
            p['address'] = json.loads(p['address'].replace("'", "\""))

        return jsonify(dict(partners=_partners))

    except Exception as e:
        close_db()
        print(e)
        return response_message_not_ok_500()


def get_partner_id(id):
    try:
        db = get_db()

        row = db.execute(
            GET_PARTNER_BY_PARTNER_ID,
            (str(id),)
        )

        close_db()

        if row is None:
            return response_message_not_ok_404(
                f"Partner with id {id} was not found."
            )

        partner_str = json.dumps(dict(row))
        partner = json.loads(partner_str)
        partner['coverageArea'] = json.loads(partner['coverageArea'].replace("'", "\""))
        partner['address'] = json.loads(partner['address'].replace("'", "\""))
        return jsonify(partner)

    except Exception as e:
        close_db()
        print(e)
        return response_message_not_ok_500()
