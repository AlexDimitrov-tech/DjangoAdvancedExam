# BoardGameConnect: Development Plan

This document outlines my development plan for BoardGameConnect, a web application designed for local board game enthusiasts to catalog, review, and rent games from one another. The project will be built using Django and Django REST Framework, adhering to strict architectural and structural requirements.

## Core Architecture

I will divide the project into exactly five modular Django apps to separate concerns and maintain clean code:

1.  **`accounts`**: Will handle custom user authentication, profiles, and role management.
2.  **`catalog`**: Will manage the board games, categories, and inventory display.
3.  **`rentals`**: Will track borrowing requests, approvals, and return statuses.
4.  **`reviews`**: Will handle user-generated ratings and comments for both games and other users.
5.  **`api`**: Will serve as the dedicated Django REST Framework app for external data access.

## Database Design & Models

I am extending the built-in Django `AbstractUser` to create a custom user model. The database will use PostgreSQL and consist of the following core models to satisfy the relational requirements:

* **CustomUser**: Extended with fields like location, avatar, and bio.
* **Game**: Stores game details (title, description, player count). 
    * *Relationship:* Foreign Key to `CustomUser` (the owner).
* **Category**: Genre tags for the games (e.g., Strategy, Party).
    * *Relationship:* Many-to-Many with `Game`.
* **Rental**: Tracks the transaction between two users.
    * *Relationship:* Foreign Key to `Game` and Foreign Key to `CustomUser` (the borrower).
* **Wishlist**: A collection of games a user wants to play.
    * *Relationship:* Many-to-Many between `CustomUser` and `Game`.

## Roles and Permissions

I will configure two primary user groups in the Django admin panel with distinct permission sets:
* **Owners**: Users who list their games. They have full CRUD permissions over their own game listings and can approve/reject rental requests.
* **Renters**: Users who browse the catalog. They can read game details, submit rental requests, and write reviews, but cannot modify the catalog itself.

## Development Roadmap & Technical Features

* **Views & Forms**: I will use Class-Based Views (CBVs) for roughly 90% of the application logic. I plan to build at least seven forms (e.g., Registration, Login, Add Game, Edit Profile, Request Rental, Submit Review), utilizing custom validations, read-only fields for immutable data (like rental dates once approved), and tailored error messages.
* **Frontend**: The UI will consist of 15+ templates rendered via the Django Template Engine using a base template, partials, and a responsive Bootstrap layout. Dynamic pages will include the main catalog, filtered category views, individual game details, user profiles, and customized 404/500 error pages.
* **RESTful API**: The `api` app will expose a catalog endpoint, allowing external clients to fetch game data and availability in JSON format using DRF serializers and appropriate permission classes.
* **Asynchronous Processing**: I will integrate Celery with Redis to handle background tasks. Specifically, this will be used to automatically process overdue rental statuses and send asynchronous email notifications to users.
* **Testing & Deployment**: I will write a minimum of 15 tests covering custom form validations, model methods, and critical views. Once the core features are stable, the application will be containerized and deployed to a cloud platform, utilizing environment variables to secure all sensitive credentials.
