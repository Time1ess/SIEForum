from django.urls import reverse
from rest_framework import serializers
from misago.core.shortcuts import paginate, pagination_dict

from onlinejudge.models import Problem
from onlinejudge.conf import settings


class ProblemViewModel(object):
    def __init__(self, request, page=0):
        problems = Problem.objects.all().select_related(
            'thread', 'starter').order_by(
            '-thread__started_on').all()
        page_size = getattr(settings, 'OJ_PROBLEMS_PER_PAGE', 20)
        list_page = paginate(problems, page, page_size, 4)
        self.problems = list_page.object_list
        for problem in self.problems:
            problem.solutions = problem.solution_set.all().count()
        self.paginator = pagination_dict(list_page)
        self.count = len(self.problems)

    def get_frontend_context(self):
        context = {
            'problems': ProblemSerializer(self.problems, many=True).data,
            'count': self.count,
        }
        context.update(self.paginator)
        return context

    def get_template_context(self):
        return {
            'problems': self.problems,
            'count': self.count,
            'paginator': self.paginator,
        }


class StarterSerialzer(serializers.Serializer):
    name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.username

    def get_url(self, obj):
        return obj.get_absolute_url()


class ProblemSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    thread_title = serializers.SerializerMethodField()
    starter = serializers.SerializerMethodField()
    ranking_url = serializers.SerializerMethodField()
    solutions = serializers.SerializerMethodField()
    api = serializers.SerializerMethodField()

    class Meta:
        model = Problem
        fields = [
            'url',
            'thread_title',
            'starter',
            'ranking_url',
            'solutions',
            'api',
        ]

    def get_url(self, obj):
        return obj.get_absolute_url()

    def get_thread_title(self, obj):
        return obj.thread.title

    def get_ranking_url(self, obj):
        return reverse('oj:rankings', args=(obj.uid,))

    def get_solutions(self, obj):
        return obj.solutions

    def get_starter(self, obj):
        return StarterSerialzer(obj.starter).data

    def get_api(self, obj):
        return {
        }
