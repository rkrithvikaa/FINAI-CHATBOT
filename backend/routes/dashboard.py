from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Income, Expense, Budget, Goal


# ========================================
# DASHBOARD BLUEPRINT
# ========================================

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/api/dashboard"
)


# ========================================
# DASHBOARD SUMMARY
# GET /api/dashboard
# ========================================

@dashboard_bp.route("", methods=["GET"])
@jwt_required()
def dashboard():

    try:

        # Get logged-in user's ID
        user_id = get_jwt_identity()

        user_id = int(user_id)

        # --------------------------------
        # Get user's income
        # --------------------------------

        incomes = Income.query.filter_by(
            user_id=user_id
        ).all()

        # --------------------------------
        # Get user's expenses
        # --------------------------------

        expenses = Expense.query.filter_by(
            user_id=user_id
        ).all()

        # --------------------------------
        # Get user's budgets
        # --------------------------------

        budgets = Budget.query.filter_by(
            user_id=user_id
        ).all()

        # --------------------------------
        # Get user's goals
        # --------------------------------

        goals = Goal.query.filter_by(
            user_id=user_id
        ).all()

        # --------------------------------
        # Calculate totals
        # --------------------------------

        total_income = sum(
            float(item.amount)
            for item in incomes
        )

        total_expense = sum(
            float(item.amount)
            for item in expenses
        )

        balance = total_income - total_expense

        # --------------------------------
        # Prepare income data
        # --------------------------------

        income_data = []

        for item in incomes:

            income_data.append({
                "id": item.id,
                "amount": float(item.amount),
                "source": item.source,
                "date": item.date.isoformat()
            })

        # --------------------------------
        # Prepare expense data
        # --------------------------------

        expense_data = []

        for item in expenses:

            expense_data.append({
                "id": item.id,
                "amount": float(item.amount),
                "category": item.category,
                "description": item.description or "",
                "date": item.date.isoformat(),
                "payment_method": item.payment_method or ""
            })

        # --------------------------------
        # Prepare budget data
        # --------------------------------

        budget_data = []

        for item in budgets:

            budget_data.append({
                "id": item.id,
                "category": item.category,
                "amount": float(item.amount),
                "month": item.month,
                "year": item.year
            })

        # --------------------------------
        # Prepare goal data
        # --------------------------------

        goal_data = []

        for item in goals:

            goal_data.append({
                "id": item.id,
                "goal_name": item.goal_name,
                "target_amount": float(item.target_amount),
                "current_amount": float(
                    item.current_amount or 0
                ),
                "deadline": (
                    item.deadline.isoformat()
                    if item.deadline
                    else None
                )
            })

        # --------------------------------
        # Return dashboard
        # --------------------------------

        return jsonify({
            "success": True,

            "summary": {
                "total_income": total_income,
                "total_expense": total_expense,
                "balance": balance
            },

            "income": income_data,

            "expenses": expense_data,

            "budgets": budget_data,

            "goals": goal_data

        }), 200

    except Exception as e:

        print("DASHBOARD ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500