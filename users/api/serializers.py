from rest_framework import serializers
from users.models import Engineer, Client, User, Issue


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',)


class EngineerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engineer
        fields = (
            'user',
            'url',
            'bio',
            'location',)


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            'id',
            'title',
            'address',
        )


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = (
            'id',
            'title',
            'client',
            'status',
            'expected_date',
            'date_resolved',
            'issue_description',
            'created_by',
            'created_at',
        )
