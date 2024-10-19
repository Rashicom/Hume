FROM python:3.11

WORKDIR /code

RUN apt-get -y update
RUN apt-get -y upgrade

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install poetry
COPY ./poetry.lock ./pyproject.toml /code/

RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-root --no-interaction

EXPOSE 8000

COPY . /code/

WORKDIR /code/Hume

CMD [ "/bin/bash", "-c", "python manage.py runserver 0.0.0.0:8000" ]