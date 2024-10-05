from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


class Brand(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Brand Name",
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z\s]+$",
                message="Brand name should start with capital letter and contain only letters",
                code="invalid_brand_name",
            )
        ],
    )
    country = models.CharField(
        max_length=100,
        verbose_name="Country",
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z\s]+$",
                message="Country name should start with capital letter and contain only letters",
                code="invalid_country_name",
            )
        ],
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"


class Model_Car(models.Model):
    model_name = models.CharField(
        max_length=100,
        verbose_name="Model Name",
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9\s\-]+$",
                message="Model name should start with a capital letter and contain only letters and numbers.",
                code="invalid_model_name",
            )
        ],
    )
    year = models.IntegerField(
        verbose_name="Year of Issue",
        validators=[
            MinValueValidator(1886, "Cars weren't manufactured before 1886."),
            MaxValueValidator(2024, "Future cars aren't allowed yet."),
        ],
    )
    body_style = models.CharField(max_length=100, verbose_name="Body Style")

    def __str__(self):
        return f"{self.model_name} {self.year} "

    class Meta:
        verbose_name = "Model"
        verbose_name_plural = "Models"


class Car(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="Brand")
    model = models.ForeignKey(Model_Car, on_delete=models.CASCADE, verbose_name="Model")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Price",
        validators=[MinValueValidator(0, "Price should be greater than 0")],
    )
    transmission = models.CharField(
        max_length=50,
        verbose_name="Transmission",
        validators=[
            RegexValidator(
                regex=r"^(Automatic|Manual)$",
                message="Transmission should be either Automatic or Manual",
            )
        ],
    )

    engine = models.CharField(
        max_length=50,
        verbose_name="Engine",
        validators=[
            RegexValidator(
                regex=r"^\d+(\.\d+)?L$",
                message="Engine size must be in format like 2.0L, 1.4L, etc.",
            )
        ],
    )

    mileage = models.PositiveBigIntegerField(
        verbose_name="Mileage",
        validators=[
            MinValueValidator(0, "Mileage should be greater than or equal to 0")
        ],
    )

    exterior_color = models.CharField(
        max_length=50,
        verbose_name="Exterior Color",
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z\s]+$",
                message="Color name should start with a capital letter and contain only letters",
                code="invalid_color_name",
            )
        ],
    )
    interior_color = models.CharField(
        max_length=50,
        verbose_name="Interior Color",
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z\s]+$",
                message="Color name should start with a capital letter and contain only letters",
                code="invalid_color_name",
            )
        ],
    )
    fuel_type = models.CharField(
        max_length=50,
        verbose_name="Fuel Type",
        validators=[
            RegexValidator(
                regex=r"^(Gasoline|Diesel|Electric)$",
                message="Fuel type should be either Gasoline, Diesel or Electric",
            )
        ],
    )
    is_on_sale = models.BooleanField(verbose_name="Is on Sale", default=False)

    def __str__(self):
        return f"{self.brand} {self.model}"

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"
