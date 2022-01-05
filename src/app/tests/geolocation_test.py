# -*- coding: utf-8 -*-
from app.core.services.geolocation import GeolocationService
import json

LAT = -22.748650
LONG= -43.432824

with open("sample.json", encoding='utf-8', errors='ignore') as json_data:
    PDATA = json.load(json_data, strict=False)

GEO = GeolocationService()

def test_point():
    point = GEO.create_point_obj(LAT, LONG)
    assert point.bounds == (-43.432824, -22.74865, -43.432824, -22.74865)

def test_partners_geo():
    pgeo = GEO.create_geo_point_obj(PDATA)
    assert (pgeo.get('features') != None) == True
    assert pgeo.get('type') == 'FeatureCollection'

def test_partners_gdf():
    pgeo = GEO.create_geo_point_obj(PDATA)
    pgdf = GEO.create_data_frame_obj(pgeo)
    assert pgdf.bounds.columns.array[0] == 'minx'
    assert pgdf.bounds.columns.array[1] == 'miny'
    assert pgdf.bounds.columns.array[2] == 'maxx'
    assert pgdf.bounds.columns.array[3] == 'maxy'

def test_nearested_partner():
    point = GEO.create_point_obj(LAT, LONG)
    pgeo = GEO.create_geo_point_obj(PDATA)
    pgdf = GEO.create_data_frame_obj(pgeo)
    nearested = GEO.search_nearested_partner(point, pgdf)
    assert nearested.get('type') == 'FeatureCollection'

def test_partner_geo_multpolygon():
    partners = PDATA.get('partners', [])
    partner_geo_mult = GEO.create_geo_multipolygon_obj(partners[0])
    assert partner_geo_mult['features'][0]['geometry']['type'] == 'MultiPolygon'

def test_partner_gdf():
    partners = PDATA.get('partners', [])
    partner_geo_mult = GEO.create_geo_multipolygon_obj(partners[0])
    partner_gdf = GEO.create_data_frame_obj(partner_geo_mult)
    assert partner_gdf.bounds.columns.array[0] == 'minx'

def test_available_partner():
    point = GEO.create_point_obj(LAT, LONG)
    partners = PDATA.get('partners', [])
    partner_geo_mult = GEO.create_geo_multipolygon_obj(partners[0])
    partner_gdf = GEO.create_data_frame_obj(partner_geo_mult)
    is_available = GEO.check_available_partner(point, partner_gdf)
    assert is_available == False

def search_available_partner():
    is_available, message, status = GEO.search_partner_for_point(LAT, LONG, PDATA)
    assert is_available == True
    assert status == '200'
