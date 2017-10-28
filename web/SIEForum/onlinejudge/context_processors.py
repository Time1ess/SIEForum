from django.urls import reverse


def oj_links(request):
    if request.include_frontend_context:
        request.frontend_context.update({
            'PROBLEMS_API': reverse('oj:api:problems-list'),
            'PROBLEMS_URL': reverse('oj:problems'),
        })

    return {}
