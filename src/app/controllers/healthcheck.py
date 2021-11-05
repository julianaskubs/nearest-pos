# -*- coding: utf-8 -*-
from flask import Flask, Blueprint

bp = Blueprint('healthcheck', __name__, url_prefix='/')

@bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    return 'Ok'