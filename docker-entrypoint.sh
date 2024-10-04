#!/bin/bash

poetry run python ./car_api/manage.py migrate

exec "$@"