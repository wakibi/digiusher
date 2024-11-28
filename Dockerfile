# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.13.0-slim-bullseye


# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
ENV PYTHONUNBUFFERED=1

# Install system packages required by Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
 && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
# Install any needed packages specified in requirements.txt
RUN pip install -r /code/requirements.txt
