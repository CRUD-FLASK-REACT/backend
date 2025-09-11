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
        print("== Importing and registering blueprint ==")
        from .routes import bp
        print("== Registering blueprint 'bp' ==")
        app.register_blueprint(bp)  # No url_prefix means routes have no prefix
        db.create_all()
        print("== Blueprint registered and DB created ==")
        
    return app
