from django.conf import settings
import jwt


def generate_access_token(user):
    user_details = {
        "username": user.username,
        "email": user.email,
        "user_id": user.id,
    }
    access_token = jwt.encode(
        user_details, settings.JWT_ACCESS_TOKEN_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return access_token
