# LexiDeck: IELTS Academic Vocabulary 

LexiDeck is a spaced-repetition flashcard application tailored for IELTS Academic Vocabulary. This repository contains the Django REST Framework backend API that manages user authentication, decks, cards, and the spaced-repetition study algorithms.

🔗 **Frontend Repository**: [lexideck-frontend](https://github.com/BipronathSaha12/lexideck-frontend)

## Tech Stack
- Python 3.10+, Django 6.x
- Django REST Framework (DRF)
- SQLite3
- `djangorestframework-simplejwt` for JWT Authentication
- `drf-spectacular` for OpenAPI / Swagger Docs
- `django-filter` and `django-cors-headers`
- `python-decouple` for environment variables

## Setup Steps

1. Clone the repository and navigate into the backend directory.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Or .\venv\Scripts\activate on Windows
   ```
3. Install dependencies:
   ```bash
   pip install django djangorestframework djangorestframework-simplejwt django-cors-headers django-filter python-decouple drf-spectacular
   ```
4. Copy the environment variables:
   ```bash
   cp .env.example .env
   ```
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. (Optional) Seed the database with the demo account, 5 full decks, and 500 study cards spanning all 5 subject categories (Programming, Language, Academic, Interview, Other):
   ```bash
   python manage.py seed_demo
   ```
7. Start the server:
   ```bash
   python manage.py runserver
   ```

## Demo & Admin Accounts
**1. Standard User (Pre-populated with 500 Cards)**
- **Username**: `demo`
- **Password**: `demo123`

**2. Admin Superuser (For Django Admin Panel)**
- **Username**: `admin`
- **Password**: `admin123`

## Environment Variables

| Variable | Description | Default |
| -------- | ----------- | ------- |
| `SECRET_KEY` | Django Secret Key | A random insecure key |
| `DEBUG` | Enable/Disable Debug Mode | `True` |

## Security & Architecture
- **Global CORS Configured**: The API explicitly permits cross-origin requests from any frontend port (via `CORS_ALLOW_ALL_ORIGINS = True`), avoiding typical Vite dev server port-blocking issues.
- **Rate Limiting**: Integrated DRF Throttling to protect endpoints (100 reqs/day for anonymous users, 1,000 reqs/day for authenticated users).
- **Environment Driven**: Fully configured to accept `DATABASE_URL` for seamless production deployment.

## Spaced Repetition Box Intervals

Cards advance based on the following schedule when answered correctly:

| Box | Next Review Due In |
| --- | ------------------ |
| 1   | 0 days (due again today) |
| 2   | 1 day |
| 3   | 3 days |
| 4   | 7 days |
| 5   | 16 days (Mastered) |

*(An incorrect answer always drops the card immediately back to Box 1, due today).*

## API Endpoints

| Endpoint | Method | Auth Level | Description |
| -------- | ------ | ---------- | ----------- |
| `/api/register/` | POST | Public | Create a new user |
| `/api/login/` | POST | Public | Obtain JWT tokens |
| `/api/token/refresh/` | POST | Public | Refresh JWT token |
| `/api/decks/` | GET/POST | JWT User | List/Create decks (owner scoped) |
| `/api/decks/<id>/` | GET/PUT/PATCH/DELETE | JWT User | Retrieve/Update/Delete deck |
| `/api/decks/<id>/study/` | GET | JWT User | Fetch up to 20 due cards |
| `/api/cards/` | GET/POST | JWT User | List/Create cards (owner scoped via deck) |
| `/api/cards/<id>/` | GET/PUT/PATCH/DELETE | JWT User | Retrieve/Update/Delete card |
| `/api/cards/<id>/review/` | POST | JWT User | Submit answer (`{"correct": true}`) |
| `/api/stats/` | GET | JWT User | Fetch user study statistics |
| `/api/schema/` | GET | Public | OpenAPI Schema |
| `/api/docs/` | GET | Public | Swagger UI Documentation |
