from cars.models import Car, Brand, Model_Car
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Delete all cars"

    def handle(self, *args, **kwargs):
        Car.objects.all().delete()
        Brand.objects.all().delete()
        Model_Car.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("All cars have been deleted"))


#python manage.py delete_cars
