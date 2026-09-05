from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database import db
from models import Budget


budget_bp = Blueprint(
    "budget",
    __name__,
    url_prefix="/api/budget"
)


# =========================================================
# HELPER: GET LOGGED-IN USER ID
# =========================================================

def get_current_user_id():
    """
    JWT identity may sometimes be returned as a string.
    Convert it safely to an integer because user_id in
    MySQL is an INT.
    """

    identity = get_jwt_identity()

    try:
        return int(identity)
    except (TypeError, ValueError):
        return None


# =========================================================
# ADD / SET BUDGET
# POST /api/budget
#
# Example JSON:
#
# {
#     "category": "Food",
#     "amount": 5000,
#     "month": 9,
#     "year": 2026
# }
# =========================================================

@budget_bp.route("", methods=["POST"])
@jwt_required()
def add_budget():

    try:
        # -------------------------------------------------
        # GET LOGGED-IN USER
        # -------------------------------------------------

        user_id = get_current_user_id()

        if user_id is None:
            return jsonify({
                "success": False,
                "message": "Invalid user identity."
            }), 401

        # -------------------------------------------------
        # GET JSON
        # -------------------------------------------------

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "No data received."
            }), 400

        category = data.get("category")
        amount = data.get("amount")
        month = data.get("month")
        year = data.get("year")

        # -------------------------------------------------
        # REQUIRED FIELD VALIDATION
        # -------------------------------------------------

        if not category:
            return jsonify({
                "success": False,
                "message": "Budget category is required."
            }), 400

        if amount is None or amount == "":
            return jsonify({
                "success": False,
                "message": "Budget amount is required."
            }), 400

        if month is None or month == "":
            return jsonify({
                "success": False,
                "message": "Budget month is required."
            }), 400

        if year is None or year == "":
            return jsonify({
                "success": False,
                "message": "Budget year is required."
            }), 400

        # -------------------------------------------------
        # CLEAN CATEGORY
        # -------------------------------------------------

        category = str(category).strip()

        if len(category) == 0:
            return jsonify({
                "success": False,
                "message": "Budget category cannot be empty."
            }), 400

        if len(category) > 50:
            return jsonify({
                "success": False,
                "message": "Budget category must be 50 characters or less."
            }), 400

        # -------------------------------------------------
        # CONVERT VALUES
        # -------------------------------------------------

        try:
            amount = float(amount)
            month = int(month)
            year = int(year)

        except (ValueError, TypeError):

            return jsonify({
                "success": False,
                "message": "Invalid amount, month or year."
            }), 400

        # -------------------------------------------------
        # VALIDATE AMOUNT
        # -------------------------------------------------

        if amount <= 0:
            return jsonify({
                "success": False,
                "message": "Budget amount must be greater than 0."
            }), 400

        # -------------------------------------------------
        # VALIDATE MONTH
        # -------------------------------------------------

        if month < 1 or month > 12:
            return jsonify({
                "success": False,
                "message": "Month must be between 1 and 12."
            }), 400

        # -------------------------------------------------
        # VALIDATE YEAR
        # -------------------------------------------------

        if year < 2000 or year > 2100:
            return jsonify({
                "success": False,
                "message": "Please enter a valid year."
            }), 400

        # -------------------------------------------------
        # CHECK WHETHER THIS BUDGET ALREADY EXISTS
        #
        # Same user + same category + same month + same year
        #
        # If it exists, update it instead of adding duplicates.
        # -------------------------------------------------

        existing_budget = Budget.query.filter_by(
            user_id=user_id,
            category=category,
            month=month,
            year=year
        ).first()

        if existing_budget:

            existing_budget.amount = amount

            db.session.commit()

            return jsonify({
                "success": True,
                "message": "Budget updated successfully.",
                "budget": {
                    "id": existing_budget.id,
                    "user_id": existing_budget.user_id,
                    "category": existing_budget.category,
                    "amount": float(existing_budget.amount),
                    "month": existing_budget.month,
                    "year": existing_budget.year
                }
            }), 200

        # -------------------------------------------------
        # CREATE NEW BUDGET
        # -------------------------------------------------

        budget = Budget(
            user_id=user_id,
            category=category,
            amount=amount,
            month=month,
            year=year
        )

        db.session.add(budget)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Budget added successfully.",
            "budget": {
                "id": budget.id,
                "user_id": budget.user_id,
                "category": budget.category,
                "amount": float(budget.amount),
                "month": budget.month,
                "year": budget.year
            }
        }), 201

    except Exception as e:

        db.session.rollback()

        print("ADD BUDGET ERROR:")
        print(e)

        return jsonify({
            "success": False,
            "message": "Failed to add budget.",
            "error": str(e)
        }), 500


# =========================================================
# GET ALL BUDGETS FOR LOGGED-IN USER
# GET /api/budget
# =========================================================

@budget_bp.route("", methods=["GET"])
@jwt_required()
def get_budgets():

    try:
        user_id = get_current_user_id()

        if user_id is None:
            return jsonify({
                "success": False,
                "message": "Invalid user identity."
            }), 401

        budgets = Budget.query.filter_by(
            user_id=user_id
        ).order_by(
            Budget.year.desc(),
            Budget.month.desc(),
            Budget.id.desc()
        ).all()

        result = []

        for budget in budgets:

            result.append({
                "id": budget.id,
                "user_id": budget.user_id,
                "category": budget.category,
                "amount": float(budget.amount),
                "month": budget.month,
                "year": budget.year
            })

        return jsonify({
            "success": True,
            "budgets": result
        }), 200

    except Exception as e:

        print("GET BUDGET ERROR:")
        print(e)

        return jsonify({
            "success": False,
            "message": "Failed to load budgets.",
            "error": str(e)
        }), 500


# =========================================================
# GET ONE BUDGET
# GET /api/budget/<id>
# =========================================================

@budget_bp.route("/<int:budget_id>", methods=["GET"])
@jwt_required()
def get_budget(budget_id):

    try:
        user_id = get_current_user_id()

        if user_id is None:
            return jsonify({
                "success": False,
                "message": "Invalid user identity."
            }), 401

        budget = Budget.query.filter_by(
            id=budget_id,
            user_id=user_id
        ).first()

        if not budget:
            return jsonify({
                "success": False,
                "message": "Budget not found."
            }), 404

        return jsonify({
            "success": True,
            "budget": {
                "id": budget.id,
                "user_id": budget.user_id,
                "category": budget.category,
                "amount": float(budget.amount),
                "month": budget.month,
                "year": budget.year
            }
        }), 200

    except Exception as e:

        print("GET SINGLE BUDGET ERROR:")
        print(e)

        return jsonify({
            "success": False,
            "message": "Failed to load budget.",
            "error": str(e)
        }), 500


# =========================================================
# UPDATE BUDGET
# PUT /api/budget/<id>
# =========================================================

@budget_bp.route("/<int:budget_id>", methods=["PUT"])
@jwt_required()
def update_budget(budget_id):

    try:
        user_id = get_current_user_id()

        if user_id is None:
            return jsonify({
                "success": False,
                "message": "Invalid user identity."
            }), 401

        budget = Budget.query.filter_by(
            id=budget_id,
            user_id=user_id
        ).first()

        if not budget:
            return jsonify({
                "success": False,
                "message": "Budget not found."
            }), 404

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "No data received."
            }), 400

        category = data.get(
            "category",
            budget.category
        )

        amount = data.get(
            "amount",
            budget.amount
        )

        month = data.get(
            "month",
            budget.month
        )

        year = data.get(
            "year",
            budget.year
        )

        category = str(category).strip()

        try:
            amount = float(amount)
            month = int(month)
            year = int(year)

        except (ValueError, TypeError):

            return jsonify({
                "success": False,
                "message": "Invalid amount, month or year."
            }), 400

        if not category:
            return jsonify({
                "success": False,
                "message": "Category is required."
            }), 400

        if len(category) > 50:
            return jsonify({
                "success": False,
                "message": "Category must be 50 characters or less."
            }), 400

        if amount <= 0:
            return jsonify({
                "success": False,
                "message": "Amount must be greater than 0."
            }), 400

        if month < 1 or month > 12:
            return jsonify({
                "success": False,
                "message": "Month must be between 1 and 12."
            }), 400

        if year < 2000 or year > 2100:
            return jsonify({
                "success": False,
                "message": "Invalid year."
            }), 400

        budget.category = category
        budget.amount = amount
        budget.month = month
        budget.year = year

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Budget updated successfully.",
            "budget": {
                "id": budget.id,
                "user_id": budget.user_id,
                "category": budget.category,
                "amount": float(budget.amount),
                "month": budget.month,
                "year": budget.year
            }
        }), 200

    except Exception as e:

        db.session.rollback()

        print("UPDATE BUDGET ERROR:")
        print(e)

        return jsonify({
            "success": False,
            "message": "Failed to update budget.",
            "error": str(e)
        }), 500


# =========================================================
# DELETE BUDGET
# DELETE /api/budget/<id>
# =========================================================

@budget_bp.route("/<int:budget_id>", methods=["DELETE"])
@jwt_required()
def delete_budget(budget_id):

    try:
        user_id = get_current_user_id()

        if user_id is None:
            return jsonify({
                "success": False,
                "message": "Invalid user identity."
            }), 401

        budget = Budget.query.filter_by(
            id=budget_id,
            user_id=user_id
        ).first()

        if not budget:

            return jsonify({
                "success": False,
                "message": "Budget not found."
            }), 404

        db.session.delete(budget)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Budget deleted successfully."
        }), 200

    except Exception as e:

        db.session.rollback()

        print("DELETE BUDGET ERROR:")
        print(e)

        return jsonify({
            "success": False,
            "message": "Failed to delete budget.",
            "error": str(e)
        }), 500