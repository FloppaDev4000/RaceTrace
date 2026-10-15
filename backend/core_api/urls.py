from rest_framework.routers import DefaultRouter
from .views import RaceViewSet

router = DefaultRouter()
router.register("races", RaceViewSet)
urlpatterns = router.urls