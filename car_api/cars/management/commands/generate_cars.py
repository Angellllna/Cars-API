# python ./car_api/manage.py generate_cars 10

import random
from decimal import Decimal

from cars.models import Brand, Car, Model_Car
from django.core.management.base import BaseCommand
from faker import Faker
from faker_vehicle import VehicleProvider

fake = Faker()
fake.add_provider(VehicleProvider)


class Command(BaseCommand):
    help = "Generate random cars with brands and models"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="The number of cars to be created")

    def handle(self, *args, **kwargs):
        number_of_cars = kwargs["count"]

        for _ in range(number_of_cars):
            brand = Brand.objects.create(
                name=fake.vehicle_make(), country=fake.country()
            )

            model = Model_Car.objects.create(
                model_name=fake.vehicle_model(),
                year=fake.vehicle_year(),
                body_style=fake.vehicle_category(),
            )

            Car.objects.create(
                brand=brand,
                model=model,
                price=Decimal(random.uniform(10000.00, 100000.00)),
                transmission=random.choice(["Automatic", "Manual"]),
                engine=random.choice(["1.4L", "2.0L", "3.0L", "5.0L"]),
                mileage=random.randint(0, 300000),
                exterior_color=fake.color_name(),
                interior_color=fake.color_name(),
                fuel_type=random.choice(["Gasoline", "Diesel", "Electric"]),
                is_on_sale=random.choice([True, False]),
            )
        self.stdout.write(
            self.style.SUCCESS(f"{number_of_cars} cars created successfully!")
        )
