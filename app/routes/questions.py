from flask import Blueprint, request, jsonify
from datetime import datetime

from app.models import Question, Image, Choice
from config import db

questions_blp = Blueprint("questions", __name__)

# 질문 단건 조회
@questions_blp.route("/questions/<int:question_id>", methods=["GET"])
def get_question_by_id(question_id):
    try:
        question = Question.query.filter_by(id=question_id).first()
        
        if not question:
            return jsonify({"message": "질문을 찾을 수 없습니다."}), 404

        response = {
            "id": question.id,
            "title": question.title,
            "sqe": question.sqe,
            "image_id": question.image_id,
        }
        return jsonify(question), 200
    
        image = Image.query.get(question.image_id)
        choice_list = (
            Choice.query.filter_by(question_id=question.id, is_active=True)
            .order_by(Choice.sqe)
            .all()
        )
        if not choice_list:
            return jsonify({"message": "선택지를 찾을 수 없습니다."}), 404  
        if not image:
            return jsonify({"message": "이미지를 찾을 수 없습니다."}), 404

        response = {
            "title": question.title,
            "image": image.url if image else None,
            "choices": [
                {
                    "id": c.id,
                    "content": c.content,
                    "sqe": c.sqe,
                    "is_active": c.is_active
                } for c in choice_list
            ],
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 질문 수 조회
@questions_blp.route("/questions/count", methods=["GET"])
def count_question():
    count = Question.query.filter_by(is_active=True).count()
    return jsonify({"total": count}), 200


# 질문 생성
@questions_blp.route("/question", methods=["POST"])
def create_question():
    try:
        data = request.get_json()

        # 필수 키 존재 확인
        required_keys = {"title", "sqe", "image_id"}
        if not data or not required_keys.issubset(data.keys()):
            return jsonify({"message": "title, sqe, image_id는 필수입니다."}), 400

        image = Image.query.get(data["image_id"])
        if not image:
            return jsonify({"message": "Image not found"}), 404

        if image.type.value != "sub":
            return jsonify({"message": "Image type must be 'sub'"}), 400

        question = Question(
            title=data["title"],
            sqe=data["sqe"],
            image_id=data["image_id"],
            is_active=data.get("is_active", True),
        )
        db.session.add(question)
        db.session.commit()

        return jsonify({
            "message": f"질문이 생성되었습니다. (ID: {question.id})",
            "id": question.id
        }), 201

    except KeyError as e:
        return jsonify({"message": f"필드 누락: {str(e)}"}), 400
