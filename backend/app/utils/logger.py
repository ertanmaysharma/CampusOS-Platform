import logging
import sys


def setup_logging(app):
    log_level = logging.DEBUG if app.config.get("DEBUG") else logging.INFO

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Suppress noisy loggers
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    app.logger.setLevel(log_level)
    app.logger.info("CampusOS logging initialized")
