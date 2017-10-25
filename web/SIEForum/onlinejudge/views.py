from django.shortcuts import redirect
from django.views.generic import ListView

from .pages import oj
from .models import Problem


def landing(request):
    return redirect(oj.get_default_link())

class ProblemList(ListView):
    model = Problem
    template_name = 'onlinejudge/problem.html'

    def get_query_set(self):
        return super().get_query_set().order_by('-id')


class SolutionRankList(ListView):
    template_Name = 'onlinejudge/rank.shtml'
