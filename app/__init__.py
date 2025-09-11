from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    print("== Flask create_app running, blueprint should be registered ==")
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    CORS(app)
    
    with app.app_context():
        from .routes import bp
        app.register_blueprint(bp)  # No url_prefix means no prefix in routes
        db.create_all()
        
    return app
