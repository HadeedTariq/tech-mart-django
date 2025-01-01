from django.conf import settings
from django.http import JsonResponse
import jwt


class SellerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/seller/"):
            access_token = request.COOKIES.get("access_token")
            if access_token:
                user_details = jwt.decode(
                    access_token,
                    settings.JWT_ACCESS_TOKEN_SECRET,
                    algorithms=[settings.JWT_ALGORITHM],
                )
                if user_details.get("role") != "seller":
                    return JsonResponse({"message": "Unauthorized"}, status=401)
                response = self.get_response(request)
                return response
            else:
                return JsonResponse({"message": "Access token not found."}, status=401)
