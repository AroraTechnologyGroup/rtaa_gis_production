from rest_framework import routers
from . import views
from django.conf.urls import url

router = routers.DefaultRouter()
router.register(r'agreements', views.AgreementViewSet)

app_name = 'lpm'
urlpatterns = [
    url(r'swag/', views.schema_view),
]

urlpatterns += router.urls
