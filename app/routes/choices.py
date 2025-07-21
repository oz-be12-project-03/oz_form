from config import db
from app.models import Choice
from flask import Blueprint, request, jsonify

# 블루프린트 생성
choice_blp = Blueprint('choice', __name__, url_prefix='/choice')

# POST: 선택지 생성
@choice_blp.route('/', methods=['POST'])

def create_choice():
    data = request.get_json()
    try:
        new_choice = Choice(
            question_id=data['question_id'],
            content=data['content'],
            sqe=data['sqe'],
            is_active=data.get('is_active', True)
        )
        db.session.add(new_choice)
        db.session.commit()
        return jsonify({"message": "Choice created", "choice_id": new_choice.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# GET: 특정 질문에 대한 선택지 리스트 조회
@choice_blp.route('/question/<int:question_id>', methods=['GET'])
def get_choice_by_question(question_id):
    choice = Choice.query.filter_by(question_id=question_id).all()

    return jsonify([
        {
            "id": c.id,
            "content": c.content,
            "sqe": c.sqe,
            "is_active": c.is_active
        } for c in choice
    ]), 200

