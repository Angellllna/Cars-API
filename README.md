# Cars-API

Welcome to **Cars-API**, a Django-based application for searching cars. This project provides a set of endpoints to easily interact with car data, including models, brands, and available listings.

## Features

- Create, manage, and search car brands, models, and listings.
- Comprehensive filtering options to refine search results.
- Command utilities for generating and fetching cars.
- File upload support for adding car data directly.

## Getting Started

### 1. Project Initialization

To set up the project, create and activate a virtual environment:

```bash
# MacOS/Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

Install all dependencies using Poetry:

```bash
poetry install
```

### 2. Database Setup

After making changes to the models, create and apply migrations:

```bash
python ./car_api/manage.py makemigrations
python ./car_api/manage.py migrate
```

### 3. Running the Server

To start a local server:

```bash
python ./car_api/manage.py runserver
```

### 4. Running Tests

To run the tests for the cars app:

```bash
python ./car_api/manage.py test cars
```

## Special Commands

### 5. Using Special Commands

- Generate random cars:
  ```bash
  python ./car_api/manage.py generate_cars <number_of_cars>
  ```
- Fetch cars from an external API:
  ```bash
  python ./car_api/manage.py fetch_cars <number_of_cars>
  ```

### 6. Other Useful Commands

- Launch the Django shell (an interactive interface for working with models):
  ```bash
  python ./car_api/manage.py shell
  ```

## API Endpoints

### 7. Endpoints

```http
POST /user/create/
```

Create a new user [fields: username, email, password, confirm password]

```http
POST /user/login/
```

Login user [fields: username/email, password]

```http
GET /brands/
```

List all brand objects

```http
GET /models/
```

List all model objects

```http
GET /cars/
```

List all car objects that are on sale (see `is_on_sale` in Car object)

```http
GET /cars/all/
```

List all car objects (both on sale and not on sale)

```http
POST /cars/upload/
```

Upload a file to add car data directly [file format: CSV, JSON]

### 8. Filters

Each endpoint supports filters for each field. Examples:

```http
GET /brands/?name=BMW
```

Returns only the BMW brand, if it exists in the database.

```http
GET /brands/?country=Germany
```

Returns all brands headquartered in Germany.

```http
GET /cars/?model_name=X5
```

Returns a list of cars with model name X5 that are currently on sale.

Users can add multiple filters:

```http
GET /cars/?model_name=X5&engine=2.0L&fuel_type=Diesel
```

Returns all BMW X5 cars with a 2.0L engine and diesel fuel type that are currently on sale.

```http
GET /cars/?brand_name=Mercedes&engine=5.0L&fuel_type=Electric
```

Returns all Mercedes cars with a 5.0L engine and electric fuel type that are currently on sale.

```http
GET /cars/?year_min=2010&year_max=2021
```
