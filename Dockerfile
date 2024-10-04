FROM python:3.11-slim


WORKDIR /car_api

COPY pyproject.toml .

RUN pip install poetry



# COPY . /app-marcket/
RUN poetry install
EXPOSE 8000

# Install dependencies
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

CMD ["poetry", "run", "./car_api/python", "manage.py", "runserver"]

# comand for run: docker-compose up --build
# http://localhost:8000

