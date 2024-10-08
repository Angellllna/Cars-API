from decimal import Decimal

import requests
from cars.models import Brand, Car, Model_Car
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Fetch cars from external API and save to the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "count", type=int, nargs="?", default=5, help="Number of cars to fetch"
        )

    def handle(self, *args, **options):
        count = options["count"]
        response = requests.get(f"https://freetestapi.com/api/v1/cars?limit={count}")

        if response.status_code == 200:
            car_data = response.json()

            for car in car_data:
                brand_name = car["make"]
                brand = Brand.objects.filter(name=brand_name).first()
                if not brand:
                    brand = Brand.objects.create(name=brand_name, country="Unknown")

                model_name = car["model"]
                year = car["year"]
                model = Model_Car.objects.filter(
                    model_name=model_name, year=year
                ).first()
                if not model:
                    model = Model_Car.objects.create(
                        model_name=model_name,
                        year=year,
                        body_style="sedan",
                    )

                Car.objects.update_or_create(
                    brand=brand,
                    model=model,
                    defaults={
                        "price": Decimal(car.get("price", 0)),
                        "transmission": car.get("transmission", "Manual"),
                        "engine": car.get("engine", "2.0L"),
                        "mileage": car.get("mileage", 0),
                        "exterior_color": car.get("color", "Unknown"),
                        "interior_color": "Unknown",
                        "fuel_type": car.get("fuelType", "gasoline"),
                        "is_on_sale": True,
                    },
                )

            self.stdout.write(self.style.SUCCESS(f"Successfully fetched {count} cars"))
        else:
            self.stdout.write(self.style.ERROR("Failed to fetch cars"))
