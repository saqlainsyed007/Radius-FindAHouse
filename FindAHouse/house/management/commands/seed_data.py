import random

from django.core.management.base import BaseCommand

from house.models import House


class Command(BaseCommand):

    help = 'Populate Initial House Data'

    def handle(self, *args, **kwargs):

        latitude_range = (12.000000, 13.000000)
        longitude_range = (77.000000, 78.000000)
        house_objs = []
        used_lat_longs = []
        for _, index in enumerate(range(25000)):
            latitude = round(random.uniform(*latitude_range), 6)
            longitude = round(random.uniform(*longitude_range), 6)
            if (latitude, longitude) in used_lat_longs:
                continue
            used_lat_longs.append((latitude, longitude))
            bedrooms = random.randint(1, 4)
            bathrooms = random.randint(max(bedrooms - 1, 1), bedrooms)
            name = (
                f"{random.choice(['Elegant', 'Luxurious', 'Well-Designed'])} "
                f"{bedrooms}BHK "
                f"{random.choice(['House', 'Apartment'])} "
                f"with {bathrooms} bathrooms"
            )
            print(f"Creating {index + 1}. {name}...")
            price = 100000 + 10000 * bedrooms + random.randint(10, 20) * 1000
            house = House(
                name=name,
                latitude=latitude,
                longitude=longitude,
                price=price,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
            )
            house_objs.append(house)
        House.objects.bulk_create(house_objs)
