FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /tubber/

RUN pip install pipenv
COPY Pipfile Pipfile.lock /tubber/
RUN pipenv install --system --dev

COPY . /tubber/

EXPOSE 8000
