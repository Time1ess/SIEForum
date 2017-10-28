from misago.core.apirouter import MisagoApiRouter

from onlinejudge.api.problems import ProblemsViewSet


urlpatterns = []

router = MisagoApiRouter()
router.register(r'problems', ProblemsViewSet,
                base_name='problems')
urlpatterns += router.urls
