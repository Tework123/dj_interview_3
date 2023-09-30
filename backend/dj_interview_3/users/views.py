from django.contrib.auth.models import User
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from users.serializers import UsersGetSerializer, UsersPostSerializer, UsersEditGetSerializer


class UsersView(generics.ListCreateAPIView):
    """
    GET Show all users
    POST Create new user
    """

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


# короче так, завтра быстро переписываем модель юзера как в социальной сети по емайлу
# пишем тесты и отправляем это задание.

# это в ветке main

# jwt я так понял должен запросы на обновление отправлять с фронтенда
# попробуем с обычным токеном поиграться и djoser (в отдельной ветке)

class UsersEditView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET Show user
    PATCH Update user fields
    DELETE Delete user
    """
    serializer_class = UsersEditGetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(pk=self.kwargs['pk'])

    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data='Информация успешно обновлена')

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data='Пользователь удален успешно')

# сделать команду для заполнения бд
# разобраться с djoser
# переделать user на email с djoserom
