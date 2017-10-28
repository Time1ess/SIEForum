from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import View
from misago.users.views.lists import ListView

from onlinejudge.models import Problem
from onlinejudge.viewmodels import SolutionRankingUsers
from onlinejudge.viewmodels import ProblemViewModel


class SolutionRankingView(View):
    template_name = 'onlinejudge/solution_ranking.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                      self.get_context_data(request, *args, **kwargs))

    def get_context_data(self, request, *args, **kwargs):
        problem = get_object_or_404(Problem, uid=kwargs.get('uid', None))
        model = SolutionRankingUsers(request, problem)

        context = model.get_template_context()
        context['REFERER'] = request.META.get('HTTP_REFERER',
                                              reverse('oj:problems'))
        return context


class ProblemView(ListView):
    template_name = 'onlinejudge/problems.html'

    def get_context_data(self, request, page=0):
        problems = ProblemViewModel(request, page)

        request.frontend_context['PROBLEMS'] = problems.get_frontend_context()
        return problems.get_template_context()
