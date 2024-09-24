from flask import Blueprint, render_template, g, request

from app.auth import login_required

from app.db import get_db

from app.utils import format_age, default_response, binary_to_base64

bp = Blueprint("dashboard", __name__)


@bp.route("/")
@login_required
def index():
    user_id = g.user["id"]

    db = get_db()

    meals = db.execute(
        "SELECT meal.id, pet.name, pet.id as pet_id, meal.datetime, meal.quantity, user.username FROM meal JOIN pet ON pet.id = meal.pet_id JOIN user ON user.id = meal.user_id WHERE meal.pet_id IN (SELECT pet_id FROM user_pet WHERE user_pet.user_id = ?) ORDER BY meal.datetime DESC",
        (user_id,),
    ).fetchall()

    pets = db.execute(
        "SELECT pet.id, pet.name FROM pet JOIN user_pet ON pet.id = user_pet.pet_id WHERE user_pet.user_id = ?",
        (user_id,),
    ).fetchall()

    return render_template("dashboard/home.html", active="home", meals=meals, pets=pets)


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


@bp.route("/update-meal/<int:id>", methods=["POST"])
@login_required
def update_meal(id):
    user_id = g.user["id"]
    meal_id = id
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

    user_meals = db.execute(
        "SELECT id FROM meal WHERE user_id = ?",
        (user_id,),
    ).fetchall()

    user_pets_ids = []

    for user_pet in user_pets:
        user_pets_ids.append(user_pet["id"])

    if int(pet_id) not in user_pets_ids:
        return default_response(403, "Forbidden")

    user_meals_ids = []

    for user_meal in user_meals:
        user_meals_ids.append(user_meal["id"])

    if meal_id not in user_meals_ids:
        return default_response(403, "Forbidden")

    db.execute(
        "UPDATE meal SET pet_id = ?, quantity = ? WHERE id = ?",
        (pet_id, quantity, meal_id),
    )
    db.commit()

    return default_response(200, "Meal updated successfully")


@bp.route("/pets")
@login_required
def pets():
    user_id = g.user["id"]

    db = get_db()

    pets = db.execute(
        "SELECT pet.* FROM pet JOIN user_pet ON pet.id = user_pet.pet_id WHERE user_pet.user_id = ?",
        (user_id,),
    ).fetchall()

    parsed_pets = []

    for pet in pets:
        parsed_pet = {}

        for key in pet.keys():
            if key == "species":
                parsed_pet[key] = pet[key].capitalize()
            if key == "photo":
                parsed_pet[key] = (
                    binary_to_base64(pet[key])
                    if pet[key]
                    else "static/pet-photo-placeholder.webp"
                )
            else:
                parsed_pet[key] = pet[key]

        parsed_pet["age"] = format_age(pet["birthday"])
        parsed_pets.append(parsed_pet)

    return render_template("dashboard/pets.html", active="pets", pets=parsed_pets)


@bp.route("/add-pet", methods=["POST"])
@login_required
def add_pet():
    user_id = g.user["id"]

    name = request.form.get("name")
    weight = request.form.get("weight")
    species = request.form.get("weight")
    birthday = request.form.get("birthday")
    photo = request.files["photo"] if request.files else None

    photo_blob = photo.read() if photo else None

    if not name:
        return default_response(400, "Name is required.")
    elif not weight:
        return default_response(400, "Weight is required.")
    elif int(weight) <= 0:
        return default_response(400, "Weight must be more than 0.")
    elif not species:
        return default_response(400, "Species is required.")
    elif not birthday:
        return default_response(400, "Birthday is required.")

    db = get_db()

    db.execute(
        "INSERT INTO pet (name, weight, species, birthday, photo, user_id) VALUES (?, ?, ?, ?, ?, ?)",
        (name, weight, species, f"{birthday} 00:00:00", photo_blob, user_id),
    )
    db.commit()

    return default_response(200, "Pet added successfully")
