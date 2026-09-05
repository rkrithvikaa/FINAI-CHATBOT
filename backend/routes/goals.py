from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import Goal

goals_bp = Blueprint("goals", __name__, url_prefix="/api/goals")


# ================================
# GET ALL GOALS
# ================================

@goals_bp.route("", methods=["GET"])
@jwt_required()
def get_goals():

    user_id = get_jwt_identity()

    goals = Goal.query.filter_by(user_id=user_id).all()

    result = []

    for goal in goals:

        result.append({
            "id": goal.id,
            "goal_name": goal.goal_name,
            "target_amount": goal.target_amount,
            "current_amount": goal.current_amount,
            "deadline": (
                goal.deadline.isoformat()
                if goal.deadline
                else None
            )
        })

    return jsonify(result), 200


# ================================
# ADD GOAL
# ================================

@goals_bp.route("", methods=["POST"])
@jwt_required()
def add_goal():

    user_id = get_jwt_identity()

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data received"
        }), 400

    goal_name = data.get("goal_name")
    target_amount = data.get("target_amount")
    current_amount = data.get("current_amount", 0)
    deadline = data.get("deadline")

    if not goal_name or target_amount is None:
        return jsonify({
            "success": False,
            "message": "Goal name and target amount are required"
        }), 400

    try:

        from datetime import datetime

        deadline_date = None

        if deadline:
            deadline_date = datetime.strptime(
                deadline,
                "%Y-%m-%d"
            ).date()

        goal = Goal(
            user_id=user_id,
            goal_name=goal_name,
            target_amount=float(target_amount),
            current_amount=float(current_amount),
            deadline=deadline_date
        )

        db.session.add(goal)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Goal added successfully",
            "id": goal.id
        }), 201

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500