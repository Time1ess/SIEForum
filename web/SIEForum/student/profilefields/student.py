import re

from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.exceptions import ValidationError
from misago.users.profilefields import basefields


class StudentIDField(basefields.TextProfileField):
    fieldname = 'student_id'
    label = _('Student ID')

    def clean(self, request, user, data):
        pat = re.compile(r'[0-9]+')
        if data and not pat.search(data):
            raise ValidationError(ugettext('This is not a valid student ID'))
        return data
