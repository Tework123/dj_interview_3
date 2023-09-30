from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser
from users.serializers import (UsersGetSerializer, UsersPostSerializer,
                               UsersEditGetSerializer, UsersAuthSerializer)


class UsersView(generics.ListCreateAPIView):
    """
    GET show all users
    POST create new user
    """

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UsersGetSerializer
        else:
            return UsersPostSerializer

    def get_queryset(self):
        return CustomUser.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = UsersPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED, data='Пользователь успешно создан')


class UsersFilterView(generics.ListAPIView):
    """
    GET show user with filter
    """
    serializer_class = UsersGetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        email = self.kwargs['email']
        return CustomUser.objects.filter(email=email)


class UsersOrderView(generics.ListAPIView):
    """
    GET show all users with order_by
    """
    serializer_class = UsersGetSerializer

    def get_queryset(self):
        order_by = self.kwargs['order_by']
        try:
            response = CustomUser.objects.order_by(order_by)
        except Exception as e:
            raise exceptions.NotFound(detail=e)

        return response


class UsersEditView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET show user
    PATCH update user fields
    DELETE delete user
    """
    serializer_class = UsersEditGetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(pk=self.kwargs['pk'])

    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data='Информация успешно обновлена')

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data='Пользователь удален успешно')


class AuthUserView(generics.GenericAPIView):
    """
    POST authorize user
    """
    serializer_class = UsersAuthSerializer

    def post(self, request):
        serializer = UsersAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(CustomUser, email=serializer.validated_data['email'])
        user = authenticate(email=user.email, password=serializer.validated_data['password'])
        if user is None:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data='Данные для авторизации неправильные')

        login(request, user)

        return Response(status=status.HTTP_200_OK, data='Вход выполнен успешно')


class UsersLogoutView(APIView):
    """
     POST logout user
     """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK, data='Выход из аккаунта выполнен успешно')
