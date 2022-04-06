from django.db import models


class FlightManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by(
            'fly_from', 'fly_to', '-fly_date'
        )


class Flight(models.Model):
    DIRECTIONS = (
        ('ALA', 'TSE'),
        ('TSE', 'ALA'),
        ('ALA', 'MOW'),
        ('MOW', 'ALA'),
        ('ALA', 'CIT'),
        ('CIT', 'ALA'),
        ('TSE', 'MOW'),
        ('MOW', 'TSE'),
        ('TSE', 'LED'),
        ('LED', 'TSE'),
    )

    fly_from = models.CharField(max_length=3)
    fly_to = models.CharField(max_length=3)
    fly_date = models.DateField()
    min_price = models.IntegerField()
    booking_token = models.CharField(max_length=1024)
    valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    skypicker_id = models.CharField(max_length=255)

    objects = FlightManager()

    def __str__(self):
        return f'{self.fly_from} --> {self.fly_to} : {self.fly_date} | ' \
               f'{self.min_price}'
