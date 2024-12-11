from random import randint
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import User, Code
from accounts.serializers import UserSerializer, EmailSerializer, LoginSerializer, AccountManagementSerializer
from utils.verification import code_expiration
from django.core.mail import send_mail
from scientificlab.settings import EMAIL_HOST_USER
from rest_framework.permissions import IsAuthenticated
from django.template.loader import render_to_string


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            code = Code.objects.filter(user__phone=serializer.validated_data['phone']).last()
            user = User.objects.filter(phone=serializer.validated_data['phone']).first()
            if not user:
                return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
            if user.phone == serializer.validated_data['phone'] and user.password == serializer.validated_data['password']:
                if not user.is_active and code and code_expiration(serializer.validated_data['phone']):
                    code.delete()
                    code = Code.objects.create(user=user, verification_code=randint(10000, 99999))
                    message = render_to_string('verify-code.html', {'code': code})
                    send_mail("your verification code", message, EMAIL_HOST_USER, [user.email], html_message=message)
                    return Response({'result': 'code has been sent'}, status=status.HTTP_200_OK)

                elif not user.is_active and not code:
                    code = Code.objects.create(user=user, verification_code=randint(10000, 99999))
                    message = render_to_string('verify-code.html', {'code': code})
                    send_mail("your verification code", message, EMAIL_HOST_USER, [user.email],
                              html_message=message)
                    return Response({'result': 'code has been sent'}, status=status.HTTP_200_OK)

                elif not user.is_active and code and not code_expiration(serializer.validated_data['phone']):
                    return Response({'result': 'insert existed code'}, status=status.HTTP_208_ALREADY_REPORTED)

                elif user.is_active:
                    old_token = Token.objects.filter(user=user).first()
                    if old_token:
                        old_token.delete()
                    token = Token.objects.create(user=user)
                    return Response({'token': token.key, 'superadmin': user.is_superuser}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'some error occurred'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

            user = User.objects.create(
                full_name=serializer.validated_data['full_name'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                phone=serializer.validated_data['phone'],
                degree=serializer.validated_data.get('degree', None),
                branch=serializer.validated_data.get('branch', None),
            )
            code = Code.objects.create(user=user, verification_code=randint(10000, 99999))
            message = render_to_string('verify-code.html', {'code': code})
            send_mail("your verification code", message, EMAIL_HOST_USER, [user.email],
                      html_message=message)
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
            code = Code.objects.filter(user=user).last()
            if int(serializer.validated_data['verification_code']) == int(code.verification_code):
                code.delete()
                user.is_active = True
                user.save()
                token = Token.objects.create(user=user)

                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'code is invalid!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = request.auth
            token.delete()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def change_pass(self, request, user, old_pass, new_pass):
        if user.check_password(old_pass):
            user.set_password(new_pass)
            user.save()
            return Response({"detail": "Password has been changed."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Incorrect password."}, status=status.HTTP_400_BAD_REQUEST)


class AccountManagementView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountManagementSerializer

    def get(self, request, hash_id):
        user = User.objects.filter(hash_identifier=hash_id)
        if not user:
            return Response({'error': 'Oops sorry'}, status=status.HTTP_404_NOT_FOUND)
        ser = self.serializer_class(user.get(), partial=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def put(self, request, hash_id):
        user = User.objects.get(hash_identifier=hash_id)
        ser = self.serializer_class(user, data=request.data, partial=True)
        if ser.is_valid():
            if user_pass := ser.validated_data.get('new_password', None):
                password = ChangePasswordView()
                pass_func = password.change_pass(user=user, old_pass=ser.validated_data.get('password', None), request=request
                                     , new_pass=user_pass)
                return pass_func
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
