from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from users.models import Client

from ..serializers import ClientSerializer


class ClientListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientDetailView(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientCreateViewAPIView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
