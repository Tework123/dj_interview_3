from django.contrib.auth.models import User
from rest_framework import serializers

from users.models import CustomUser


class UsersGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email']


class UsersPostSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class UsersEditGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name',
                  'phone', 'city', 'about_me', 'date_of_birth', 'date_joined']


class UsersEditPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name',
                  'phone', 'city', 'about_me', 'date_of_birth']


class UsersAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
