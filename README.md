# Finance Backend

A backend API for a finance dashboard system built with **FastAPI** and **PostgreSQL**. Supports role-based access control, financial record management, and dashboard analytics.

---

## Tech Stack

| Layer | Choice |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Auth | JWT (python-jose) |
| Validation | Pydantic v2 |
| Password Hashing | bcrypt (passlib) |

---

## Project Structure

```
finance-backend/
├── app/
│   ├── api/v1/
│   │   ├── auth.py          # Login, token
│   │   ├── users.py         # User management
│   │   ├── transactions.py  # Financial records
│   │   └── dashboard.py     # Aggregated analytics
│   ├── core/
│   │   ├── config.py        # Environment settings
│   │   ├── database.py      # DB session
│   │   ├── security.py      # JWT + password utils
│   │   └── dependencies.py  # Auth + RBAC dependencies
│   ├── models/
│   │   ├── user.py          # User ORM model
│   │   └── transaction.py   # Transaction ORM model
│   ├── schemas/
│   │   ├── user.py          # User request/response shapes
│   │   ├── transaction.py   # Transaction request/response shapes
│   │   └── dashboard.py     # Dashboard response shapes
│   ├── repositories/
│   │   ├── user_repository.py         # User DB queries
│   │   └── transaction_repository.py  # Transaction DB queries
│   └── services/
│       ├── user_service.py        # User business logic
│       ├── transaction_service.py # Transaction business logic
│       └── dashboard_service.py   # Analytics logic
├── alembic/                 # DB migrations
├── main.py
├── requirements.txt
└── .env
```

---

## Setup

### 1. Clone and install dependencies

```bash
git clone <repo-url>
cd finance-backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file in the root:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/financedb
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Run migrations

```bash
alembic upgrade head
```

### 4. Start the server

```bash
uvicorn main:app --reload
```

API will be available at `http://localhost:8000`
Swagger docs at `http://localhost:8000/docs`

---

## Roles & Permissions

| Action | Viewer | Analyst | Admin |
|---|---|---|---|
| View transactions | ✅ | ✅ | ✅ |
| View dashboard summary | ❌ | ✅ | ✅ |
| Create transactions | ❌ | ❌ | ✅ |
| Update transactions | ❌ | ❌ | ✅ |
| Delete transactions | ❌ | ❌ | ✅ |
| Manage users | ❌ | ❌ | ✅ |

---

## API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/auth/login` | Login and get JWT token |

### Users *(Admin only)*
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/users/` | List all users |
| POST | `/api/v1/users/` | Create a user |
| GET | `/api/v1/users/{id}` | Get user by ID |
| PATCH | `/api/v1/users/{id}` | Update user |
| DELETE | `/api/v1/users/{id}` | Delete user |

### Transactions
| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/api/v1/transactions/` | All roles | List transactions (with filters) |
| POST | `/api/v1/transactions/` | Admin | Create transaction |
| GET | `/api/v1/transactions/{id}` | All roles | Get transaction by ID |
| PATCH | `/api/v1/transactions/{id}` | Admin | Update transaction |
| DELETE | `/api/v1/transactions/{id}` | Admin | Soft delete transaction |

**Filters supported on GET `/transactions/`:**
- `type` — `income` or `expense`
- `category` — filter by category name
- `from_date` — start date (YYYY-MM-DD)
- `to_date` — end date (YYYY-MM-DD)

### Dashboard
| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/api/v1/dashboard/summary` | Analyst, Admin | Total income, expenses, net balance, category breakdown |

---

## Data Models

### User
| Field | Type | Notes |
|---|---|---|
| id | Integer | Primary key |
| email | String | Unique |
| full_name | String | |
| role | Enum | viewer, analyst, admin |
| is_active | Boolean | Default true |
| created_at | DateTime | Auto |

### Transaction
| Field | Type | Notes |
|---|---|---|
| id | Integer | Primary key |
| amount | Decimal(12,2) | Must be positive |
| type | Enum | income or expense |
| category | String | |
| date | Date | |
| description | Text | Optional |
| is_deleted | Boolean | Soft delete flag |
| created_by | Integer | FK to users |
| created_at | DateTime | Auto |

---

## Authentication

All protected endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer <your_token>
```

Get a token by calling `POST /api/v1/auth/login` with your email and password.

---

## Assumptions Made

- Transactions can only be created, updated, or deleted by admins. Viewers and analysts have read-only access.
- Soft delete is used for transactions — records are never permanently removed, just marked as deleted. This is standard practice for financial systems.
- Integer IDs are used instead of UUIDs for simplicity and query performance, appropriate for this scale.
- Dashboard summary aggregates all non-deleted transactions in the system.
- User registration is done by an admin via the users endpoint, not through a public signup route.

---

## Notes

- Full Swagger UI available at `/docs` — all endpoints are documented and testable there.
- Passwords are hashed using bcrypt before storage.
- JWT tokens expire after 30 minutes (configurable in `.env`).