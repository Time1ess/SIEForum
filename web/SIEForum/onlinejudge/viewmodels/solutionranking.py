from misago.users.online.utils import make_users_status_aware
from misago.users.serializers import UserCardSerializer

from onlinejudge.solutionranking import get_solution_ranking
from onlinejudge.conf import settings


class SolutionRankingUsers(object):
    def __init__(self, request, problem):
        ranking = get_solution_ranking(problem)
        make_users_status_aware(request.user, ranking['users'],
                                fetch_state=True)

        self.problem = problem
        self.count = ranking['users_count']
        self.tracked_period = settings.MISAGO_RANKING_LENGTH
        self.users = ranking['users']
        self.participants = problem.solution_set.all().count()

    def get_frontend_context(self):
        return {
            'tracked_period': self.tracked_period,
            'results': SolutionUserSerializer.extend_fields('meta')(
                self.users, many=True).data,
            'count': self.count,
            'participants': self.participants,
        }

    def get_template_context(self):
        return {
            'tracked_period': self.tracked_period,
            'users': self.users,
            'users_count': self.count,
            'participants': self.participants,
        }


class SolutionUserSerializer(UserCardSerializer):
    def get_meta(self, obj):
        return {'score': obj.score, 'submissions': obj.submissions}
