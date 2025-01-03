import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product, PRODUCT_CATEGORIES, PRODUCT_TYPES
from decimal import Decimal


@csrf_exempt
def create_product(request):
    if request.method == "POST":
        try:
            # Parse incoming JSON data
            data = json.loads(request.body)
            product_title = data.get("productTitle")
            product_description = data.get("productDescription")
            product_category = data.get("productCategory")
            product_image = data.get("productImage")
            product_price = data.get("productPrice")
            product_type = data.get("productType")
            print(data)

            # Validate input data
            if not product_title or len(product_title) < 15:
                return JsonResponse(
                    {"message": "Product title must be at least 15 characters long"},
                    status=400,
                )

            if not product_description or len(product_description) < 100:
                return JsonResponse(
                    {
                        "message": "Product description must be at least 100 characters long"
                    },
                    status=400,
                )

            if product_category not in [
                category[0] for category in PRODUCT_CATEGORIES.choices
            ]:
                return JsonResponse({"message": "Invalid product category"}, status=400)

            if not product_image or not product_image.startswith("https"):
                return JsonResponse(
                    {"message": "Invalid product image URL"}, status=400
                )

            try:
                product_price = Decimal(product_price)
                if product_price <= 0:
                    return JsonResponse(
                        {"message": "Product price must be greater than 0"}, status=400
                    )
            except (ValueError, TypeError):
                return JsonResponse({"message": "Invalid product price"}, status=400)

            if product_type not in [type[0] for type in PRODUCT_TYPES.choices]:
                return JsonResponse({"message": "Invalid product type"}, status=400)
            # Create and save the product
            product = Product(
                product_title=product_title,
                product_description=product_description,
                product_category=product_category,
                product_image=product_image,
                product_price=product_price,
                product_type=product_type,
                product_seller_id=request.user_data["id"],
            )
            product.save()

            return JsonResponse(
                {"message": "Product created successfully"},
                status=201,
            )

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON data"}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({"message": str(e)}, status=500)

    return JsonResponse({"message": "Only POST method is allowed"}, status=405)
