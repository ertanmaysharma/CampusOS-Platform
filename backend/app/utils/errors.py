from flask import jsonify


def error_response(message, status_code, code=None, details=None):
    response = {
        "success": False,
        "error": {
            "code": code or f"ERROR_{status_code}",
            "message": message,
        }
    }
    if details:
        response["error"]["details"] = details
    return jsonify(response), status_code


def success_response(data=None, message="Success", status_code=200):
    response = {"success": True, "message": message}
    if data is not None:
        response["data"] = data
    return jsonify(response), status_code


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return error_response("Bad request", 400, "BAD_REQUEST")

    @app.errorhandler(401)
    def unauthorized(e):
        return error_response("Unauthorized", 401, "UNAUTHORIZED")

    @app.errorhandler(403)
    def forbidden(e):
        return error_response("Forbidden", 403, "FORBIDDEN")

    @app.errorhandler(404)
    def not_found(e):
        return error_response("Not found", 404, "NOT_FOUND")

    @app.errorhandler(409)
    def conflict(e):
        return error_response("Conflict", 409, "CONFLICT")

    @app.errorhandler(422)
    def unprocessable(e):
        return error_response("Unprocessable entity", 422, "UNPROCESSABLE")

    @app.errorhandler(429)
    def rate_limited(e):
        return error_response("Rate limited", 429, "RATE_LIMITED")

    @app.errorhandler(500)
    def internal_error(e):
        return error_response("Internal server error", 500, "INTERNAL_ERROR")

    @app.errorhandler(503)
    def service_unavailable(e):
        return error_response("Service unavailable", 503, "SERVICE_UNAVAILABLE")
