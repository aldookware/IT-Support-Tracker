from django.shortcuts import Http404, get_object_or_404

from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response


from users.models import Issue, IssueLog
from users.api.serializers import IssueSerializer


class IssueListAPIView(ListAPIView):
    """
    List all issues.
    """
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, ]


class IssueDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve,update and delete an Issue.
    """
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = "pk"

    def get_object(self):
        queryset = self.filter_queryset(self.queryset)

        lookup_url_kwarg = self.lookup_url_kwarg
        assert lookup_url_kwarg in self.kwargs

        filter_kwarg = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        issue = get_object_or_404(queryset, filter_kwarg)

        # check object permissions which might raise permission challenges
        self.check_object_permissions(self.request, issue)

        return issue

    def update(self):
        issue = self.get_object()
        serializer = self.get_serializer(issue, data=self.request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)







