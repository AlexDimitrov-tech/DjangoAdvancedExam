# BoardGameConnect

Just a Django app idea for local board game people.

Goal (eventually): you can list your games, browse other people’s games, request to borrow them, and leave reviews.

Right now it’s basically the “starter base” of the project, but it already runs.

## The basic plan (messy notes)

I’m keeping it as **exactly 5 Django apps** so it doesn’t turn into spaghetti:

* `accounts` — login/signup, profiles, roles
* `catalog` — games + categories and showing them
* `rentals` — borrow requests / approvals / returns
* `reviews` — ratings + comments (games + maybe users too)
* `api` — DRF endpoints

Models we want to end up with:

* `CustomUser` (extends `AbstractUser`) with stuff like location/avatar/bio
* `Game` (belongs to an owner user)
* `Category` (games can have many categories)
* `Rental` (game + borrower + status)
* `Wishlist` (users can save games they want)

Permissions idea (later in admin groups):

* Owners: can manage their own games + approve rental requests
* Renters: can browse + request rentals + write reviews

Other stuff I want later (not doing all of this yet): mostly CBVs, a bunch of forms, Bootstrap templates, DRF for catalog, Celery+Redis for overdue rentals + emails, tests, then containerize/deploy.

---

## What actually works right now

Auth works:

* signup
* login
* logout
* a simple “my profile” page

Catalog works (super basic):

* `Game` + `Category` models
* game list page
* game detail page
* add game page (you need to be logged in)

Also there’s a tiny DRF endpoint just to prove DRF is wired: `/api/ping/`.

## How to run it

If you already have a venv, just activate it. Otherwise:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Optional admin user:

```bash
python manage.py createsuperuser
```

## Links (when the server is running)

* Home: `http://127.0.0.1:8000/`
* Sign up: `http://127.0.0.1:8000/accounts/signup/`
* Login: `http://127.0.0.1:8000/accounts/login/`
* Profile: `http://127.0.0.1:8000/accounts/me/`
* Catalog: `http://127.0.0.1:8000/catalog/`
* Add game: `http://127.0.0.1:8000/catalog/games/new/`
* Admin: `http://127.0.0.1:8000/admin/`
* API ping: `http://127.0.0.1:8000/api/ping/`
