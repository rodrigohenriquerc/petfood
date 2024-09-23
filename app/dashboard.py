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
        "SELECT meal.id, pet.name, meal.datetime, meal.quantity, user.username FROM meal JOIN pet ON pet.id = meal.pet_id JOIN user ON user.id = meal.user_id WHERE meal.pet_id IN (SELECT pet_id FROM user_pet WHERE user_pet.user_id = ?) ORDER BY meal.datetime DESC",
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

    if not pet_id:
        return default_response(400, "Pet is required.")
    elif not quantity:
        return default_response(400, "Quantity is required.")
    elif int(quantity) <= 0:
        return default_response(400, "Quantity must be more than 0.")

    db = get_db()

    user_pets = db.execute(
        "SELECT pet_id as id FROM user_pet WHERE user_id = ?",
        (user_id,),
    ).fetchall()

    user_pets_ids = []

    for user_pet in user_pets:
        user_pets_ids.append(user_pet["id"])

    if int(pet_id) not in user_pets_ids:
        return default_response(403, "Forbidden")

    db.execute(
        "INSERT INTO meal (user_id, pet_id, quantity) VALUES (?, ?, ?)",
        (user_id, pet_id, quantity),
    )
    db.commit()

    return default_response(200, "Meal added successfully")


@bp.route("/remove-meal/<int:id>", methods=["POST"])
@login_required
def remove_meal(id):
    user_id = g.user["id"]
    meal_id = id

    if not meal_id:
        return default_response(400, "Meal is required.")

    db = get_db()

    user_meals = db.execute(
        "SELECT id FROM meal WHERE pet_id IN (SELECT pet_id FROM user_pet WHERE user_id = ?)",
        (user_id,),
    )

    user_meals_ids = []

    for user_meal in user_meals:
        user_meals_ids.append(user_meal["id"])

    if meal_id not in user_meals_ids:
        return default_response(403, "Forbidden.")

    db.execute(
        "DELETE FROM meal WHERE id = ?",
        (meal_id,),
    )
    db.commit()

    return default_response(200, "Meal successfully deleted.")


def default_response(status, message):
    return (
        jsonify(
            {
                "message": message,
            }
        ),
        status,
    )
