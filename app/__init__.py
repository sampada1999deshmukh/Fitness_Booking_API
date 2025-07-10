from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)

    from app.fitness_booking_api.routes import bp as fitness_bp
    app.register_blueprint(fitness_bp)
    # from app.home.routes import bp as first_bp
    # app.register_blueprint(first_bp)

    return app
