from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('agreements', views.AgreementViewSet)

app_name = 'lpm'

urlpatterns = []
urlpatterns += router.urls
