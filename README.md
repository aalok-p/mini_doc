# Mini Doc Bookings

Backend service for authenticated users to book diagnostic tests at centres and complete simulated payments.

## Tech Stack

- FastAPI + SQLAlchemy 2.0 (async) + Alembic
- Supabase (my go to) or use Postgresql)
- JWT authentication (python-jose + bcrypt)

## Setup

### Environment

Copy `.env.example` to `.env` and fill in your values:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/diagnostic_db
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Local (without Docker)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

API is at `http://localhost:8000`. Interactive docs at `/docs`.

### Docker

```bash
docker-compose up --build
```

Migrations run automatically. To stop and remove the database:

```bash
docker-compose down -v
```

### Seed Data

After the database is ready, run the seed script to insert sample centres and tests:

**Local:**
```bash
source venv/bin/activate
python tmp/seed_data.py
```

**Docker:**
```bash
docker compose exec app python tmp/seed_data.py
```

## API Endpoints

### Auth

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/signup` | No | Register a new user |
| POST | `/auth/login` | No | Login (form data) and get JWT token |
| GET | `/auth/me` | Bearer | Get current user profile |

**Signup:**
```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"a@b.com","password":"secret123","full_name":"Alok"}'
```

**Login:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=a@b.com&password=secret123"
```

**Me:**
```bash
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer <token>"
```

### Diagnostics (public, no auth)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/centres` | List all active diagnostic centres |
| GET | `/centres/{id}` | Get a specific centre |
| GET | `/centres/{id}/tests` | List tests available at this centre with prices |
| GET | `/tests` | List all active diagnostic tests |
| GET | `/tests/{id}` | Get a specific test |

**List centres:**
```bash
curl http://localhost:8000/centres
```

**Get tests at a centre:**
```bash
curl http://localhost:8000/centres/<centre-id>/tests
```

### Bookings (Bearer token required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/bookings` | Create a booking |
| GET | `/bookings` | List my bookings |
| GET | `/bookings/{id}` | Get a specific booking |
| PATCH | `/bookings/{id}/cancel` | Cancel a pending booking |

**Create booking:**
```bash
curl -X POST http://localhost:8000/bookings \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "test_id": "<test-uuid>",
    "centre_id": "<centre-uuid>",
    "appointment_datetime": "2026-10-15T10:00:00+00:00"
  }'
```

**Cancel booking:**
```bash
curl -X PATCH http://localhost:8000/bookings/<booking-id>/cancel \
  -H "Authorization: Bearer <token>"
```

### Payments (Bearer token required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/payments` | Pay for a pending booking |

**Create payment:**
```bash
curl -X POST http://localhost:8000/payments \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "booking_id": "<booking-uuid>",
    "idempotency_key": "attempt-1"
  }'
```

## Database Schema

| Table | Key Columns | Notes |
|-------|-------------|-------|
| `users` | `id`, `email`, `hashed_password`, `full_name` | User = patient in this domain |
| `diagnostic_centres` | `id`, `name`, `city`, `location` | Physical test locations |
| `diagnostic_tests` | `id`, `name`, `description` | Medical tests/procedures |
| `centre_tests` | `centre_id`, `test_id`, `price`, `duration_minutes` | Junction table with pricing |
| `bookings` | `id`, `user_id`, `test_id`, `centre_id`, `appointment_datetime`, `amount`, `status` | Unique constraint on `(centre_id, test_id, appointment_datetime)` prevents double-booking |
| `payments` | `id`, `booking_id`, `amount`, `status`, `transaction_reference`, `idempotency_key` | Multiple payment records per booking for audit trail |

### Relationships

- `users` → `bookings` → `payments`
- `diagnostic_centres` ↔ `diagnostic_tests` via `centre_tests`

## what I would do if i have more time

- **Async payment processing** - Move the mock payment to a background task instead of blocking
- **A Interactive web app** - to play with api endpoint
- **Webhook endpoint** - Implement `POST /payments/webhook` with `X-Mock-Secret` validation and `event_id` deduplication
- **Notifications** - Email/SMS on booking confirmation, reminders before appointment
- **Admin endpoints** - CRUD for centres and tests, viewing all bookings
- **Redis caching** - Cache centre and test listings
- **Rate limiting** - On auth and payment endpoints
- **Search/filter** - Filter centres by city, filter tests by name
- **Predefined time slots** - Instead of free-form datetime, offer 9am, 10am, 11am slots per centre
- **Test coverage** - Add tests for diagnostic, booking, and payment routers
