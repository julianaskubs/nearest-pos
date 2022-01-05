# -*- coding: utf-8 -*-
from app.core.services.partner_validator import PartnerValidator

mock_payload = {
    "id": 1,
    "tradingName": "Doceria Duna",
    "ownerName": "Confeiteira Duna",
    "document": "13.415.000/0001-00",
    "coverageArea": {
        "type": "MultiPolygon",
        "coordinates": [
            [[[30, 20], [45, 40], [10, 40], [30, 20]]],
            [[[15, 5], [40, 10], [10, 20], [5, 10], [15, 5]]]
        ]
    },
    "address": {
        "type": "Point",
        "coordinates": [-46.57421, -21.785741]
    }
}

validator = PartnerValidator(mock_payload)

def test_payload_ok():
    result, msg = validator.validate()
    assert result == True
    assert msg == "ok"

def test_empty_payload():
    validator.payload = {}
    result, msg = validator.validate()
    assert result == False
    assert msg == "An empty payload is not valid."

def test_empty_partner_id():
    validator.payload = mock_payload
    validator.payload['id'] = None
    result, msg = validator.validate()
    assert result == False
    assert msg == "An 'id' attribute should be provided."

def test_empty_trading_name():
    validator.payload['tradingName'] = None
    validator.payload['id'] = 1
    result, msg = validator.validate()
    assert result == False
    assert msg == "A 'tradingName' attribute should be provided."

def test_empty_owner_name():
    validator.payload['ownerName'] = None
    validator.payload['tradingName'] = "Doceria Duna"
    result, msg = validator.validate()
    assert result == False
    assert msg == "An 'ownerName' attribute should be provided."

def test_empty_document():
    validator.payload['document'] = None
    validator.payload['ownerName'] = "Confeiteira Duna"
    result, msg = validator.validate()
    assert result == False
    assert msg == "An 'document' attribute should be provided."

def test_empty_coverage_area():
    validator.payload['coverageArea'] = None
    validator.payload['document'] = "13.415.000/0001-00"
    result, msg = validator.validate()
    assert result == False
    assert msg == "A 'coverageArea' attribute should be provided."

def test_coverage_area():
    validator.payload['coverageArea'] = {
        "type": "Point",
        "coordinates": [
            [[[30, 20], [45, 40], [10, 40], [30, 20]]],
            [[[15, 5], [40, 10], [10, 20], [5, 10], [15, 5]]]
        ]
    }
    result, msg = validator.validate()
    assert result == False
    assert msg == "The 'type' attribute value of 'coverageArea' must be 'MultiPolygon'."

def test_invalid_multipolygon_format():
    validator.payload['coverageArea']['coordinates'] = [
        [[[30, 20], [45, 40]]],
        [[[15, 5], [40, 10], [10, 20], [5, 10], [15, 5]]]
    ]
    validator.payload['coverageArea']["type"] = "MultiPolygon"
    result, msg = validator.validate()
    assert result == False
    assert msg == "The 'coordinates' field of 'coverageArea' is invalid. Take a look."

def test_multipolygon_auto_fix():
    validator.payload['coverageArea']['coordinates'] = [
        [[[30, 20], [45, 40], [10, 40]]],
        [[[15, 5], [40, 10], [10, 20], [5, 10]]]
    ]
    result, msg = validator.validate()
    assert result == True
    assert msg == "ok"
