import json
from django.conf import settings
from django.http import JsonResponse
import jwt
from .utils import generate_access_token
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from .models import User


@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return JsonResponse({"message": "All fields are required."}, status=400)

        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({"message": "Invalid email address."}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"message": "Username already exists."}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"message": "Email already exists."}, status=400)

        user = User.objects.create(
            username=username,
            email=email,
            password=password,
        )
        return JsonResponse({"message": "User Registered Successfully"}, status=201)

    return JsonResponse({"message": "Invalid request method."}, status=405)


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return JsonResponse(
                {"message": "Email and password are required."}, status=400
            )

        user = User.objects.filter(email=email).first()
        if user and user.is_correct_password(password, user.password):
            access_token = generate_access_token(user)
            response = JsonResponse({"message": "Login Successful"})
            response.set_cookie("access_token", access_token)
            return response
        return JsonResponse({"message": "Invalid credentials"}, status=401)


def get_user(request):
    access_token = request.COOKIES.get("access_token")
    if access_token:
        try:
            user_details = jwt.decode(
                access_token,
                settings.JWT_ACCESS_TOKEN_SECRET,
                algorithms=[settings.JWT_ALGORITHM],
            )
            return JsonResponse({"user": user_details})
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "Access token expired."}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"message": "Invalid access token."}, status=401)
    else:
        return JsonResponse({"message": "Access token not found."}, status=401)


@csrf_exempt
def logout_user(request):
    if request.method == "POST":
        response = JsonResponse({"message": "Logged out successfully"})
        response.delete_cookie("access_token")
        return response
