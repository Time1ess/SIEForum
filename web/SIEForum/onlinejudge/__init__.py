from django.utils.translation import ugettext_lazy as _


default_app_config = 'onlinejudge.apps.OnlineJudgeConfig'


LOW_SCORE_FIRST = '低值优先'
HIGH_SCORE_FIRST = '高值优先'

ORDER_TYPES = (
    (LOW_SCORE_FIRST, _('Lower score first')),
    (HIGH_SCORE_FIRST, _('Higher score first')),
)


SOL_PENDING = 0
SOL_RUNNING = 1
SOL_FINISHED = 2
SOL_ERROR = -1


SOLUTION_STATUSES = (
    (SOL_PENDING, _('Solution pending')),
    (SOL_RUNNING, _('Solution running')),
    (SOL_FINISHED, _('Solution finished')),
    (SOL_ERROR, _('Solution error')),
)
