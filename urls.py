from django.conf.urls import url
from question import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.getQuestion, name='question'),
    url(r'NaN/', views.finalPlayerList, name='finish'),
    url(r'^johncena/', views.getQuestion),
    url(r'^(?P<level>[0-9]+)/', views.getQuestionByLevel, name='question_by_level'),
    url(r'^(?P<level>[0-9]+)/johncena$', views.getQuestionByLevel),
    url(r'^answer/$', views.submitAnswer, name='answer'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
