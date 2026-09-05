from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import ChatHistory

chatbot_bp = Blueprint(
    "chatbot",
    __name__,
    url_prefix="/api/chatbot"
)


# ================================
# CHAT
# ================================

@chatbot_bp.route("", methods=["POST"])
@jwt_required()
def chatbot():

    user_id = get_jwt_identity()

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No message received"
        }), 400

    message = data.get("message")

    if not message:
        return jsonify({
            "success": False,
            "message": "Message is required"
        }), 400

    # Basic response for now
    response = (
        "I received your message. "
        "The FinAI chatbot backend is working."
    )

    try:

        chat = ChatHistory(
            user_id=user_id,
            message=message,
            response=response
        )

        db.session.add(chat)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": message,
            "response": response
        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500