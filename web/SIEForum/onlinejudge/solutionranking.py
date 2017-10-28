from onlinejudge import LOW_SCORE_FIRST
from onlinejudge.models import SolutionRanking, Problem, Solution

from .conf import settings


def get_solution_ranking(problem):
    users = []
    queryset = SolutionRanking.objects.filter(problem=problem)
    queryset = queryset.select_related('solution', 'user')
    if problem.order_type == LOW_SCORE_FIRST:
        queryset = queryset.order_by('solution__result')
    else:
        queryset = queryset.order_by('-solution__result')
    for ranking in queryset:
        ranking.user.score = ranking.solution.result
        ranking.user.submissions = ranking.solution.submit_counter
        users.append(ranking.user)

    return {
        'users': users,
        'users_count': len(users),
    }


def build_solution_ranking():
    problems = Problem.objects.all()
    max_len = getattr(settings, 'OJ_RANKING_SIZE', 100)
    for problem in problems:
        # Delete old records
        SolutionRanking.objects.filter(problem=problem).delete()
        solutions = Solution.objects.filter(problem=problem)
        solutions = solutions.exclude(result__lt=0).select_related('starter')
        if problem.order_type == LOW_SCORE_FIRST:
            solutions = solutions.order_by('result')
        else:
            solutions = solutions.order_by('-result')
        for sol in solutions[:max_len]:
            SolutionRanking.objects.create(
                problem=problem,
                solution=sol,
                user=sol.starter,)
