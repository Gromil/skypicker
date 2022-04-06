from rest_framework import routers

from flights.views import FlightViewSet

router = routers.SimpleRouter()

router.register(r'flights', FlightViewSet, 'flight')

urlpatterns = router.urls
