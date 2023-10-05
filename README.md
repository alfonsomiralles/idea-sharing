# idea-sharing

## Overview
This project is a GraphQL API developed with Python, Django and PostgreSQL.
A platform where users can authenticate, share ideas, follow each other, and receive notifications.

## Features
- Register with email, username, and password.
- Login using email and password.
- Change or reset password via email with a magic link.
- Publish, view and delete short text ideas.
- Set and edit visibility settings: public, protected, or private.
- Send, view, approve, or deny follow requests.
- View lists of following and followers.
 -Unfollow or remove followers.
- Search for users by username.
- View other users' ideas based on visibility settings.
- See a timeline of ideas from self and followed users based on visibility.
- Receive notifications when a followed user posts a new accessible idea.

## Prerequisites
Before you begin, make sure you have the following installed:

- Docker
- Docker Compose
- PostgreSQL
- Python 3.10.11
- Django 3.2

## Getting Started
To set up the project, follow these steps:

## Clone the repository:
```bash
git clone https://github.com/alfonsomiralles/idea-sharing.git
```

## Environment Setup
### Virtual Environment

Before running the project, set up a Python virtual environment:

```bash
python -m venv venv
```

## Enviroment Variables
Create a .env file in the project root to set the following variables:
```env
# Django settings
SECRET_KEY:Your Django secret key
DEBUG=1 # Set to 0 in production
# Allowed hosts
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 172.19.0.2 [::1]
# Database settings
SQL_ENGINE=django.db.backends.postgresql
SQL_HOST=db
SQL_PORT=5432
POSTGRES_DB=Your PostgreSQL database name
POSTGRES_USER=Your PostgreSQL user
POSTGRES_PASSWORD=Your PostgreSQL password
```

## Build the Docker images:
```bash
docker-compose build
```

## Run the Docker containers:
```bash
docker-compose up
```

## Perform database migrations:
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

# API Usage
## Access Admin Panel
To create superuser, run
```bash
docker-compose exec web python manage.py createsuperuser
```
Then, access the admin panel at http://localhost:8000/admin/

## GrraphQL Panel
Access the GraphQL panel at http://localhost:8000/graphql/

## Postman Collection
A Postman collection is provided for your convenience to test GraphQL queries.
