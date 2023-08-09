# Choose the proper python image
FROM python:3
ENV PYTHONUNBUFFERED=1

# Define working directory
WORKDIR /app

# Copy Pipefiles to the all directory
COPY Pipfile Pipfile.lock /app/

# Install all dependencies
RUN pip install pipenv \
    && pipenv install --system --deploy

# Copy the remaining files to app directory
COPY . /app

EXPOSE 8000