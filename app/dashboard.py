from flask import Blueprint, render_template, g

from app.auth import login_required

from app.db import get_db

bp = Blueprint("dashboard", __name__)


@bp.route("/")
@login_required
def index():
    db = get_db()

    meals = db.execute(
        "SELECT pet.name, meal.datetime, meal.quantity, user.username FROM meal JOIN pet ON pet.id = meal.pet_id JOIN user ON user.id = meal.user_id WHERE meal.pet_id IN (SELECT pet_id FROM user_pet WHERE user_pet.user_id = ?)",
        (g.user["id"],),
    )

    return render_template("dashboard/home.html", meals=meals)
