from rest_framework import viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from onlinejudge.models import Problem
from .userendpoints.list import problems_set


class ProblemsViewSet(viewsets.GenericViewSet):
    queryset = Problem.objects.order_by('-thread__started_on')
    parser_classes = (FormParser, JSONParser, MultiPartParser)

    def get_queryset(self):
        return self.queryset

    def list(self, request):
        return problems_set(request)
