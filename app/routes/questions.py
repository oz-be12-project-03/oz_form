from flask import Blueprint, request, jsonify
from datetime import datetime

from app.models import Question, Image
from config import db

questions_blp = Blueprint("questions", __name__)

# 질문 전체 조회
@questions_blp.route("/questions", methods=["GET"])
def get_all_questions():
    questions = Question.query.order_by(Question.sqe).all()
    result = []

    for q in questions:
        result.append({
            "id": q.id,
            "title": q.title,
            "image_url": q.image.url if q.image else None,
            "sqe": q.sqe,
            "is_active": q.is_active,
            "created_at": q.created_at.isoformat(),
            "updated_at": q.updated_at.isoformat(),
        })

    return jsonify({"questions": result}), 200


# 질문 단건 조회 by ID
@questions_blp.route("/question/<int:question_id>", methods=["GET"])
def get_question_by_id(question_id):
    question = Question.query.get(question_id)
    if not question:
        return jsonify({"message": "질문을 찾을 수 없습니다."}), 404

    return jsonify({
        "id": question.id,
        "title": question.title,
        "image_url": question.image.url if question.image else None,
        "sqe": question.sqe,
        "is_active": question.is_active,
        "created_at": question.created_at.isoformat(),
        "updated_at": question.updated_at.isoformat()
    }), 200

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
