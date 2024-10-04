from django.db import models

# Brand Object:
# 1. Each brand has its own name [Audi, BMW, Mercedes]
# 2. Each brand has its own  country [Germany, Poland, USA]


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Brand Name")
    country = models.CharField(max_length=100, verbose_name="Country")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"


# Model Object:
# 1. Each model has its own name [a8, x5, E 200]
# 2. Each model has year of issue, for example 2008, 2010, 2021
# 3. Each car has body style, for example [sedan, hatchback, liftback, coupe, crossover,
# truck, wagon]


class Model_Car(models.Model):
    model_name = models.CharField(max_length=100, verbose_name="Model Name")
    year = models.IntegerField(verbose_name="Year of Issue")
    body_style = models.CharField(max_length=100, verbose_name="Body Style")

    def __str__(self):
        return f"{self.model_name} {self.year} "

    class Meta:
        verbose_name = "Model"
        verbose_name_plural = "Models"


# Car Object:
# 1. Each car has Brand [related to Brand Object]
# 2. Each car has Model [related to Model Object]
# 3. Each car has its own price, for example 100000 (in USD)
# 4. Each car has mileage, for example [1000, 37500, 220000] (in kilometers)
# 5. Each car has exterior color, for example [blue, black, gray]
# 6. Each car has interior color, for example [black, white, orange]
# 7. Each car has fuel type, for example [gas, diesel]
# 8. Each car has transmission [automatic, manual]
# 9. Each car has engine, for example [2.0L, 1.4L, 3.0L, 5.0L]
# 10. Each car can be on sale [boolean is_on_sale = True/False]


class Car(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="Brand")
    model = models.ForeignKey(Model_Car, on_delete=models.CASCADE, verbose_name="Model")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    transmission = models.CharField(max_length=50, verbose_name="Transmission")
    engine = models.CharField(max_length=50, verbose_name="Engine")
    mileage = models.PositiveBigIntegerField(verbose_name="Mileage")
    exterior_color = models.CharField(max_length=50, verbose_name="Exterior Color")
    interior_color = models.CharField(max_length=50, verbose_name="Interior Color")
    fuel_type = models.CharField(max_length=50, verbose_name="Fuel Type")
    is_on_sale = models.BooleanField(verbose_name="Is on Sale")

    def __str__(self):
        return f"{self.brand} {self.model}"

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"
