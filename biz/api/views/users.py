from django.shortcuts import get_object_or_404, get_list_or_404

from biz.models import Engineer, Client, User
from biz.api.serializers import UserSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# write individual views to handle requests
@api_view(['GET', 'POST'])
def user_list(request):
    """
    API Endpoint Used to get all biz or created a single user based on the request
    """
    if request.method == 'GET':
        users = get_list_or_404(User)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    """
    API Endpoint used to retrieve, update or delete a user from database
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)
    # user = get_object_or_404(User, pk=pk)

    if request.method == 'GET':  # get user details
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':  # update of user
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':  # delete user based on the delete request submitted
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  # TODO: find out what a http status codes mean!!

