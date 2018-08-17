from django.shortcuts import get_object_or_404, get_list_or_404

from users.models import Engineer, Client, User
from users.api.serializers import UserSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# write individual views to handle requests
@api_view('GET', 'POST')
def user_list(request):
    """
    API Endpoint Used to get all users or created a single user based on the request
    :param request: either a POST or GET request is sent
    :return: if GET -- Query db for all Users and return if POST store data and return
    instance of the object
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


@api_view('GET', 'PUT', 'DELETE')
def user_detail(request, pk):
    """
    API Endpoint used to retrieve, update or delete a user from database
    :param request: Http request (GET,PUT,DELETE)
    :param pk: the primary key of the user in question
    :return: user details of validation errors
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

# we start with users




# # use of viewsets
# class EngineerViewSet(viewsets.ModelViewSet):
#     """
#     API Endpoint that allows Engineers to be viewed and edited
#     """
#     queryset = Engineer.objects.all().order_by('-user__date_joined')
#     serializer_class = EngineerSerializer
#
#
# class ClientViewSet(viewsets.ModelViewSet):
#     """
#     API Endpoint that allows Clients to viewed and Edited
#     """
#     queryset = Client.objects.all()
#     serializer_class = ClientSerializer
#
#
# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API Endpoint that allows all users to be viewd and edited
#     """
#
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
