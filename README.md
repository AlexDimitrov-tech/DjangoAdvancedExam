# BoardGameConnect

BoardGameConnect is a Django web app for local board-game communities.

The idea is simple: people create profiles, share the games they own, browse what others have listed, send borrow requests, and leave reviews after playing. I wanted the project to feel like a practical community platform instead of just a collection of disconnected CRUD pages.

## What the project does

BoardGameConnect has both a public and a private part.

### Public area
Visitors can:
- open the home page and see recent activity
- browse the game catalog
- open game details
- explore categories
- read user reviews
- use the REST API endpoints for game data

### Private area
Authenticated users can:
- register, log in, and log out
- manage their profile
- add, edit, and delete their own games
- create, edit, and delete categories
- send rental requests for games listed by other users
- review games
- favorite games
- track rental-related notifications

## Project structure

The application is organized into five Django apps with separate responsibilities:

- `accounts` - authentication, profile data, and user roles
- `catalog` - games and categories
- `rentals` - borrow requests, statuses, and notifications
- `reviews` - ratings and written reviews
- `api` - Django REST Framework endpoints

Keeping the project split this way made it easier to reason about features and avoid putting everything into one giant app.

## Main features

- Custom user model based on Django `AbstractUser`
- Public and private sections
- Two predefined user groups: `Member` and `CommunityAdmin`
- Class-based views used across the project
- Full CRUD flows for multiple resources
- Searchable catalog
- Rental request workflow with statuses
- Review system with star rendering through a custom template filter
- REST API for games
- Custom error pages
- Responsive layout with Bootstrap
- Background task processing with Celery and Redis

## Tech stack

- Python
- Django
- Django REST Framework
- Celery
- Redis
- SQLite by default for easy local setup
- Optional PostgreSQL support
- Gunicorn
- WhiteNoise
- Bootstrap 5

## Local setup

### 1. Clone the project
```bash
git clone <your-repository-url>
cd BoardGameConnect
```

### 2. Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Create your environment file
```bash
cp .env.example .env
```

Then load it:
```bash
set -a
source .env
set +a
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Create an admin user
```bash
python manage.py createsuperuser
```

### 7. Collect static files
```bash
python manage.py collectstatic --noinput
```

### 8. Start the development server
```bash
python manage.py runserver
```

Open the app at:
- `http://127.0.0.1:8000/`
- admin panel: `http://127.0.0.1:8000/admin/`

## Environment variables

The sample `.env.example` file is enough to start locally with SQLite.

Minimum local settings:

```env
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_SECRET_KEY=change-me-for-local-development
```

### Optional PostgreSQL setup
If you want to use PostgreSQL instead of SQLite, fill these values:

```env
POSTGRES_DB=boardgameconnect
POSTGRES_USER=boardgameconnect
POSTGRES_PASSWORD=change-me
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
```

If `POSTGRES_DB` is left empty, the project uses SQLite.

## Running background tasks

Rental status updates create notifications through Celery.

### Start Redis
```bash
redis-server
```

### Start the Celery worker
In a second terminal, with the same virtual environment and environment variables loaded:

```bash
celery -A boardgameconnect worker -l info
```

## API endpoints

The project includes a small REST API:

- `GET /api/ping/`
- `GET /api/games/`
- `GET /api/games/<id>/`

## Tests

To run the test suite:

```bash
python manage.py test
```

## Deployment notes

For production, the app can run with:
- Gunicorn as the application server
- Caddy or Nginx as a reverse proxy
- WhiteNoise for static files
- Redis and Celery for background processing
- SQLite or PostgreSQL as the relational database

Minimum production environment settings:

```env
DJANGO_DEBUG=0
DJANGO_SECRET_KEY=your-secret-key
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

## Final note

This project was built to show a complete Django application with authentication, permissions, modular structure, class-based views, REST endpoints, template rendering, async processing, testing, and deployment.

It is not meant to be just a demo homepage with a few forms glued onto it — the goal was to build something that feels like a real small community platform.
