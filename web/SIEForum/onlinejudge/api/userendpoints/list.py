from rest_framework.response import Response
from misago.core.shortcuts import get_int_or_404

from onlinejudge.viewmodels import ProblemViewModel


def problems_set(request):
    page = get_int_or_404(request.query_params.get('page', 0))
    if page == 1:
        page = 0
    problems = ProblemViewModel(request, page)
    return Response(problems.get_frontend_context())
