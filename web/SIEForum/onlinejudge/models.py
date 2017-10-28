from uuid import uuid4

from django.db import models

from . import ORDER_TYPES, SOLUTION_STATUSES, SOL_PENDING
from .conf import settings


class Problem(models.Model):
    thread = models.OneToOneField(
        'misago_threads.Thread',
        on_delete=models.CASCADE)
    starter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    order_type = models.CharField(
        choices=ORDER_TYPES,
        max_length=10)
    judge_name = models.CharField(
        default='default',
        max_length=40)
    module_name = models.CharField(
        max_length=40)
    uid = models.UUIDField(default=uuid4)

    def __str__(self):
        return str(self.thread)

    def get_absolute_url(self):
        return self.thread.get_absolute_url()


class Solution(models.Model):
    problem = models.ForeignKey(
        'Problem',
        on_delete=models.CASCADE)
    starter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    thread = models.OneToOneField(
        'misago_threads.Thread',
        on_delete=models.SET_NULL,
        blank=True,
        null=True)
    result = models.FloatField(default=-1)
    submit_counter = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=SOLUTION_STATUSES,
                                 default=SOL_PENDING)

    def __str__(self):
        return '{}:{}'.format(self.problem, self.starter)


class SolutionRanking(models.Model):
    problem = models.ForeignKey('Problem', on_delete=models.CASCADE)
    solution = models.ForeignKey('Solution', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0, db_index=True)
