import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta

from .config import Config
from .extensions import db, migrate, jwt
from .utils.errors import register_error_handlers
from .utils.logger import setup_logging


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # CORS - parse comma-separated origins from env var, default to * for flexibility
    raw_origins = app.config.get("CORS_ORIGINS", "*")
    origins = [o.strip() for o in raw_origins.split(",") if o.strip()]
    CORS(
        app,
        resources={r"/api/*": {"origins": origins, "allow_headers": ["*"]}},
        supports_credentials=True,
    )

    # Setup logging
    setup_logging(app)

    # Register error handlers
    register_error_handlers(app)

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.users import users_bp
    from .routes.requests import requests_bp
    from .routes.workflows import workflows_bp
    from .routes.agents import agents_bp
    from .routes.approvals import approvals_bp
    from .routes.departments import departments_bp
    from .routes.notifications import notifications_bp
    from .routes.dashboard import dashboard_bp
    from .routes.audit import audit_bp
    from .routes.knowledge import knowledge_bp
    from .routes.feedback import feedback_bp
    from .routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(requests_bp, url_prefix="/api/requests")
    app.register_blueprint(workflows_bp, url_prefix="/api/workflows")
    app.register_blueprint(agents_bp, url_prefix="/api/agents")
    app.register_blueprint(approvals_bp, url_prefix="/api/approvals")
    app.register_blueprint(departments_bp, url_prefix="/api/departments")
    app.register_blueprint(notifications_bp, url_prefix="/api/notifications")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
    app.register_blueprint(audit_bp, url_prefix="/api/audit-logs")
    app.register_blueprint(knowledge_bp, url_prefix="/api/knowledge")
    app.register_blueprint(feedback_bp, url_prefix="/api/feedback")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    # Health check
    @app.route("/api/health")
    def health():
        try:
            # Verify database connectivity
            from sqlalchemy import text
            db.session.execute(text("SELECT 1"))
            db_ok = True
        except Exception:
            db_ok = False

        status = "ok" if db_ok else "degraded"
        return {"status": status, "database": "connected" if db_ok else "disconnected", "message": "CampusOS API is running"}

    return app
