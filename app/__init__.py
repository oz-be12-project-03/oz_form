from flask import Blueprint, Flask, jsonify
from flask_migrate import Migrate
from app.routes import register_routes
from config import db

migrate = Migrate()

main_blp = Blueprint("main", __name__)

@main_blp.route("/", methods=["GET"])
def health_check():
    return jsonify({"message": "Success Connect"})

def create_app():
	application = Flask(__name__)
	application.config.from_object("config.Config")
	application.secret_key = "oz_form_secret"

	db.init_app(application)
	migrate.init_app(application, db)


	@application.errorhandler(400)
	def handle_bad_request(error):
		response = jsonify({"message": error.description})
		response.status_code = 400
		return response
	
	application.register_blueprint(main_blp)
	register_routes(application)

	return application
