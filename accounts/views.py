from random import randint
from rest_framework.authtoken.models import Token
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.generics import ValidationError, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from accounts.models import User, Code
from accounts.serializers import UserSerializer, EmailSerializer
from utils.verification import code_expiration


class LoginView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            code = Code.objects.filter(user__phone=serializer.validated_data['phone']).exists()

            if not self.request.user.is_active and code and code_expiration(serializer.validated_data['phone']):
                code.delete()
                code = Code.objects.create(user__phone=serializer.validated_data['phone'])
                # todo: send another email
                return Response({'result': 'code has been sent'}, status=status.HTTP_200_OK)
            elif not self.request.user.is_active and code and not code_expiration(serializer.validated_data['phone']):
                return Response({'result': 'insert existed code'}, status=status.HTTP_208_ALREADY_REPORTED)

            user = User.objects.filter(phone=serializer.validated_data['phone']).first()
            if user.phone == serializer.validated_data['phone'] and user.password == serializer.validated_data['password']:
                token = Token.objects.create(user=self.request.user)
            else:
                return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'token': token}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            match serializer.validated_data:
                case 1:
                    return Response({'error': 'user exists'}, status=status.HTTP_400_BAD_REQUEST)

                case 2:
                    return Response({'error': 'password does not match'}, status=status.HTTP_400_BAD_REQUEST)

                case 3:
                    return Response({'error' 'input the degree right'}, status=status.HTTP_400_BAD_REQUEST)

                case 4:
                    return Response({'error': 'fullname'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create(
                full_name=serializer.validated_data['full_name'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                phone=serializer.validated_data['phone'],
                degree=serializer.validated_data.get('degree', None),
                branch=serializer.validated_data.get('branch', None),
            )
            Code.objects.create(user=user, verification_code=randint(10000, 99999))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(APIView):
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data == 0:
                return Response({'error': 'code is expired'}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.filter(phone=serializer.validated_data['phone']).first()
            code = Code.objects.filter(user=user).first()
            if serializer.validated_data['verification_code'] == code:
                code.delete()
                user.is_active = True
                user.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'code is invalid!'}, status=status.HTTP_400_BAD_REQUEST)


