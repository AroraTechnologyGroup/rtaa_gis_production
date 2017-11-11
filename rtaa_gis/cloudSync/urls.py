from rest_framework import routers
from .views import OnlineViewSet, FLayerViewSet, GDBViewSet, FDatasetViewSet,\
    FClassViewSet, PLogViewSet, WebMapViewSet

app_name = 'cloudSync'
router = routers.DefaultRouter()
router.register(r'gdb', GDBViewSet)
router.register(r'dataset', FDatasetViewSet)
router.register(r'fcs', FClassViewSet)
router.register(r'webmap', WebMapViewSet)
router.register(r'flayer', FLayerViewSet)
router.register(r'web', OnlineViewSet, base_name="web")

router.register(r'publisher', PLogViewSet)

urlpatterns = []

urlpatterns += router.urls


