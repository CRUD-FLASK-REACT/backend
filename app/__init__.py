def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    CORS(app)

    with app.app_context():
        from .routes import bp
        app.register_blueprint(bp)
        db.create_all()

        print("== Registered Routes ==")
        for rule in app.url_map.iter_rules():
            print(rule)

    return app
