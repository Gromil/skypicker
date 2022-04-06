from datetime import datetime
from typing import Optional

import requests
from dateutil.relativedelta import relativedelta
from requests import Response


class SkyPicker:
    PARTNER = 'bekzhanaviata'
    CURRENCY = 'KZT'

    def get_flights(
            self, fly_from: str, fly_to: str,
            date_from: Optional[str] = None, date_to: Optional[str] = None
    ) -> Response:
        url = 'https://api.skypicker.com/flights'
        today = datetime.today()
        date_from: str = (
            date_from if date_from else today.strftime('%d/%m/%Y')
        )
        date_after_month = today + relativedelta(months=1)
        date_to: str = (
            date_to if date_to else date_after_month.strftime('%d/%m/%Y')
        )
        response: Response = requests.get(
            url,
            params={
                'curr': self.CURRENCY, 'partner': self.PARTNER, 'sort': 'date',
                'fly_from': fly_from, 'fly_to': fly_to,
                'date_from': date_from, 'date_to': date_to
            }
        )
        response.raise_for_status()
        return response

    def check_flight(self, booking_token: str) -> Response:
        url = 'https://booking-api.skypicker.com/api/v0.1/check_flights'
        response: Response = requests.get(
            url,
            params={
                'curr': self.CURRENCY, 'affily': self.PARTNER,
                'v': 2, 'bnum': 0, 'pnum': 1,
                'booking_token': booking_token
            }
        )
        response.raise_for_status()
        return response
