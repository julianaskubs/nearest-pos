# -*- coding: utf-8 -*-

CREATE_PARTNER = \
'INSERT INTO partner(\
    partner_id,\
    trading_name,\
    owner_name,\
    document,\
    coverage_area,\
    address\
) VALUES (?,?,?,?,?,?)'

GET_PARTNER_BY_DOC = \
'SELECT id FROM partner WHERE document = ?'

GET_ID_BY_PARTNER_ID = \
'SELECT id FROM partner WHERE partner_id = ?'

UPDATE_PARTNER_ID = \
'UPDATE partner SET \
    trading_name = ?, \
    owner_name = ? \
    coverage_area = ? \
    address = ? \
WHERE partner_id = ? \
AND document = ?'

GET_PARTNERS_ALL = \
'SELECT \
    partner_id as id, \
    trading_name as tradingName, \
    owner_name as ownerName, \
    document, \
    coverage_area as coverageArea, \
    address \
FROM partners'

GET_PARTNER_BY_PARTNER_ID = \
'SELECT \
    partner_id as id, \
    trading_name as tradingName, \
    owner_name as ownerName, \
    document, \
    coverage_area as coverageArea, \
    address \
FROM partner \
WHERE partner_id = ?'
