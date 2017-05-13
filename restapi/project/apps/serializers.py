# -*- coding: utf-8 -*-
from calendar import timegm
from datetime import datetime

from rest_framework import serializers

from rest_framework_jwt.settings import api_settings

from .models import User
from .models import Resume
from .models import Keyword

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'last_name',
            'second_last_name',
            'bio',
            'data',
            'email',
            'birthday',
            'gender',
            'phone',
            'address',
            'avatar',
            'avatar_thumbnail',
            'is_staff',
            'is_active',
            'register_date',
            'last_modify_date'
        )

    def save(self, request, validated_data):
        """
        Create register in table's user and register.
        """
        # Create user
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['username'].encode('utf-8')
        )

        return user


class RegistrationResultSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'last_name',
            'second_last_name',
            'bio',
            'data',
            'email',
            'birthday',
            'gender',
            'phone',
            'address',
            'avatar',
            'avatar_thumbnail',
            'is_staff',
            'is_active',
            'register_date',
            'last_modify_date',
            'token'
        )

    def get_token(self, obj):
        """
        Create token to user when user register.
        """

        user = User.objects.get(email=obj.email)

        payload = jwt_payload_handler(user)

        if api_settings.JWT_ALLOW_REFRESH:
            payload['orig_iat'] = timegm(
                datetime.utcnow().utctimetuple()
            )

        token = jwt_encode_handler(payload)

        return token


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'last_name',
            'second_last_name',
            'bio',
            'data',
            'email',
            'birthday',
            'gender',
            'phone',
            'address',
            'avatar',
            'avatar_thumbnail',
            'is_staff',
            'is_active',
            'register_date',
            'last_modify_date'
        )

class KeywordSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Keyword
        fields = (
            'id',
            'keyword'
        )

class ResumeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Resume
        fields = (
            'id',
            'title',
            'user',
            'date',
            'resume',
            'resume_file',
            'request_date',
            'keywords',
            'status'
        )

class ResumeDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Resume
        fields = (
            'id',
            'title',
            'user',
            'date',
            'resume',
            'resume_file',
            'request_date',
            'keywords',
            'status'
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)