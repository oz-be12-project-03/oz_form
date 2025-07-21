from flask import jsonify, request, Blueprint
from app.models import Image
from config import db

images_blp = Blueprint("images", __name__)

@images_blp.route("/image", methods=["POST"])
def create_image():
    data = request.get_json()

    if not data or "url" not in data or "type" not in data:
        return jsonify({"message": "url과 type을 모두 포함해야 합니다."}), 400

    new_image = Image(
        url=data["url"],
        type=data["type"]
    )

    db.session.add(new_image)
    db.session.commit()
    return jsonify({"message": f"ID: {new_image.id} 이미지가 성공적으로 생성되었습니다."}), 201


@images_blp.route("/image/main", methods=["GET"])
def get_main_image():
    main_image = Image.query.filter_by(type="main").first()

    if main_image:
        return jsonify({"image": main_image.url}), 200
    else:
        return jsonify({"image": None, "message": "메인 이미지가 없습니다."}), 200
