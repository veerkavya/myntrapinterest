from flask import Flask
from config import Config
from flask_migrate import Migrate
from .models import db
from .routes import bp  # Adjust the import path as per your project structure
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(bp)

    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    
    return app
