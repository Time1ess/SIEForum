from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from .pages import oj


class OnlineJudgeConfig(AppConfig):
    name = 'onlinejudge'
    label = 'onlinejudge'
    verbose_name = 'Online Judge'

    def ready(self):
        self.register_online_judge_pages()

    def register_online_judge_pages(self):
        oj.add_section(
            link='oj:problems_list',
            name=_('Problems'))
        oj.add_section(
            link='oj:solution_rank',
            name=_('Rank'))
