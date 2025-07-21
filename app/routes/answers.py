from flask import Blueprint, jsonify, request
from config import db
from app.models import Answer

answers_blp = Blueprint("answers", __name__)

@answers_blp.route("/submit", methods=["POST"])
def submit_answers():
    try:
        data = request.get_json()

        if not isinstance(data, list):
            return jsonify({"message": "리스트 형식의 JSON 데이터를 보내주세요."}), 400

        new_answers = []
        user_id_set = set()

        for item in data:
            user_id = item.get("user_id")
            choice_id = item.get("choice_id")

            if user_id is None or choice_id is None:
                return jsonify({"message": "user_id와 choice_id는 필수입니다."}), 400

            answer = Answer(user_id=user_id, choice_id=choice_id)
            db.session.add(answer)
            new_answers.append(answer)
            user_id_set.add(user_id)

        db.session.commit()

        return jsonify({"message": f"User: {list(user_id_set)[0]}'s answers Success Create"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
