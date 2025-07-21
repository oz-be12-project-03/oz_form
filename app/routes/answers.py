from flask import Blueprint, request, jsonify
from config import db
from app.models import Answer

answers_blp = Blueprint("answer", __name__)

@answers_blp.route("/answer", methods=["POST"])
def get_answers():
    try:
        answers = Answer.query.all()
        result = [
            {
                "id": a.id,
                "user_id": a.user_id,
                "choice_id": a.choice_id,
                "created_at": a.created_at.isoformat(),
                "update_at": a.update_at.isoformat()
            }
            for a in answers
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500