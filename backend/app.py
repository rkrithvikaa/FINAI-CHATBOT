from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from config import Config
from database import db

from models import (
    User,
    Income,
    Expense,
    Budget,
    Goal,
    ChatHistory
)

from routes.auth import auth_bp
from routes.income import income_bp
from routes.expenses import expenses_bp
from routes.budget import budget_bp
from routes.goals import goals_bp
from routes.chatbot import chatbot_bp
from routes.dashboard import dashboard_bp


app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

jwt = JWTManager(app)

CORS(app)


# ========================================
# REGISTER ROUTES
# ========================================

app.register_blueprint(auth_bp)
app.register_blueprint(income_bp)
app.register_blueprint(expenses_bp)
app.register_blueprint(budget_bp)
app.register_blueprint(goals_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(dashboard_bp)


# ========================================
# HOME
# ========================================

@app.route("/")
def home():

    return {
        "success": True,
        "message": "FinAI Backend is running!"
    }


# ========================================
# HEALTH
# ========================================

@app.route("/api/health")
def health():

    return {
        "success": True,
        "message": "Backend and API are working!"
    }


# ========================================
# CREATE TABLES
# ========================================

with app.app_context():

    db.create_all()

    print(
        "Database tables created/verified successfully!"
    )


# ========================================
# RUN
# ========================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )