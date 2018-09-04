import logging
from django.shortcuts import Http404, get_object_or_404

from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, RetrieveUpdateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response

from biz.models import Issue, IssueLog
from biz.api.serializers import IssueListSerializer, IssueCreateUpdateSerializer
from app import settings

# setup logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fileHandler = logging.FileHandler(settings.BASE_DIR + '/logs/issues.log')
formatter = logging.Formatter('%(asctime)s:%(name)s:%(module)s:%(lineno)d:%(message)s')
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)


class IssueListAPIView(ListAPIView):
    """
    List all issues.
    """
    queryset = Issue.objects.all()
    serializer_class = IssueListSerializer
    permission_classes = [IsAuthenticated, ]


class IssueDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve,update and delete an Issue.
    """
    queryset = Issue.objects.all()
    serializer_class = IssueCreateUpdateSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = "pk"

    def get_object(self):
        queryset = self.filter_queryset(self.queryset)

        lookup_url_kwarg = self.lookup_url_kwarg
        assert lookup_url_kwarg in self.kwargs, 'pk Should be in Keyword arguments'

        filter_kwarg = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        issue = get_object_or_404(queryset, id=filter_kwarg[self.lookup_field])

        # check object permissions which might raise permission challenges
        self.check_object_permissions(self.request, issue)

        return issue

    def get(self, request, *args, **kwargs):
        issue = self.get_object()
        serializer = self.get_serializer(issue)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.debug(serializer.data)
            return Response(serializer.data)
        logger.debug(str(serializer.errors))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        issue = self.get_object()
        logger.debug(issue)
        if issue:
            issue.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class IssueCreateAPIView(CreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueCreateUpdateSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        return super(IssueCreateAPIView, self).post(request, *args, **kwargs)
