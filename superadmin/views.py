from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .serializers import ManageUserSerializer
from .permissions import IsSuperAndStuffUser
from accounts.models import User


class ManageUsers(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_superuser=False, is_staff=False)
    serializer_class = ManageUserSerializer
    permission_classes = (IsSuperAndStuffUser,)
    lookup_field = 'pk'
    http_method_names = ['get', 'put',]

    def list(self, request, *args, **kwargs):
        ser = self.serializer_class(self.queryset, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        user = self.get_object()
        ser = self.serializer_class(user, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None, *args, **kwargs):
        user = self.get_object()
        ser = self.serializer_class(user, partial=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    class ManageArticles(viewsets.ModelViewSet):
        queryset = User.objects.filter(is_superuser=False, is_staff=False)
        serializer_class = ManageUserSerializer
        permission_classes = (IsSuperAndStuffUser,)
        lookup_field = 'pk'
        http_method_names = ['get', 'put', 'post']

        def list(self, request, *args, **kwargs):
            ser = self.serializer_class(self.queryset, many=True)
            return Response(ser.data, status=status.HTTP_200_OK)

        def create(self, request, *args, **kwargs):
            ser = self.serializer_class(data=request.data)
            if ser.is_valid():
                user = ser.save()  # Save the new user instance
                return Response(self.serializer_class(user).data, status=status.HTTP_201_CREATED)
            else:
                return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

        def update(self, request, pk=None, *args, **kwargs):
            user = self.get_object()
            ser = self.serializer_class(user, data=request.data, partial=True)
            if ser.is_valid():
                ser.save()
                return Response(ser.data, status=status.HTTP_200_OK)
            else:
                return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

        def retrieve(self, request, pk=None, *args, **kwargs):
            user = self.get_object()
            ser = self.serializer_class(user, partial=True)
            return Response(ser.data, status=status.HTTP_200_OK)

