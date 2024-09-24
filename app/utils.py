from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask import jsonify
import magic
import mimetypes
import base64


def get_age(birthday):
    return relativedelta(datetime.now(), birthday)


def format_age(birthday):
    age = get_age(birthday)
    years = age.years
    months = age.months
    days = age.days

    formatted = ""

    if years > 1:
        formatted = f"{years} years "
    elif years == 1:
        formatted = f"{years} year "

    if months > 1:
        formatted += f"{months} months "
    elif months == 1:
        formatted += f"{months} month "

    if days > 1:
        formatted += f"{days} days"
    elif days == 1:
        formatted += f"{days} day"

    return formatted.strip()


def default_response(status, message):
    return (
        jsonify(
            {
                "message": message,
            }
        ),
        status,
    )

def binary_to_base64(data):
    extension = mimetypes.guess_extension(magic.Magic(mime=True).from_buffer(data))
    return f"data:image/{extension};base64,{base64.b64encode(data).decode("utf-8")}"

