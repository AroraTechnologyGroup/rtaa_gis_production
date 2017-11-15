from rest_framework import routers
from . import views
from django.conf.urls import url

router = routers.DefaultRouter()
router.register(r'agreements', views.AgreementViewSet)
router.register(r'spaces', views.SpaceViewSet)

app_name = 'lpm'
urlpatterns = [
    url(r'space-editor/(.*)', views.SpaceEditor.as_view(), name='space-editor')
]

urlpatterns += router.urls
