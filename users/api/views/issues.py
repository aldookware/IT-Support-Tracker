from django.shortcuts import Http404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from users.models import Issue, IssueLog
from users.api.serializers import IssueSerializer


class IssueListAPIView(APIView):
    """
    List all issues and create a new Issue.
    """

    def get(self, request, format=None):
        issues = Issue.objects.all()
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueDetailAPIView(APIView):
    """
    Retrieve, update and delete an Issue.
    """

    def get_object(self, pk):
        try:
            return Issue.objects.get(pk=pk)
        except Issue.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        issue = self.get_object(pk)
        serializer = IssueSerializer(issue)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        issue = self.get_object(pk)

        serializer = IssueSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, satus=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        issue = self.get_object(pk)
        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
