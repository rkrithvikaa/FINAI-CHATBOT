from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from database import db
from models import Income


# ========================================
# INCOME BLUEPRINT
# ========================================

income_bp = Blueprint(
    "income",
    __name__,
    url_prefix="/api/income"
)


# ========================================
# ADD INCOME
# POST /api/income
# ========================================

@income_bp.route("", methods=["POST"])
@jwt_required()
def add_income():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "No data received."
            }), 400

        user_id = int(get_jwt_identity())

        amount = data.get("amount")
        source = data.get("source")
        date_string = data.get("date")
        notes = data.get("notes", "")

        # --------------------------------
        # Validate
        # --------------------------------

        if amount is None:
            return jsonify({
                "success": False,
                "message": "Amount is required."
            }), 400

        if not source:
            return jsonify({
                "success": False,
                "message": "Source is required."
            }), 400

        if not date_string:
            return jsonify({
                "success": False,
                "message": "Date is required."
            }), 400

        # --------------------------------
        # Convert amount
        # --------------------------------

        try:
            amount = float(amount)

        except (ValueError, TypeError):

            return jsonify({
                "success": False,
                "message": "Amount must be a number."
            }), 400

        # --------------------------------
        # Convert date
        # --------------------------------

        try:

            income_date = datetime.strptime(
                date_string,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            return jsonify({
                "success": False,
                "message": "Invalid date. Use YYYY-MM-DD."
            }), 400

        # --------------------------------
        # Create income
        # --------------------------------

        income = Income(
            user_id=user_id,
            amount=amount,
            source=source,
            date=income_date,
            notes=notes
        )

        db.session.add(income)
        db.session.commit()

        # --------------------------------
        # Response
        # --------------------------------

        return jsonify({
            "success": True,
            "message": "Income added successfully!",
            "income": {
                "id": income.id,
                "amount": float(income.amount),
                "source": income.source,
                "date": income.date.isoformat(),
                "notes": income.notes or ""
            }
        }), 201

    except Exception as e:

        db.session.rollback()

        print("ADD INCOME ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ========================================
# GET INCOME
# GET /api/income
# ========================================

@income_bp.route("", methods=["GET"])
@jwt_required()
def get_income():

    try:

        user_id = int(get_jwt_identity())

        incomes = Income.query.filter_by(
            user_id=user_id
        ).order_by(
            Income.date.desc()
        ).all()

        result = []

        for income in incomes:

            result.append({
                "id": income.id,
                "amount": float(income.amount),
                "source": income.source,
                "date": income.date.isoformat(),
                "notes": income.notes or ""
            })

        return jsonify(result), 200

    except Exception as e:

        print("GET INCOME ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ========================================
# DELETE INCOME
# DELETE /api/income/<id>
# ========================================

@income_bp.route("/<int:income_id>", methods=["DELETE"])
@jwt_required()
def delete_income(income_id):

    try:

        user_id = int(get_jwt_identity())

        income = Income.query.filter_by(
            id=income_id,
            user_id=user_id
        ).first()

        if not income:

            return jsonify({
                "success": False,
                "message": "Income not found."
            }), 404

        db.session.delete(income)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Income deleted successfully!"
        }), 200

    except Exception as e:

        db.session.rollback()

        print("DELETE INCOME ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500