from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render
from django.http import JsonResponse
from random import randrange
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.views import generic
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile, Avatar
from .serializers import ProfileSerializer

User = get_user_model()

def banners(request):
    data = [
        {
            "id": "123",
            "category": 55,
            "price": 500.67,
            "count": 12,
            "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
            "title": "video card",
            "description": "description of the product",
            "freeDelivery": True,
            "images": [
                {
                    "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                    "alt": "any alt text",
                }
            ],
            "tags": [
                "string"
            ],
            "reviews": 5,
            "rating": 4.6
        },
    ]
    return JsonResponse(data, safe=False)

def categories(request):
    data = [
         {
             "id": 123,
             "title": "video card",
             "image": {
                "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                 "alt": "Image alt string"
             },
             "subcategories": [
                 {
                     "id": 123,
                     "title": "video card",
                     "image": {
                            "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                            "alt": "Image alt string"
                     }
                 }
             ]
         }
     ]
    return JsonResponse(data, safe=False)


def catalog(request):
    data = {
         "items": [
                 {
                     "id": 123,
                     "category": 123,
                     "price": 500.67,
                     "count": 12,
                     "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                     "title": "video card",
                     "description": "description of the product",
                     "freeDelivery": True,
                     "images": [
                            {
                                "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                                "alt": "hello alt",
                            }
                     ],
                     "tags": [
                            {
                                "id": 0,
                                "name": "Hello world"
                            }
                     ],
                     "reviews": 5,
                     "rating": 4.6
                 }
         ],
         "currentPage": randrange(1, 4),
         "lastPage": 3
     }
    return JsonResponse(data)

def productsPopular(request):
    data = [
        {
            "id": "123",
            "category": 55,
            "price": 500.67,
            "count": 12,
            "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
            "title": "video card",
            "description": "description of the product",
            "freeDelivery": True,
            "images": [
                    {
                        "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                        "alt": "hello alt",
                    }
             ],
             "tags": [
                    {
                        "id": 0,
                        "name": "Hello world"
                    }
             ],
            "reviews": 5,
            "rating": 4.6
        }
    ]
    return JsonResponse(data, safe=False)

def productsLimited(request):
    data = [
        {
            "id": "123",
            "category": 55,
            "price": 500.67,
            "count": 12,
            "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
            "title": "video card",
            "description": "description of the product",
            "freeDelivery": True,
            "images": [
                    {
                        "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                        "alt": "hello alt",
                    }
             ],
             "tags": [
                    {
                        "id": 0,
                        "name": "Hello world"
                    }
             ],
            "reviews": 5,
            "rating": 4.6
        }
    ]
    return JsonResponse(data, safe=False)

def sales(request):
    data = {
        'items': [
            {
                "id": 123,
                "price": 500.67,
                "salePrice": 200.67,
                "dateFrom": "05-08",
                "dateTo": "05-20",
                "title": "video card",
                "images": [
                        {
                            "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                            "alt": "hello alt",
                        }
                 ],
            }
        ],
        'currentPage': randrange(1, 4),
        'lastPage': 3,
    }
    return JsonResponse(data)

def basket(request):
    if(request.method == "GET"):
        print('[GET] /api/basket/')
        data = [
            {
                "id": 123,
                "category": 55,
                "price": 500.67,
                "count": 12,
                "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                "title": "video card",
                "description": "description of the product",
                "freeDelivery": True,
                "images": [
                        {
                            "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                            "alt": "hello alt",
                        }
                 ],
                 "tags": [
                        {
                            "id": 0,
                            "name": "Hello world"
                        }
                 ],
                "reviews": 5,
                "rating": 4.6
            },
            {
                "id": 124,
                "category": 55,
                "price": 201.675,
                "count": 5,
                "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                "title": "video card",
                "description": "description of the product",
                "freeDelivery": True,
                "images": [
                        {
                            "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                            "alt": "hello alt",
                        }
                 ],
                 "tags": [
                        {
                            "id": 0,
                            "name": "Hello world"
                        }
                 ],
                "reviews": 5,
                "rating": 4.6
            }
        ]
        return JsonResponse(data, safe=False)

    elif (request.method == "POST"):
        body = json.loads(request.body)
        id = body['id']
        count = body['count']
        print('[POST] /api/basket/   |   id: {id}, count: {count}'.format(id=id, count=count))
        data = [
            {
                "id": id,
                "category": 55,
                "price": 500.67,
                "count": 13,
                "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                "title": "video card",
                "description": "description of the product",
                "freeDelivery": True,
                "images": [
                        {
                            "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                            "alt": "hello alt",
                        }
                 ],
                 "tags": [
                        {
                            "id": 0,
                            "name": "Hello world"
                        }
                 ],
                "reviews": 5,
                "rating": 4.6
            }
        ]
        return JsonResponse(data, safe=False)

    elif (request.method == "DELETE"):
        body = json.loads(request.body)
        id = body['id']
        print('[DELETE] /api/basket/')
        data = [
            {
            "id": id,
            "category": 55,
            "price": 500.67,
            "count": 11,
            "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
            "title": "video card",
            "description": "description of the product",
            "freeDelivery": True,
            "images": [
                    {
                        "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                        "alt": "hello alt",
                    }
             ],
             "tags": [
                    {
                        "id": 0,
                        "name": "Hello world"
                    }
             ],
            "reviews": 5,
            "rating": 4.6
            }
        ]
        return JsonResponse(data, safe=False)


class SignInView(APIView):
    def post(self, request):
        serialized_data = list(request.POST.keys())[0]
        user_data = json.loads(serialized_data)
        username = user_data.get("username")
        password = user_data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SignUpView(APIView):
    def post(self, request):
        serialized_data = list(request.data.keys())[0]
        user_data = json.loads(serialized_data)
        name = user_data.get("name")
        username = user_data.get("username")
        password = user_data.get("password")

        try:
            user = User.objects.create_user(username=username, password=password)
            profile = Profile.objects.create(user=user, fullName=name)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def signOut(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)


def product(request, id):
    data = {
        "id": 123,
        "category": 55,
        "price": 500.67,
        "count": 12,
        "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
        "title": "video card",
        "description": "description of the product",
        "fullDescription": "full description of the product",
        "freeDelivery": True,
        "images": [
                {
                    "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                    "alt": "hello alt",
                }
         ],
         "tags": [
                {
                    "id": 0,
                    "name": "Hello world"
                }
         ],
        "reviews": [
            {
                "author": "Annoying Orange",
                "email": "no-reply@mail.ru",
                "text": "rewrewrwerewrwerwerewrwerwer",
                "rate": 4,
                "date": "2023-05-05 12:12"
            }
        ],
        "specifications": [
            {
                "name": "Size",
                "value": "XL"
            }
        ],
        "rating": 4.6
    }
    return JsonResponse(data)

def tags(request):
    data = [
        { "id": 0, "name": 'tag0' },
        { "id": 1, "name": 'tag1' },
        { "id": 2, "name": 'tag2' },
    ]
    return JsonResponse(data, safe=False)

def productReviews(request, id):
    data = [
    {
      "author": "Annoying Orange",
      "email": "no-reply@mail.ru",
      "text": "rewrewrwerewrwerwerewrwerwer",
      "rate": 4,
      "date": "2023-05-05 12:12"
    },
    {
      "author": "2Annoying Orange",
      "email": "no-reply@mail.ru",
      "text": "rewrewrwerewrwerwerewrwerwer",
      "rate": 5,
      "date": "2023-05-05 12:12"
    },
    ]
    return JsonResponse(data, safe=False)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePasswordView(APIView):
    def post(self, request):
        user = request.user
        old_password = request.data.get("currentPassword")
        new_password = request.data.get("newPassword")
        if not user.check_password(old_password):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user.password = make_password(new_password)
        user.save()
        return Response(status=status.HTTP_200_OK)


def orders(request):
    if(request.method == 'GET'):
        data = [
            {
        "id": 123,
        "createdAt": "2023-05-05 12:12",
        "fullName": "Annoying Orange",
        "email": "no-reply@mail.ru",
        "phone": "88002000600",
        "deliveryType": "free",
        "paymentType": "online",
        "totalCost": 567.8,
        "status": "accepted",
        "city": "Moscow",
        "address": "red square 1",
        "products": [
          {
            "id": 123,
            "category": 55,
            "price": 500.67,
            "count": 12,
            "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
            "title": "video card",
            "description": "description of the product",
            "freeDelivery": True,
            "images": [
              {
                "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                "alt": "Image alt string"
              }
            ],
            "tags": [
              {
                "id": 12,
                "name": "Gaming"
              }
            ],
            "reviews": 5,
            "rating": 4.6
          }
        ]
      },
            {
        "id": 123,
        "createdAt": "2023-05-05 12:12",
        "fullName": "Annoying Orange",
        "email": "no-reply@mail.ru",
        "phone": "88002000600",
        "deliveryType": "free",
        "paymentType": "online",
        "totalCost": 567.8,
        "status": "accepted",
        "city": "Moscow",
        "address": "red square 1",
        "products": [
          {
            "id": 123,
            "category": 55,
            "price": 500.67,
            "count": 12,
            "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
            "title": "video card",
            "description": "description of the product",
            "freeDelivery": True,
            "images": [
              {
                "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                "alt": "Image alt string"
              }
            ],
            "tags": [
              {
                "id": 12,
                "name": "Gaming"
              }
            ],
            "reviews": 5,
            "rating": 4.6
          }
        ]
      }
        ]
        return JsonResponse(data, safe=False)

    elif(request.method == 'POST'):
        data = {
            "orderId": 123,
        }
        return JsonResponse(data)

    return HttpResponse(status=500)

def order(request, id):
    if(request.method == 'GET'):
        data = {
            "id": 123,
            "createdAt": "2023-05-05 12:12",
            "fullName": "Annoying Orange",
            "email": "no-reply@mail.ru",
            "phone": "88002000600",
            "deliveryType": "free",
            "paymentType": "online",
            "totalCost": 567.8,
            "status": "accepted",
            "city": "Moscow",
            "address": "red square 1",
            "products": [
                {
                    "id": 123,
                    "category": 55,
                    "price": 500.67,
                    "count": 12,
                    "date": "Thu Feb 09 2023 21:39:52 GMT+0100 (Central European Standard Time)",
                    "title": "video card",
                    "description": "description of the product",
                    "freeDelivery": True,
                    "images": [
                        {
                        "src": "https://proprikol.ru/wp-content/uploads/2020/12/kartinki-ryabchiki-14.jpg",
                        "alt": "Image alt string"
                        }
                    ],
                    "tags": [
                        {
                        "id": 12,
                        "name": "Gaming"
                        }
                    ],
                    "reviews": 5,
                    "rating": 4.6
                },
            ]
        }
        return JsonResponse(data)

    elif(request.method == 'POST'):
        data = { "orderId": 123 }
        return JsonResponse(data)

    return HttpResponse(status=500)

def payment(request, id):
    print('qweqwewqeqwe', id)
    return HttpResponse(status=200)


def updateAvatar(request):
    if request.method == "POST":
        profile = Profile.objects.get(user=request.user)
        avatar = Avatar.objects.get_or_create(src=request.FILES["avatar"])[0]
        profile.avatar = avatar
        profile.save()
        return HttpResponse(status=status.HTTP_200_OK)
    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
