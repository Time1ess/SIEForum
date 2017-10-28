from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from misago.users.pages import users_list


class OnlineJudgeConfig(AppConfig):
    name = 'onlinejudge'
    label = 'onlinejudge'
    verbose_name = 'Online Judge'

    def ready(self):
        self.register_oj_pages()

    def register_oj_pages(self):
        users_list.add_section(
            link='oj:problems',
            component='problems',
            name=_('Online Judge'))
