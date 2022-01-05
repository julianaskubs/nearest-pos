# -*- coding: utf-8 -*-
from shapely.geometry import shape, Polygon

class PartnerValidator(object):

    def __init__(self, payload):
        self.payload = payload

    def validate(self):
        if not self.payload:
            return (False, "An empty payload is not valid.")
        return self.validate_id()

    def validate_id(self):
        """Validate payload 'id' field"""
        if not self.payload.get('id'):
            return (False, "An 'id' attribute should be provided.")

        return self.validate_names()

    def validate_names(self):
        """Validate payload 'tradingName' and 'ownerName' fields"""

        if not self.payload.get('tradingName'):
            return (False, "A 'tradingName' attribute should be provided.")

        if not self.payload.get('ownerName'):
            return (False, "An 'ownerName' attribute should be provided.")

        return self.validate_document()

    def validate_document(self):
        """Validate payload 'document' fields"""
        if not self.payload.get('document'):
            return (False, "An 'document' attribute should be provided.")

        return self.validate_covarage_area()

    def validate_multipolygon(self):
        try:
            coordinates = self.payload['coverageArea']
            multipoly = shape(coordinates)
            poly_coords = [list(p.exterior.coords) for p in multipoly]
            for p in poly_coords:
                polygon = Polygon(p)
                # Removing this validation for now, until a deep investigation.
                # if not polygon.is_valid:
                #     print('Polygon is not valid')
                #     return False
            return True
        except Exception as e:
            print(e)
            return False

    def validate_covarage_area(self):
        if not self.payload.get('coverageArea'):
            return (False, "A 'coverageArea' attribute should be provided.")

        if not self.payload['coverageArea'].get('type'):
            return (False, "A 'type' attribute of 'coverageArea' should be provided.")

        if not self.payload['coverageArea'].get('coordinates'):
            return (False, "A 'coordinates' attribute of 'coverageArea' should be provided.")

        if self.payload['coverageArea']['type'] != 'MultiPolygon':
            return (False, "The 'type' attribute value of 'coverageArea' must be 'MultiPolygon'.")

        # validate multipolygon field
        if not self.validate_multipolygon():
            return (False, "The 'coordinates' field of 'coverageArea' is invalid. Take a look.")

        return self.validate_address_point()

    def validate_point(self):
        try:
            coordinates = self.payload['address']
            point = shape(coordinates)
            if not point.is_valid:
                return False
            return True
        except Exception as e:
            print(e)
            return False

    def validate_address_point(self):
        if not self.payload.get('address'):
            return (False, "An 'address' attribute should be provided.")

        if not self.payload['address'].get('type'):
            return (False, "A 'type' attribute of 'address' should be provided.")

        if not self.payload['address'].get('coordinates'):
            return (False, "A 'coordinates' attribute of 'address' should be provided.")

        if self.payload['address']['type'] != 'Point':
            return (False, "The 'type' attribute value of 'address' must be 'Point'.")

        # validate point field
        if not self.validate_point():
            return (False, "The 'coordinates' field of 'address' is invalid. Please, take a look.")

        return (True, "ok")
