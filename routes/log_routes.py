from flask import Blueprint, jsonify, request
from database.database import get_db
from services.calorie_calc import CalorieCalc

log_bp = Blueprint("log", __name__)

@log_bp.route("/daily", methods=["GET"])
def get_daily_logs():
    user_id = request.args.get("user_id")
    date    = request.args.get("date")

    if not user_id or not date:
        return jsonify({"error": "user_id and date required"}), 400

    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM meals WHERE user_id = ? AND date = ?",
        (user_id, date)
    ).fetchall()
    conn.close()

    meals = [dict(row) for row in rows]
    total = CalorieCalc.calculate_total(meals)

    return jsonify({
        "date": date,
        "total_calories": total,
        "meals": meals
    }), 200