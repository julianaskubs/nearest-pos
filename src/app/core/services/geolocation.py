# -*- coding: utf-8 -*-
from shapely.geometry import Point
from shapely.ops import nearest_points
import geopandas
import json

class GeolocationService:

    def search_partner_for_point(self, lat:float, long:float, partners:dict):
        # search for an available partner for a point

        point = self.create_point_obj(lat, long)

        partners_geo = self.create_geo_point_obj(partners)
        if partners_geo is None:
            return (False, 'Internal Server Error', 500)

        partners_gdf = self.create_data_frame_obj(partners_geo)

        while len(partners_gdf) > 0:

            nearested_partner = self.search_nearested_partner(
                point, partners_gdf
            )
            if not nearested_partner:
                return (False, 'Internal Server Error', 500)

            partner_id = nearested_partner['features'][0]['properties']['id']
            partner = next(iter(filter(lambda x: x['id'] == partner_id,
                partners['partners'])),
                None
            )
            partner_geo = self.create_geo_multipolygon_obj(partner)
            if partner_geo is None:
                return (False, 'Internal Server Error', 500)

            partner_gdf = self.create_data_frame_obj(partner_geo)

            is_available = self.check_available_partner(point, partner_gdf)

            if is_available:
                print(f'PartnerId {partner_id} is available for the point.')
                return (True, partner, 200)
            else:
                print(f'PartnerId {partner_id} is not available for the point.')

            partners_geo = self.remove_partner_from_geo_obj(partner_id, partners_geo)
            partners_gdf = self.create_data_frame_obj(partners_geo)

        return (False, None, 200)

    def create_point_obj(self, lat, long):
        return Point(long, lat)

    def create_geo_point_obj(self, data):
        # return a GeoJsonObject from data.
        try:
            features = []
            partners = data.get('partners', [])

            geo_json_obj = {
                'type': 'FeatureCollection'
            }
            for partner in partners:
                features.append(
                {
                    'id': partner['id'],
                    'type': 'Feature',
                    'properties': {
                        'tradingName': partner['tradingName'],
                        'lat': partner['address']['coordinates'][1],
                        'lon': partner['address']['coordinates'][0],
                        'id': partner['id']
                    },
                    'geometry': partner['address']
                })

            geo_json_obj.update(features=features)
            return geo_json_obj

        except Exception as e:
            print(e)
            return None

    def create_data_frame_obj(self, geo_json_obj):
        # return a GeoDataFrame object from a GeoJsonObject
        return geopandas.GeoDataFrame.from_features(geo_json_obj)

    def search_nearested_partner(self, point, partners_gdf):
        # return the nearested partner for the point
        try:
            # create a multipoint for partners point
            partners_multipoint = partners_gdf["geometry"].unary_union
            # create shapely geometry points
            partners_point = nearest_points(point, partners_multipoint)

            partner_data = partners_gdf.loc[partners_gdf["geometry"] == partners_point[1]]
            return json.loads(partner_data.to_json())

        except Exception as e:
            print(e)
            return None

    def create_geo_multipolygon_obj(self, data):
        # return a GeoJsonObject from data.
        try:
            return {
                'type': 'FeatureCollection',
                'features': [{
                    'id': data['id'],
                    'type': 'Feature',
                    'properties': {
                        'name': data['tradingName']
                    },
                    'geometry': data['coverageArea']
                }]
            }
        except Exception as e:
            print(e)
            return None

    def check_available_partner(self, point, partner_gdf):
        # verify if partner is available for point
        # create polygons object from partner coverageArea (MultiPolygons)
        polygons = partner_gdf["geometry"].unary_union
        if point.within(polygons):
            return True
        return False

    def remove_partner_from_geo_obj(self, partner_id, geo_json):
        # return a GeoJsonObject from data.
        features = geo_json['features']
        features.remove(next(iter(filter(lambda x: x['id'] == partner_id,
            features)),
            None
        ))
        return geo_json
