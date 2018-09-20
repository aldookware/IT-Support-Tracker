from rest_framework import serializers
from biz.models import Engineer, Client, User, Issue


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
    url = serializers.HyperlinkedIdentityField(
        view_name='client-api:detail',
        lookup_field='pk'
    )

    class Meta:
        model = Client
        fields = (
            'id',
            'url',
            'title',
            'address',
        )


class IssueListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='issue-api:detail',
        lookup_field='pk',

    )

    class Meta:
        model = Issue
        fields = (
            'url',
            'id',
            'subject',
            'client',
            'status',
            'expected_date',
            'date_resolved',
            'issue_description',
            'created_by',
            'created_at',
        )


class IssueCreateUpdateSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='issue-api:detail',
        lookup_field='pk',
    )

    class Meta:
        model = Issue
        fields = (
            'url',
            'subject',
            'client',
            'status',
            'expected_date',
            'date_resolved',
            'issue_description',
            'created_by',
            'created_at',
        )
