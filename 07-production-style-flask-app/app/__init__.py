from flask import Flask

from app.extensions import db, migrate


def create_app():
    app=Flask(__name__)
    
    app.config.from_object("config.Config")
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.routes.main import main
    app.register_blueprint(main)
    
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Resource not found"}, 404

    
    return app