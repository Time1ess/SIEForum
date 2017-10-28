import re

from . import LOW_SCORE_FIRST
from .judges import judges_dict
from .conf import settings


def get_problem_uid(content):
    res = re.findall(settings.OJ_UID_PATTERN, str(content))
    if len(res) != 1:
        return None
    else:
        return res[0]


def extract_problem_kwargs(content):
    header_args, remain = content.split('\n', 1)
    kwargs = dict(re.findall(r'\[(.*?):(.*?)\]', header_args))
    order_type = kwargs.get(settings.OJ_ORDER_KEY, LOW_SCORE_FIRST)
    judge_name = judges_dict[kwargs.get(settings.OJ_JUDGE_KEY,
                                        settings.OJ_DEFAULT_JUDGE)]
    module_name = kwargs[settings.OJ_MODULE_KEY]
    return order_type, judge_name, module_name
