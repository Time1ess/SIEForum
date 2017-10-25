from uuid import uuid4

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _

from . import ORDER_TYPES, SOLUTION_STATUSES, SOL_PENDING


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
    uid = models.UUIDField(default=uuid4)

    def __str__(self):
        return _('Problem:{}'.format(self.thread))


class Solution(models.Model):
    problem = models.ForeignKey(
        'Problem',
        on_delete=models.CASCADE)
    starter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    thread = models.OneToOneField(
        'misago_threads.Thread',
        on_delete=models.CASCADE)
    result = models.FloatField(default=-1)
    submit_counter = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=SOLUTION_STATUSES,
        default=SOL_PENDING)

    def __str__(self):
        return '{}:{}'.format(problem, starter)
