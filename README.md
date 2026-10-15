# Lost & Found

A web application for publishing lost and found items, built with **Django and PostgreSQL**.

**[Open the live application](https://lostfound.scirtor.com)** · [Developer portfolio](https://scirtor.com)

## Features

- User registration and authentication.
- Item listings with **lost**, **found** and **returned** statuses.
- Categories, locations and optional item photos.
- Comments on listings.
- Views for adding, editing and deleting items.
- JSON endpoints for items and comments.

## Stack

Python · Django · PostgreSQL · Gunicorn · Docker Compose

## Run with Docker

1. Copy `.env.example` to `.env`.
2. Configure the database values in `.env` to match the PostgreSQL service in `docker-compose.yml`, and set your own `DJANGO_SECRET_KEY`.
3. Build and start the services:

```bash
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). The Compose file binds the web service to the local interface.

## Repository map

- `main/models.py` — items, categories, locations and comments.
- `main/views.py` — page views, account flows and JSON endpoints.
- `myproject/` — Django project configuration.
- `media/` — uploaded item images.
- `Dockerfile` and `docker-compose.yml` — application and database services.

This project is part of my software development portfolio alongside cybersecurity labs and CTF practice.

