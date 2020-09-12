from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.


class House(models.Model):

    name = models.CharField(
        max_length=256,
    )
    latitude = models.FloatField(
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        help_text="Latitude of house in range (-90 to 90)"
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        help_text="Longitude of house in range (-180 to 180)"
    )
    price = models.FloatField(
        validators=[MinValueValidator(1)],
        help_text="Price of house"
    )
    bedrooms = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Number of Bedrooms"
    )
    bathrooms = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Number of Bathrooms"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('longitude', 'latitude')
        db_table = 'house'
        constraints = [
            models.CheckConstraint(
                check=models.Q(latitude__range=(-90, 90)),
                name="valid_latitude_constraint",
            ),
            models.CheckConstraint(
                check=models.Q(longitude__range=(-180, 180)),
                name="valid_longitude_constraint",
            ),
            models.CheckConstraint(
                check=models.Q(price__gte=1),
                name="valid_price_constraint",
            ),
            models.CheckConstraint(
                check=models.Q(bedrooms__gt=0),
                name="valid_bedrooms_constraints",
            ),
            models.CheckConstraint(
                check=models.Q(bathrooms__gt=0),
                name="valid_bathrooms_constraints",
            ),
        ]
