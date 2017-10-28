from django.conf.urls import include, url


from onlinejudge.views import lists


urlpatterns = [
    url(r'^users/', include([
        url(r'^rankings/(?P<uid>.+)',
            lists.SolutionRankingView.as_view(), name='rankings'),
        url(r'^rankings/',
            lists.SolutionRankingView.as_view(), name='rankings'),
        url(r'^problems/(?P<page>\d+)/',
            lists.ProblemView.as_view(), name='problems'),
        url(r'^problems/',
            lists.ProblemView.as_view(), name='problems'),
        ])),
]

apipatterns = [
    url(r'^', include('onlinejudge.urls.api')),
]

urlpatterns += [
    url(r'^api/', include((apipatterns, 'api'), namespace='api')),
]
