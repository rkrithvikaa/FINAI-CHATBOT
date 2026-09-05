from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from database import db
from models import Expense
# ========================================
# EXPENSE BLUEPRINT
# ========================================
expenses_bp = Blueprint(
    "expenses",
    __name__,
    url_prefix="/api/expenses"
)
# ========================================
# ADD EXPENSE
# POST /api/expenses
# ========================================

@expenses_bp.route("", methods=["POST"])
@jwt_required()
def add_expense():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "No data received."
            }), 400

        user_id = int(get_jwt_identity())

        amount = data.get("amount")
        category = data.get("category")
        description = data.get("description", "")
        date_string = data.get("date")
        payment_method = data.get("payment_method", "")

        # -----------------------------
        # Validate
        # -----------------------------

        if amount is None:
            return jsonify({
                "success": False,
                "message": "Amount is required."
            }), 400

        if not category:
            return jsonify({
                "success": False,
                "message": "Category is required."
            }), 400

        if not date_string:
            return jsonify({
                "success": False,
                "message": "Date is required."
            }), 400

        # -----------------------------
        # Convert amount
        # -----------------------------

        try:
            amount = float(amount)

        except (ValueError, TypeError):

            return jsonify({
                "success": False,
                "message": "Amount must be a number."
            }), 400

        # -----------------------------
        # Convert date
        # -----------------------------

        try:

            expense_date = datetime.strptime(
                date_string,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            return jsonify({
                "success": False,
                "message": "Invalid date. Use YYYY-MM-DD."
            }), 400

        # -----------------------------
        # Create expense
        # -----------------------------

        expense = Expense(
            user_id=user_id,
            amount=amount,
            category=category,
            description=description,
            date=expense_date,
            payment_method=payment_method
        )

        db.session.add(expense)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Expense added successfully!",
            "expense": {
                "id": expense.id,
                "amount": expense.amount,
                "category": expense.category,
                "description": expense.description,
                "date": expense.date.isoformat(),
                "payment_method": expense.payment_method
            }
        }), 201

    except Exception as e:

        db.session.rollback()

        print("ADD EXPENSE ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ========================================
# GET EXPENSES
# GET /api/expenses
# ========================================

@expenses_bp.route("", methods=["GET"])
@jwt_required()
def get_expenses():

    try:

        user_id = int(get_jwt_identity())

        expenses = Expense.query.filter_by(
            user_id=user_id
        ).order_by(
            Expense.date.desc()
        ).all()

        result = []

        for expense in expenses:

            result.append({
                "id": expense.id,
                "amount": float(expense.amount),
                "category": expense.category,
                "description": expense.description or "",
                "date": expense.date.isoformat(),
                "payment_method":
                    expense.payment_method or ""
            })

        return jsonify(result), 200

    except Exception as e:

        print("GET EXPENSES ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ========================================
# DELETE EXPENSE
# DELETE /api/expenses/<id>
# ========================================

@expenses_bp.route("/<int:expense_id>", methods=["DELETE"])
@jwt_required()
def delete_expense(expense_id):

    try:

        user_id = int(get_jwt_identity())

        expense = Expense.query.filter_by(
            id=expense_id,
            user_id=user_id
        ).first()

        if not expense:

            return jsonify({
                "success": False,
                "message": "Expense not found."
            }), 404

        db.session.delete(expense)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Expense deleted successfully!"
        }), 200

    except Exception as e:

        db.session.rollback()

        print("DELETE EXPENSE ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500