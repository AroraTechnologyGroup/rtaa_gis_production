from rest_framework import routers
from .views import RecordViewSet

router = routers.DefaultRouter()
router.register('counts', RecordViewSet)

app_name = 'analytics'

urlpatterns = []
urlpatterns += router.urls
