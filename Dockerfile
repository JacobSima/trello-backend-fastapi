FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv \
    && pipenv install --system --deploy
COPY . /app
EXPOSE 8000