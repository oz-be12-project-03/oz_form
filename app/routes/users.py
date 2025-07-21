from flask import Blueprint, jsonify, request
from app.models import User
from config import db

user_blp = Blueprint("users", __name__)

# 사용자 생성
@user_blp.route("/users", methods=["POST"])

def create_user():
    data = request.get_json()

    required_fields = {"name", "age", "gender", "email"}
    if not data or not required_fields.issubset(data):
        return jsonify({"message": "name, age, gender, email 모두 필요합니다."}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "이미 존재하는 이메일입니다."}), 400

    new_user = User(
        name=data["name"],
        age=data["age"],
        gender=data["gender"],
        email=data["email"]
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "사용자가 생성되었습니다.", "user_id": new_user.id}), 201

# 전체 사용자 조회
@user_blp.route("/users", methods=["GET"])
def get_all_users():
    users = User.query.all()
    result = [
        {
            "id": user.id,
            "name": user.name,
            "age": user.age,
            "gender": user.gender,
            "email": user.email,
            "created_at": user.created_at.isoformat()
        }
        for user in users
    ]
    return jsonify(result), 200

# 특정 사용자 조회
@user_blp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "해당 사용자를 찾을 수 없습니다."}), 404

    return jsonify({
        "id": user.id,
        "name": user.name,
        "age": user.age,
        "gender": user.gender,
        "email": user.email,
        "created_at": user.created_at.isoformat()
    }), 200
