# idea-sharing

## Prerequisites
Before you begin, make sure you have the following installed:

- Docker
- Docker Compose

## Getting Started
To set up the project, follow these steps:

Clone the repository:
```bash
git clone https://github.com/alfonsomiralles/MentorshipPlatformAPI.git
```
Build the Docker images:
```bash
docker-compose build
```
Run the Docker containers:
```bash
docker-compose up -d
```
Perform the database migrations:
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```
## Now the API should be up and running at http://localhost:8000.

docker-compose exec web python manage.py createsuperuser

## API Endpoints
To acces admin panel
Create superuser
```bash
docker-compose exec web python manage.py createsuperuser
```
http://localhost:8000/admin