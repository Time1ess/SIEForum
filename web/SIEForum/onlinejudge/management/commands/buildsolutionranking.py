from django.core.management.base import BaseCommand

from onlinejudge.solutionranking import build_solution_ranking


class Command(BaseCommand):
    help = 'Builds solution ranking'

    def handle(self, *args, **options):
        self.stdout.write('\n\nBuilding solution ranking...')
        build_solution_ranking()
        self.stdout.write('Done!')
