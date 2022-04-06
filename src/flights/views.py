from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from flights.models import Flight
from flights.serializers import FlightSerializer


class FlightViewSet(ListModelMixin, GenericViewSet):
    serializer_class = FlightSerializer
    queryset = Flight.objects.all()
