from flask import (
    Blueprint,
    render_template,
    g,
    redirect,
    url_for,
    request,
    flash,
    jsonify,
)

from app.auth import login_required

from app.db import get_db

bp = Blueprint("dashboard", __name__)


@bp.route("/")
@login_required
def index():
    user_id = g.user["id"]

    db = get_db()

    meals = db.execute(
        "SELECT pet.name, meal.datetime, meal.quantity, user.username FROM meal JOIN pet ON pet.id = meal.pet_id JOIN user ON user.id = meal.user_id WHERE meal.pet_id IN (SELECT pet_id FROM user_pet WHERE user_pet.user_id = ?) ORDER BY meal.datetime DESC",
        (user_id,),
    ).fetchall()

    pets = db.execute(
        "SELECT pet.id, pet.name FROM pet JOIN user_pet ON pet.id = user_pet.pet_id WHERE user_id = ?",
        (user_id,),
    ).fetchall()

    return render_template("dashboard/home.html", meals=meals, pets=pets)


@bp.route("/add-meal", methods=["POST"])
@login_required
def add_meal():
    user_id = g.user["id"]
    data = request.get_json()
    pet_id = data.get("pet_id")
    quantity = data.get("quantity")

    error = None

    if not pet_id:
        error = "Pet is required."
    elif not quantity:
        error = "Quantity is required."
    elif int(quantity) <= 0:
        error = "Quantity must be more than 0."

    if error is not None:
        return (
            jsonify(
                {
                    "message": error,
                }
            ),
            400,
        )

    db = get_db()

    db.execute(
        "INSERT INTO meal (user_id, pet_id, quantity) VALUES (?, ?, ?)",
        (user_id, pet_id, quantity),
    )
    db.commit()

    return (
        jsonify(
            {
                "message": "Meal added successfully",
            }
        ),
        200,
    )
