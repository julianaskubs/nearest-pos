# -*- coding: utf-8 -*-
import os
from flask import Flask

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
        SECRET_KEY='dev'
    )
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except Exception as e:
        print(e)

    from .controllers import healthcheck
    app.register_blueprint(healthcheck.bp)

    return app
