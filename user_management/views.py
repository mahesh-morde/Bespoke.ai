from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json,random
from botocore.exceptions import ClientError
from rest_framework.decorators import api_view
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import UserCredentials, Catalog
from django.core.exceptions import ObjectDoesNotExist


@method_decorator(csrf_exempt, name='dispatch')
class CreateUserView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))

        #checking mandatary fields
        if 'customer_name' not in data or 'username' not in data or 'password' not in data:
            return JsonResponse({'error': 'Mandatory fields missing'}, status=400)

        try:
            # Check if username is duplicate
            existing_user = UserCredentials.objects.get(username=data['username'])
            return JsonResponse({'error': 'Username already exists'}, status=400)
        except UserCredentials.DoesNotExist:
            pass

        # Store record in the database
        user = UserCredentials(**data)
        user.save()

        return JsonResponse({'message': 'User created successfully'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class ProductSearchView(View):
    def get(self, request, *args, **kwargs):
        search_keyword = request.GET.get('search_keyword', '')
        price_min = request.GET.get('price_min', None)
        price_max = request.GET.get('price_max', None)

        #print(f"Search Keyword: {search_keyword}, Price Min: {price_min}, Price Max: {price_max}")
        try:
            # Apply keyword search
            queryset = Catalog.objects.filter(
                Q(product_description__icontains=search_keyword) | Q(brand_name__icontains=search_keyword)
            )

            # Apply price range filter
            if price_min is not None and price_max is not None:
                queryset = queryset.filter(price__range=(price_min, price_max))

            # Sort and get top 10 products based on rank
            queryset = queryset.order_by('rank')[:10]

            #print(f"Number of items in queryset: {len(queryset)}")


            # Serialize and return the data
            data = [
                {
                    "product_id": item.product_id,
                    "product_category": item.product_category,
                    "rank": item.rank,
                    "brand_name": item.brand_name,
                    "product_description": item.product_description,
                    "price": item.price,
                    "image_link": item.image_link
                }
                for item in queryset
            ]
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": "An error occurred during data retrieval."}, status=500)

        print("Debug: Data before response", data)
        return JsonResponse({"data": data}, content_type="application/json")
        

def recommend_products(request):
    username = request.GET.get('username')
    print("DEBUG: Requested username -", username)

    try:
        user = UserCredentials.objects.get(username=username)
        preferred_category = user.preferred_category

        print("DEBUG: User -", user)
        print("DEBUG: Preferred category -", preferred_category)

        # Retrieve products based on the preferred category
        products = Catalog.objects.filter(product_category=preferred_category).order_by('rank')[:10]

        # If no products are found in the preferred category, return random 10 products
        if not products:
            all_products = list(Catalog.objects.all())
            if all_products:
                products = random.sample(all_products, min(10, len(all_products)))

        print("DEBUG: Retrieved Products -", products)

        result = []
        for product in products:
            result.append({
                'product_id': product.product_id,
                'product_category': product.product_category,
                'rank': product.rank,
                'brand_name': product.brand_name,
                'product_description': product.product_description,
                'price': str(product.price),
                'image_link': product.image_link,
            })

        print(f"DEBUG: Result - {result}")

        return JsonResponse(result, safe=False)

    except UserCredentials.DoesNotExist:
        print("DEBUG: User not found")
        return JsonResponse({'error': 'User not found'}, status=404)