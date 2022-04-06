from datetime import datetime, date
from itertools import groupby

from celery import shared_task
from dateutil.relativedelta import relativedelta

from flights.models import Flight
from flights.services import SkyPicker


def grouper(item: dict) -> date:
    return datetime.fromtimestamp(item['dTimeUTC']).date()


@shared_task
def populate_flights_data():
    for direction in Flight.DIRECTIONS:
        fly_from, fly_to = direction[0], direction[1]
        service = SkyPicker()
        response = service.get_flights(fly_from=fly_from, fly_to=fly_to)
        data = response.json()['data']

        for fly_date, group_items in groupby(data, key=grouper):
            record_with_min_price: dict = min(
                group_items, key=lambda item: item['price']
            )
            Flight.objects.update_or_create(
                fly_from=fly_from, fly_to=fly_to,
                skypicker_id=record_with_min_price['id'],
                defaults={
                    'fly_date': fly_date,
                    'min_price': record_with_min_price['price'],
                    'booking_token': record_with_min_price['booking_token']
                }
            )


@shared_task
def check_flights():
    today = datetime.today()
    date_after_month = today + relativedelta(months=1)
    flights = Flight.objects.filter(
        fly_date__gte=today, fly_date__lte=date_after_month
    )
    service = SkyPicker()
    for flight in flights:
        response = service.check_flight(flight.booking_token)
        data = response.json()
        if data['price_change']:
            flight.min_price = data['conversion']['amount']
        if not data['flights_invalid']:
            flight.valid = False
        flight.save()
