from rest_framework import routers
from .api import InstanceViewSet

router = routers.DefaultRouter()
router.register('api/database', InstanceViewSet)

urlpatterns = router.urls