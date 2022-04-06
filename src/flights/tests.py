import responses

from pytest import fixture
from responses import RequestsMock

from flights.models import Flight
from flights.tasks import populate_flights_data


@fixture
def mocked_flights() -> RequestsMock:
    with RequestsMock(
            assert_all_requests_are_fired=True
    ) as responses_mock:
        response_data = {
            'data': [
                {
                    "dTimeUTC": 1649221800,  # 06/04/2022--11:10
                    "price": 43905.9999,
                },
                {
                    "dTimeUTC": 1649252100,  # 06/04/2022--19:35
                    "price": 69448.9997,
                },
                {
                    "dTimeUTC": 1649255100,  # 06/04/2022--20:25
                    "price": 23129.9997,
                },
            ]
        }
        url = 'https://api.skypicker.com/flights'
        responses_mock.add(
            method=responses.GET, url=url, json=response_data, status=200
        )
        yield responses_mock


def test_populate_data(db, mocked_flights):
    populate_flights_data()
    flight = Flight.objects.first()
    assert flight.min_price == 23129.9997
