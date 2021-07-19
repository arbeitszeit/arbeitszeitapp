from flask import Flask, session
from flask_table import Col, Table  # Do not delete

from project.extensions import db, login_manager, migrate


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_envvar("ARBEITSZEIT_APP_CONFIGURATION")

    # Where to redirect the user when he attempts to access a login_required
    # view without being logged in.
    login_manager.login_view = "auth.start"

    # init flask extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from .models import Company, Member

        @login_manager.user_loader
        def load_user(user_id):
            """
            This callback is used to reload the user object from the user ID
            stored in the session.
            """
            user_type = session["user_type"]
            if user_type == "member":
                return Member.query.get(int(user_id))
            elif user_type == "company":
                return Company.query.get(int(user_id))

        # register blueprints
        from .auth import routes as auth_routes
        from .company import routes as company_routes
        from .member import routes as member_routes

        app.register_blueprint(auth_routes.auth)
        app.register_blueprint(company_routes.main_company)
        app.register_blueprint(member_routes.main_member)

        # create the initial database
        db.create_all()

        return app
