from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Brand, Car, Model_Car

User = get_user_model()
# poetry run python ./car_api/manage.py test cars


class CarModelTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )

        response = self.client.post(
            "/acc/user/login/",
            {"username": "testuser", "password": "testpassword"},
            format="json",
        )
        self.token = response.data.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.brand_bmw = Brand.objects.create(name="BMW", country="Germany")
        self.brand_mercedes = Brand.objects.create(name="Mercedes", country="Germany")

        self.model_x5_2015 = Model_Car.objects.create(
            model_name="x5", year=2015, body_style="SUV"
        )
        self.model_x5_2020 = Model_Car.objects.create(
            model_name="x5", year=2020, body_style="SUV"
        )
        self.model_e200_2018 = Model_Car.objects.create(
            model_name="E 200", year=2018, body_style="Sedan"
        )

        self.car1 = Car.objects.create(
            brand=self.brand_bmw,
            model=self.model_x5_2015,
            price=50000,
            transmission="Automatic",
            engine="2.0L",
            mileage=20000,
            exterior_color="Black",
            interior_color="Black",
            fuel_type="diesel",
            is_on_sale=True,
        )
        self.car2 = Car.objects.create(
            brand=self.brand_bmw,
            model=self.model_x5_2020,
            price=70000,
            transmission="Automatic",
            engine="3.0L",
            mileage=5000,
            exterior_color="White",
            interior_color="Black",
            fuel_type="gas",
            is_on_sale=True,
        )
        self.car3 = Car.objects.create(
            brand=self.brand_mercedes,
            model=self.model_e200_2018,
            price=55000,
            transmission="Automatic",
            engine="2.0L",
            mileage=15000,
            exterior_color="White",
            interior_color="Beige",
            fuel_type="gas",
            is_on_sale=False,
        )

    def test_user_creation(self):
        response = self.client.post(
            "/acc/user/create/",
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "newpassword",
                "password2": "newpassword",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(
            User.objects.get(username="newuser").email, "newuser@example.com"
        )

    def test_user_login(self):
        response = self.client.post(
            "/acc/user/login/",
            {"username": "testuser", "password": "testpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_get_brands(self):
        response = self.client.get("/brands/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        brand_names = [brand["name"] for brand in response.data]
        self.assertIn("BMW", brand_names)
        self.assertIn("Mercedes", brand_names)

    def test_filter_brands_by_name(self):
        response = self.client.get("/brands/?name=BMW", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "BMW")
        self.assertEqual(response.data[0]["country"], "Germany")

    def test_filter_brands_by_country(self):
        response = self.client.get("/brands/?country=Germany", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_models(self):
        response = self.client.get("/models/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        model_names = [model["model_name"] for model in response.data]
        self.assertIn("x5", model_names)
        self.assertIn("E 200", model_names)

    def test_filter_models_by_name(self):
        response = self.client.get("/models/?model_name=x5", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["model_name"], "x5")
        self.assertEqual(response.data[1]["model_name"], "x5")

    def test_get_cars_on_sale(self):
        response = self.client.get("/cars/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        car_ids = [car["id"] for car in response.data]
        self.assertIn(self.car1.id, car_ids)
        self.assertIn(self.car2.id, car_ids)

    def test_get_all_cars(self):
        response = self.client.get("/cars/all/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        car_ids = [car["id"] for car in response.data]
        self.assertIn(self.car1.id, car_ids)
        self.assertIn(self.car2.id, car_ids)
        self.assertIn(self.car3.id, car_ids)

    def test_filter_cars_by_model_name(self):
        response = self.client.get("/cars/?model_name=x5", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["model"]["model_name"], "x5")
        self.assertEqual(response.data[1]["model"]["model_name"], "x5")

    def test_filter_cars_by_multiple_fields(self):
        response = self.client.get(
            "/cars/?model_name=x5&engine=2.0L&fuel_type=diesel", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.car1.id)

    def test_filter_cars_by_brand_and_engine(self):
        response = self.client.get(
            "/cars/?brand_name=Mercedes&engine=2.0L&fuel_type=gas", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        response = self.client.get(
            "/cars/all/?brand_name=Mercedes&engine=2.0L&fuel_type=gas", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.car3.id)

    def test_filter_cars_by_year_range(self):
        response = self.client.get(
            "/cars/all/?year_min=2010&year_max=2021", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]["id"], self.car1.id)
        self.assertEqual(response.data[1]["id"], self.car2.id)
        self.assertEqual(response.data[2]["id"], self.car3.id)

    def test_filter_cars_by_body_style(self):
        response = self.client.get("/cars/?body_style=Sedan", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        response = self.client.get("/cars/all/?body_style=Sedan", format="json")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["model"]["body_style"], "Sedan")

    def test_filter_cars_by_price_range(self):
        response = self.client.get(
            "/cars/?price_min=60000&price_max=80000", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.car2.id)

    def test_filter_cars_by_mileage(self):
        response = self.client.get(
            "/cars/?mileage_min=0&mileage_max=10000", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.car2.id)

    def test_filter_cars_by_color(self):
        response = self.client.get(
            "/cars/?exterior_color=White&interior_color=Black", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.car2.id)

    def test_filter_cars_by_transmission(self):
        response = self.client.get("/cars/?transmission=Automatic", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # car1 and car2
        car_ids = [car["id"] for car in response.data]
        self.assertIn(self.car1.id, car_ids)
        self.assertIn(self.car2.id, car_ids)

    def test_filter_cars_on_sale(self):
        response = self.client.get("/cars/?is_on_sale=True", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        car_ids = [car["id"] for car in response.data]
        self.assertIn(self.car1.id, car_ids)
        self.assertIn(self.car2.id, car_ids)

        response = self.client.get("/cars/all/?is_on_sale=False", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.car3.id)

    def test_invalid_year_filter(self):
        response = self.client.get(
            "/cars/?year_min=two_thousand&year_max=2020", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("year_min", response.data)

    def test_invalid_price_filter(self):
        response = self.client.get("/cars/?price_min=chh&price_max=10000", format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price_min", response.data)

  
