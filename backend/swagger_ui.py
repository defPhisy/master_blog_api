from flask_swagger_ui import get_swaggerui_blueprint

# swagger endpoint e.g. HTTP://localhost:5002/api/docs
SWAGGER_URL = "/api/docs"

# swagger config file
API_URL = "http://127.0.0.1:5002/static/masterblog.yaml"

# swagger blueprint for flask app
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Masterblog API"},
)
