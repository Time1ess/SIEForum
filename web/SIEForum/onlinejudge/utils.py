import re

from django.conf import settings


def get_problem_uid(content):
    res = re.findall(settings.OJ_UID_PATTERN, str(content))
    if len(res) != 1:
        return None
    else:
        return res[0]
