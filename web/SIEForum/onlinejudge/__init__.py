from django.utils.translation import ugettext_lazy as _


LOW_SCORE_FIRST = 'low'
HIGH_SCORE_FIRST = 'high'

ORDER_TYPES = (
    (LOW_SCORE_FIRST, _('Lower score first')),
    (HIGH_SCORE_FIRST, _('Higher score first')),
)


SOL_PENDING = 0
SOL_RUNNING = 1
SOL_FINISHED = 2


SOLUTION_STATUSES = (
    (SOL_PENDING, _('Solution pending')),
    (SOL_RUNNING, _('Solution running')),
    (SOL_FINISHED, _('Solution finished'))
)
