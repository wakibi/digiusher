import logging

from flask import Flask
from flask_migrate import Migrate

from app import commands, routes, config
from app.db import db
from .extensions import scheduler


def create_app():
    app = Flask(__name__)
    # DB initialisation
    app.config.from_object(config.PostgreSQLConfig)
    db.init_app(app)
    # Migrate command
    migrate = Migrate(app, db)
    
    # Scheduler
    scheduler.init_app(app)
    logging.getLogger("apscheduler").setLevel(logging.INFO)
    scheduler.start()
    
    app.register_blueprint(routes.bp)
    app.register_blueprint(commands.integrations)
    return app
