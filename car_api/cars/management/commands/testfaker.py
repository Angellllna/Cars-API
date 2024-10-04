from faker import Faker
from faker_vehicle import VehicleProvider

fake = Faker()
fake.add_provider(VehicleProvider)

import json

print(fake.vehicle.fuel()) 
#