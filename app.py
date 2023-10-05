from flask import Flask
# from flask_restx import Api
from database import database
from sqlalchemy.dialects.postgresql import psycopg2
from src.controllers.post_controller import post_route
from src.controllers.user_controller import auth
from flask_swagger_ui import get_swaggerui_blueprint


SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'


def create_app():
    temp_app = Flask(__name__)

    temp_app.config.from_object('config.DevelopmentConfig')

    database.init_app(temp_app)

    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        API_URL,
        config={  # Swagger UI config overrides
            'app_name': "Test application"
        }
    )

    temp_app.register_blueprint(auth, url_prefix="/user")
    temp_app.register_blueprint(post_route, url_prefix="/")
    temp_app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    with temp_app.app_context():
        from flask_migrate import migrate

    from src.models.Post import Post
    from src.models.User import User
    from src.models.Comment import Comment
    from src.models.Like import Like
    from src.models.BlacklistToken import BlacklistToken

    return temp_app


run_app = create_app()

# api_app = Api(app=run_app,
#               version="1.0",
#               title="Blog",
#               description="Manage names of various users of the application")

if __name__ == "__main__":
    run_app.run(debug=True, port=3000, host='localhost')
