from rest_framework.routers import DefaultRouter
from .views import RaceViewSet, ResultViewSet

# register view sets for models
router = DefaultRouter()
router.register("races", RaceViewSet)
router.register("results", ResultViewSet)

urlpatterns = router.urls