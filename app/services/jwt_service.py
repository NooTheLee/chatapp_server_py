import jwt
from datetime import datetime, timedelta, UTC
from flask import current_app


def generate_jwt(user):
    secret = current_app.config["JWT_SECRET_KEY"]
    issuer = current_app.config["JWT_ISSUER"]
    audiance = current_app.config["JWT_AUDIENCE"]
    expires_in = int(current_app.config["JWT_EXPIRES_HOURS"])

    payload = {
        "sub": str(user.id),
        "name": user.username,
        "email": user.email,
        "exp": datetime.now(UTC) + timedelta(hours=expires_in),
        "iss": issuer,
        "aud": audiance,
    }

    token = jwt.encode(payload, secret, algorithm="HS256")
    return token
