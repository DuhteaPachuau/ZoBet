# ZoBet

Mizoram's tournament prediction platform. Predict winners, win rewards.

## Setup

1. Clone & create virtual environment
2. Copy \.env.example\ to \.env\ and fill in values
3. \pip install -r requirements.txt\
4. \python manage.py migrate\
5. \python manage.py createsuperuser\
6. \python manage.py runserver\

Optional: Set \DATABASE_URL\ in \.env\ for NeonDB PostgreSQL (defaults to SQLite).
Optional: Set \CLOUDINARY_URL\ in \.env\ for Cloudinary image hosting.

