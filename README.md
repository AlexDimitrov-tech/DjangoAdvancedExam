# BoardGameConnect

BoardGameConnect is a Django-based web application designed for local board‑game communities.  
Users can list the games they own, browse games from other members, request to borrow them, and leave reviews.  
The project is structured into multiple Django apps and follows clean, modular architecture.

---

## 🚀 Features (Current Progress)

### 👤 Accounts
- Custom user model extending Django’s `AbstractUser`
- Registration, login, logout
- Basic profile page

### 🎲 Catalog
- Game & Category models
- Game list and detail pages
- Add‑a‑game form (login required)

### 🔄 Rentals (in progress)
- Base structure for borrow requests and approvals

### ⭐ Reviews (in progress)
- Ratings & comments for games

### 🧩 API
- DRF wired and functional
- Example endpoint: `/api/ping/`

---

## 🗂 Project Structure

The project is intentionally organized into **exactly five Django apps**:

- `accounts` — authentication, profiles, roles  
- `catalog` — games, categories, browsing  
- `rentals` — borrow requests & workflow  
- `reviews` — ratings & comments  
- `api` — REST API endpoints  

This separation keeps responsibilities clear and avoids unnecessary coupling.

---

## 🛠 Installation & Setup

### 1. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```
