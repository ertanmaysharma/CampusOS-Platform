# CampusOS

**An Autonomous AI Workforce for Smarter Campus Operations**

## Overview

CampusOS is a full-stack autonomous multi-agent AI workforce platform for university/campus operations. It uses a custom LangGraph-inspired pipeline to orchestrate AI agents that automatically classify, route, analyze, and resolve campus requests — with human-in-the-loop approval for sensitive actions.

---

## Deployment

### Architecture

```
GitHub
 ├── Vercel  → React Frontend (Vite)
 └── Render  → Flask Backend (Gunicorn) → PostgreSQL (SQLAlchemy)
```

```
Vercel Frontend
       │  /api/* rewritten to backend
       ▼
Render Flask Backend
       │
       ▼
PostgreSQL Database
```

---

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Production-ready CampusOS"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/campusos.git
git push -u origin main
```

---

### 2. Deploy Backend (Render)

1. Go to [Render](https://dashboard.render.com) → **New Web Service**
2. Connect your GitHub repository
3. Configure:
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn wsgi:app --bind 0.0.0.0:$PORT`
4. Add environment variables:

   | Variable | Value |
   |----------|-------|
   | `DATABASE_URL` | Your PostgreSQL URL (e.g. from Render's free PostgreSQL or Neon) |
   | `SECRET_KEY` | Generate a random string |
   | `JWT_SECRET_KEY` | Generate a different random string |
   | `FLASK_ENV` | `production` |
   | `FLASK_DEBUG` | `0` |
   | `CORS_ORIGINS` | `https://YOUR-PROJECT.vercel.app` |
   | `FRONTEND_URL` | `https://YOUR-PROJECT.vercel.app` |

5. Deploy → note the Render URL (e.g. `https://campusos-backend.onrender.com`)

**Initialize the production database:**
```bash
# After first deploy, run seed script via Render shell or a one-off job
cd backend
python seed.py
```

**Verify:**
```
GET https://campusos-backend.onrender.com/api/health
# → {"status": "ok", "database": "connected", "message": "CampusOS API is running"}
```

---

### 3. Deploy Frontend (Vercel)

1. Go to [Vercel](https://vercel.com) → **Import Project**
2. Connect your GitHub repository
3. Configure:
   - **Framework:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
4. Add environment variable:

   | Variable | Value |
   |----------|-------|
   | `BACKEND_URL` | `https://campusos-backend.onrender.com` |

5. Update `frontend/vercel.json` — replace `YOUR-RENDER-BACKEND.onrender.com` with your actual Render URL:
   ```json
   {
     "rewrites": [
       { "source": "/api/:path*", "destination": "https://YOUR-ACTUAL-RENDER-URL.onrender.com/api/:path*" },
       { "source": "/((?!assets/|.*\\.).*)", "destination": "/index.html" }
     ]
   }
   ```
6. Deploy

---

### 4. Environment Variables

#### Frontend (Vercel)

| Variable | Purpose | Example |
|----------|---------|---------|
| `BACKEND_URL` | Backend API base URL for Vercel rewrites | `https://campusos-backend.onrender.com` |

#### Backend (Render)

| Variable | Purpose | Example |
|----------|---------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/dbname` |
| `SECRET_KEY` | Flask secret key | `your-random-secret-key` |
| `JWT_SECRET_KEY` | JWT signing secret | `your-jwt-secret-key` |
| `FLASK_ENV` | Environment mode | `production` |
| `FLASK_DEBUG` | Debug mode (must be 0 in prod) | `0` |
| `CORS_ORIGINS` | Allowed frontend origins (comma-separated) | `https://your-app.vercel.app` |
| `FRONTEND_URL` | Frontend URL (for CORS / reference) | `https://your-app.vercel.app` |
| `JWT_ACCESS_TOKEN_EXPIRES` | Access token TTL in seconds | `3600` |
| `JWT_REFRESH_TOKEN_EXPIRES` | Refresh token TTL in seconds | `2592000` |
| `LLM_API_KEY` | OpenAI/LLM API key (optional, demo mode without) | `sk-...` |
| `LLM_MODEL` | LLM model name | `gpt-3.5-turbo` |
| `LLM_BASE_URL` | Custom LLM base URL (if needed) | `` |

> **Never commit actual secrets.** Use `.env.example` as a template.

---

## Quick Start (Local Development)

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

### Option 1: Docker (Recommended)

```bash
docker-compose up -d
```

### Option 2: Manual Setup

**Database:**
```bash
createdb campusos
# Or use Docker just for Postgres:
docker run -d --name campusos-db -e POSTGRES_USER=campusos -e POSTGRES_PASSWORD=campusos -e POSTGRES_DB=campusos -p 5432:5432 postgres:15-alpine
```

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env
# Edit .env with your database credentials
python run.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Seed Database:**
```bash
cd backend
python seed.py
```

### Initialize Migrations

```bash
cd backend
export FLASK_APP=app
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@campusos.local | Admin123! |
| Manager | manager@campusos.local | Manager123! |
| Staff | staff@campusos.local | Staff123! |
| Student | student@campusos.local | Student123! |
| Faculty | faculty@campusos.local | Faculty123! |

---

## API Endpoints

### Authentication
- `POST /api/auth/register` — Register new user
- `POST /api/auth/login` — Login
- `POST /api/auth/refresh` — Refresh token
- `GET /api/auth/me` — Current user
- `POST /api/auth/change-password` — Change password

### Requests
- `POST /api/requests` — Create request
- `GET /api/requests` — List requests (with filters)
- `GET /api/requests/:id` — Get request details
- `PATCH /api/requests/:id` — Update request
- `DELETE /api/requests/:id` — Cancel request
- `POST /api/requests/:id/process` — Process through AI workflow

### Workflows
- `GET /api/workflows` — List workflows
- `GET /api/workflows/:id` — Get workflow details

### Approvals
- `GET /api/approvals` — List pending approvals
- `POST /api/approvals/:id/approve` — Approve action
- `POST /api/approvals/:id/reject` — Reject action

### Dashboard
- `GET /api/dashboard/student` — Student dashboard
- `GET /api/dashboard/admin` — Admin dashboard

### Admin
- `GET /api/users` — List users
- `POST /api/users` — Create user
- `GET /api/admin/roles` — List roles
- `GET /api/departments` — List departments
- `POST /api/departments` — Create department
- `GET /api/knowledge` — Knowledge base
- `GET /api/audit-logs` — Audit logs

### Health Check
- `GET /api/health` — Health status (no auth required)

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, JavaScript, Vite |
| Backend | Python, Flask |
| Database | PostgreSQL, SQLAlchemy |
| AI/Agents | Custom LangGraph-inspired pipeline |
| Auth | JWT (Flask-JWT-Extended) |
| ORM | Flask-SQLAlchemy |
| Migrations | Flask-Migrate (Alembic) |
| Production Server | Gunicorn |

---

## Project Structure

```
campusos/
├── backend/
│   ├── app/
│   │   ├── models/          # SQLAlchemy models
│   │   ├── routes/          # Flask blueprints
│   │   ├── services/        # Business logic
│   │   ├── agents/          # AI agent pipeline
│   │   ├── tools/           # Agent tools
│   │   ├── schemas/         # Validation schemas
│   │   └── utils/           # Helpers, decorators
│   ├── tests/               # Backend tests
│   ├── seed.py              # Database seeder
│   ├── run.py               # Dev entry point
│   ├── wsgi.py              # Production WSGI entrypoint
│   ├── render.yaml          # Render deployment config
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/           # React pages
│   │   ├── layouts/         # App layout
│   │   ├── context/         # Auth context
│   │   └── services/        # API client
│   ├── vercel.json          # Vercel deployment config
│   └── package.json
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Testing

```bash
cd backend
pip install pytest
pytest tests/ -v
```

---

## AI Workflow

When a request is submitted:

1. **Intake** — Extracts and normalizes request data
2. **Classification** — Categorizes into Maintenance, IT, Finance, etc.
3. **Priority** — Determines urgency (Low/Medium/High/Critical)
4. **Research** — Retrieves relevant knowledge base articles
5. **Routing** — Assigns to appropriate department
6. **Analysis** — Generates action recommendations
7. **Verification** — Safety check on proposed actions
8. **Approval** — Routes to human reviewer if needed
9. **Action** — Executes approved actions via tools
10. **Communication** — Generates user-facing messages
11. **Audit** — Logs complete workflow trail

---

## Deployment Checklist

### Before GitHub
- [ ] `.env` removed from repository
- [ ] Secrets removed
- [ ] `.gitignore` configured
- [ ] `.env.example` created
- [ ] README updated
- [ ] Dependencies verified

### Vercel (Frontend)
- [ ] `frontend/vercel.json` — backend URL updated
- [ ] Framework set to Vite
- [ ] Root directory set to `frontend`
- [ ] `BACKEND_URL` environment variable set
- [ ] Production build succeeds
- [ ] Client-side routing works (SPA rewrite)

### Render (Backend)
- [ ] Root directory set to `backend`
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `gunicorn wsgi:app --bind 0.0.0.0:$PORT`
- [ ] `DATABASE_URL` set to production PostgreSQL
- [ ] `SECRET_KEY` and `JWT_SECRET_KEY` set to random values
- [ ] `CORS_ORIGINS` set to Vercel URL
- [ ] `/api/health` returns `{"status": "ok"}`
- [ ] Database seeded with `python seed.py`

### Integration
- [ ] Vercel frontend reaches Render backend via `/api/*`
- [ ] Login/signup works
- [ ] Authenticated requests work
- [ ] CORS headers present
- [ ] No localhost URLs remain in production code

---

## Known Limitations

- LLM integration requires API key (demo mode works without it)
- Email notifications not implemented (in-app only)
- No file upload support yet
- WebSocket real-time updates not implemented

---

## License

Built for hackathon use.
