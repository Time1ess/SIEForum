import re

from uuid import UUID

from django.conf import settings
from django.utils.translation import ugettext as _
from misago.threads.api.postingendpoint import PostingMiddleware
from misago.threads.checksums import update_post_checksum
from rest_framework import serializers


from . import LOW_SCORE_FIRST
from .models import Problem, Solution
from .utils import get_problem_uid


class OJMiddleware(PostingMiddleware):
    def _handle_problem(self, serializer):
        thread = self.thread
        post = self.post
        starter = self.user
        problem, created = Problem.objects.get_or_create(
            thread=thread, starter=starter)
        uid = problem.uid
        uid_str = settings.OJ_UID_FORMAT.format(uid.hex)
        # Only update problem when thread updated
        if post.is_first_post:
            header_args, _ = post.original.split('\n', 1)
            kwargs = dict(re.findall(r'\[(.*?):(.*?)\]', header_args))
            order_type = kwargs.get('O', LOW_SCORE_FIRST)
            problem.order_type = order_type
            post.parsed = post.parsed + '\n' + uid_str
            update_post_checksum(post)
            post.save()
            problem.save()

    def _handle_solution(self, serializer):
        thread = self.thread
        post = self.post
        starter = self.user
        # Only update problem when thread updated
        if post.is_first_post:
            uid = get_problem_uid(post.parsed)
            if uid is None:
                # TODO: validate message
                raise serializers.ValidationError(_('Problem uid parse error'))
            ps = Problem.objects.filter(uid=UUID(uid))
            if ps.count() == 0:
                # TODO: validate message
                raise serializers.ValidationError(_('No such problem'))
            problem = ps[0]
            sol = Solution.objects.filter(problem=problem, starter=starter)
            if sol.exists():
                solution = sol[0]
            else:
                solution = Solution.objects.create(problem=problem,
                                                   starter=starter,
                                                   thread=thread)
            if solution.thread != thread:
                # TODO: validate message
                raise serializers.ValidationError(_(
                    'Only one solution should be '
                    'submitted to the same problem'))
            solution.save()
            # TODO: Add to task queue

    def post_save(self, serializer):
        # Problem
        if str(self.thread.category) == settings.OJ_CATE_NAME:
            self._handle_problem(serializer)
        # Solution
        elif str(self.thread.category) == settings.OJ_SUB_CATE_NAME:
            self._handle_solution(serializer)
