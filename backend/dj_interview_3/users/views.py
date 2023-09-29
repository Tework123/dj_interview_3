from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response

from users.serializers import UsersGetSerializer, UsersPostSerializer, UsersEditGetSerializer


class UsersView(generics.ListCreateAPIView):
    """"""

    # permission_classes = None

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UsersGetSerializer
        else:
            return UsersPostSerializer

    def get_queryset(self):
        return User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = UsersPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED, data='Пользователь успешно создан')


class UsersEditView(generics.RetrieveUpdateDestroyAPIView):
    """"""
    serializer_class = UsersEditGetSerializer

    # permission_classes = None

    def get_queryset(self):
        return User.objects.filter(pk=self.kwargs['pk'])

    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data='Информация успешно обновлена')

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data='Пользователь удален успешно')


