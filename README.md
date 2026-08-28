# 🎓 CampusOS — An Autonomous AI Workforce for Smarter Campus Operations live at (https://campus-os-platform.vercel.app/login)

> **CampusOS** is a full-stack autonomous multi-agent AI workforce platform that uses a LangGraph-inspired pipeline to orchestrate AI agents. These agents automatically classify, route, analyze, and resolve campus requests — with human-in-the-loop approval for sensitive actions.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Features](#features)
- [Database Schema](#database-schema)
- [AI Agent Workflow](#ai-agent-workflow)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Quick Start with Docker](#quick-start-with-docker)
  - [Manual Setup](#manual-setup)
- [Environment Variables](#environment-variables)
- [API Documentation](#api-documentation)
- [Frontend Pages](#frontend-pages)
- [Deployment](#deployment)
  - [Backend on Render](#backend-on-render)
  - [Frontend on Vercel](#frontend-on-vercel)
- [Testing](#testing)
- [Demo Credentials](#demo-credentials)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)

---

## Overview

University campuses generate hundreds of service requests daily — broken equipment, IT issues, facility complaints, scholarship queries, and more. Traditionally, these are handled manually, leading to delays, misrouting, and lost information.

**CampusOS** replaces this with an autonomous AI workforce that:

1. **Accepts** a high-level user request (natural language)
2. **Understands** the request via an Intake Agent
3. **Classifies** it into categories (Maintenance, IT, Finance, etc.)
4. **Prioritizes** it (Low → Critical)
5. **Researches** relevant knowledge base articles and historical data
6. **Routes** it to the appropriate department
7. **Analyzes** the issue and generates recommendations
8. **Verifies** the proposed action for safety and consistency
9. **Requests human approval** when the action is high-risk
10. **Executes** approved actions via defined tools
11. **Communicates** results to the requester and stakeholders
12. **Audits** every step for full traceability

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        SYSTEM ARCHITECTURE                        │
└──────────────────────────────────────────────────────────────────┘

                          ┌──────────────┐
                          │    GitHub     │
                          └──────┬───────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
          ┌─────────────────┐       ┌──────────────────┐
          │     Vercel      │       │      Render      │
          │  React Frontend │       │   Flask Backend   │
          │    (Vite SPA)   │       │   (Gunicorn)      │
          └────────┬────────┘       └────────┬─────────┘
                   │                         │
                   │  /api/* proxy via        │
                   │  Vercel Serverless       │
                   └─────────────────────────┘
                                           │
                                           ▼
                                 ┌──────────────────┐
                                 │    PostgreSQL     │
                                 │   (SQLAlchemy)    │
                                 └──────────────────┘
```

### Request Lifecycle

```
Browser ──POST /api/auth/login──▶ Vercel ──rewrite──▶ Serverless Proxy
                                                          │
                                                    BACKEND_URL
                                                          │
                                                          ▼
                                                   Flask Backend
                                                          │
                                                          ▼
                                                    PostgreSQL
```

---

## Technology Stack

| Layer             | Technology                            |
|-------------------|---------------------------------------|
| **Frontend**      | React 18, JavaScript, Vite            |
| **Styling**       | Custom CSS (CSS Variables)            |
| **Routing**       | React Router v6                       |
| **HTTP Client**   | Axios (with interceptors)             |
| **Charts**        | Recharts                              |
| **Icons**         | Lucide React                          |
| **Backend**       | Python 3.11, Flask 3.0                |
| **Database**      | PostgreSQL 15, SQLAlchemy 2.0         |
| **Migrations**    | Flask-Migrate (Alembic)               |
| **Auth**          | JWT (Flask-JWT-Extended), bcrypt      |
| **AI/Agents**     | LangGraph (custom pipeline)           |
| **ORM**           | Flask-SQLAlchemy                      |
| **CORS**          | Flask-CORS                            |
| **Production WS** | Gunicorn                              |
| **Deployment**    | Vercel (frontend) + Render (backend)  |
| **Container**     | Docker, docker-compose                |

---

## Features

### Authentication & Authorization
- JWT access + refresh tokens
- bcrypt password hashing
- Role-Based Access Control (RBAC): Student, Faculty, Staff, Department Manager, Admin
- Token refresh with automatic retry

### AI Agent Workforce
- **11 specialized agents** orchestrated via a LangGraph-inspired pipeline
- Deterministic + AI-assisted classification and prioritization
- Tool-based execution (no arbitrary database access by LLMs)
- Safety verification agent with human-in-the-loop gates
- Full audit trail for every agent action

### Request Management
- Create, view, filter, and track campus requests
- 10 request categories (Maintenance, IT, Finance, Hostel, etc.)
- 11 request statuses from NEW → COMPLETED
- Real-time workflow progress tracking

### Dashboard
- Role-aware dashboards (Student, Staff, Manager, Admin)
- Live metrics from the database (no hardcoded data)
- Charts for requests by category, priority, department, status

### Admin Panel
- User management (create, activate/deactivate, assign roles)
- Department management
- Workflow inspection and agent run history
- Approval queue for human-in-the-loop actions
- Knowledge base management (CRUD)
- Audit log viewer with filters
- Analytics dashboard

### Notifications
- In-app notification system
- Unread count badge
- Triggered by request lifecycle events

---

## Database Schema

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATABASE SCHEMA                                     │
└─────────────────────────────────────────────────────────────────────────────────┘

┌───────────┐       ┌───────────┐
│   roles    │       │departments│
├───────────┤       ├───────────┤
│ id (PK)   │       │ id (PK)   │
│ name      │       │ name      │
│description│       │description│
│permissions│ JSON  │ is_active │
│ created_at│       │ created_at│
└─────┬─────┘       │ updated_at│
      │              └─────┬─────┘
      │                    │
      │  ┌─────────────────┤
      │  │                 │
      ▼  ▼                 ▼
┌────────────────┐    ┌────────────────────┐
│     users      │    │knowledge_documents  │
├────────────────┤    ├────────────────────┤
│ id (PK)        │    │ id (PK)            │
│ name           │    │ title              │
│ email (UNIQUE) │    │ content            │
│ password_hash  │    │ category           │
│ phone          │    │ department_id (FK) │
│ role_id (FK)   │    │ meta_data (JSON)   │
│ department_id  │    │ created_at         │
│ is_active      │    │ updated_at         │
│ created_at     │    └────────────────────┘
│ updated_at     │
│ last_login     │
└───────┬────────┘
        │
        ├─── requests (as requester)
        ├─── requests (as assignee)
        ├─── notifications (as recipient)
        ├─── audit_logs (as actor)
        ├─── feedback (as submitter)
        └─── approvals (as requester / reviewer)

┌───────────────────┐        ┌────────────────────┐
│     requests      │        │     workflows      │
├───────────────────┤   1:1  ├────────────────────┤
│ id (PK)           │◄──────►│ id (PK)            │
│ request_number    │        │ request_id (FK, UQ) │
│ requester_id (FK) │        │ state              │
│ title             │        │ current_agent      │
│ description       │        │ status             │
│ category          │        │requires_human_appr │
│ priority          │        │ approval_status    │
│ status            │        │ created_at         │
│ department_id(FK) │        │ completed_at       │
│ assigned_to (FK)  │        └─────────┬──────────┘
│ created_at        │                  │
│ updated_at        │                  │ 1:N
│ resolved_at       │                  │
└───────┬───────────┘        ┌─────────┴──────────┐
        │                    │                    │
        │                    ▼                    ▼
        │         ┌─────────────────┐  ┌──────────────────┐
        │         │ workflow_tasks  │  │    agent_runs    │
        │         ├─────────────────┤  ├──────────────────┤
        │         │ id (PK)         │  │ id (PK)          │
        │         │ workflow_id(FK) │  │ workflow_id (FK) │
        │         │ agent_name      │  │ agent_name       │
        │         │ task_type       │  │ task_description │
        │         │ input_data(JSON)│  │ input_data (JSON)│
        │         │ output_data(JSN)│  │ output_data(JSON)│
        │         │ status          │  │ status           │
        │         │ started_at      │  │ duration_ms      │
        │         │ completed_at    │  │ error_message    │
        │         │ error_message   │  │ created_at       │
        │         └─────────────────┘  │ completed_at     │
        │                              └──────────────────┘
        │
        ├─── notifications (request_id)
        ├─── feedback (request_id)
        ├─── audit_logs (request_id)
        │
        └─── approvals (via workflow)

┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│ notifications│       │  audit_logs  │       │   feedback   │
├──────────────┤       ├──────────────┤       ├──────────────┤
│ id (PK)      │       │ id (PK)      │       │ id (PK)      │
│recipient(FK) │       │ user_id (FK) │       │request_id(FK)│
│request_id(FK)│       │request_id(FK)│       │workflow_id FK│
│ title        │       │workflow_idFK │       │submitted_byFK│
│ message      │       │ action       │       │ rating (1-5) │
│ type         │       │ actor_type   │       │ comment      │
│ is_read      │       │ old_value    │       │ correction   │
│ created_at   │       │ new_value    │       │ created_at   │
└──────────────┘       │ meta_data    │       └──────────────┘
                       │ created_at   │
                       └──────────────┘
```

### Key Relationships

| Relationship          | Type     | Description                              |
|-----------------------|----------|------------------------------------------|
| User → Role           | Many:1   | Every user has one role                  |
| User → Department     | Many:1   | Users belong to a department             |
| Request → User        | Many:1   | Requester and assignee                   |
| Request → Workflow    | 1:1      | Each request gets one workflow           |
| Workflow → Tasks      | 1:N      | Each workflow has multiple agent tasks   |
| Workflow → AgentRuns  | 1:N      | Execution history for each agent         |
| Workflow → Approvals  | 1:N      | Human approval requests                  |
| Request → Notifications| 1:N     | Notifications tied to requests           |
| Request → AuditLogs   | 1:N      | Complete audit trail                     |
| Request → Feedback    | 1:N      | User feedback on resolution              |
| Department → Knowledge| 1:N      | Knowledge base docs per department       |

---

## AI Agent Workflow

### Pipeline Overview

```
┌───────────────────────────────────────────────────────────────────┐
│                    AGENT PIPELINE FLOW                             │
└───────────────────────────────────────────────────────────────────┘

                            ┌───────┐
                            │ START │
                            └───┬───┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │   1. INTAKE AGENT   │
                     │  Extract & normalize│
                     │  request data       │
                     └─────────┬───────────┘
                               │
                               ▼
                  ┌────────────────────────┐
                  │ 2. CLASSIFICATION AGENT│
                  │  Categorize into:      │
                  │  Maintenance, IT,      │
                  │  Finance, Hostel...    │
                  └────────────┬───────────┘
                               │
                               ▼
                   ┌──────────────────────┐
                   │  3. PRIORITY AGENT   │
                   │  LOW / MEDIUM / HIGH │
                   │  / CRITICAL          │
                   └──────────┬───────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ 4. RESEARCH AGENT │
                    │  Search knowledge │
                    │  base + related   │
                    │  requests         │
                    └────────┬──────────┘
                             │
                             ▼
                    ┌───────────────────┐
                    │  5. ROUTING AGENT │
                    │  Assign to dept   │
                    │  + assignee       │
                    └────────┬──────────┘
                             │
                             ▼
                   ┌────────────────────┐
                   │ 6. ANALYSIS AGENT  │
                   │  Generate action   │
                   │  recommendations   │
                   └────────┬───────────┘
                            │
                            ▼
                  ┌──────────────────────┐
                  │7. VERIFICATION AGENT │
                  │  Safety check on     │
                  │  proposed actions    │
                  └──────┬──────┬────────┘
                         │      │
                    ┌────┘      └────┐
                    ▼                ▼
           ┌─────────────┐  ┌────────────────┐
           │   PASS ✓    │  │  FAIL / RISK   │
           └──────┬──────┘  │  ⚠ Human       │
                  │         │  Approval Gate  │
                  │         └────────┬───────┘
                  │                  │
                  │         ┌────────▼────────┐
                  │         │  ADMIN REVIEWS  │
                  │         │  Approve/Reject │
                  │         └────────┬────────┘
                  │                  │
                  ▼                  ▼
           ┌─────────────────────────────┐
           │      8. ACTION AGENT        │
           │  Execute via defined tools  │
           │  (create ticket, update     │
           │   request, assign, notify)  │
           └──────────────┬──────────────┘
                          │
                          ▼
           ┌─────────────────────────────┐
           │   9. COMMUNICATION AGENT    │
           │  Generate user-facing       │
           │  messages & notifications   │
           └──────────────┬──────────────┘
                          │
                          ▼
                 ┌────────────────┐
                 │ AUDIT LOGGING  │
                 │ Record all     │
                 │ actions taken  │
                 └───────┬────────┘
                         │
                         ▼
                   ┌──────────┐
                   │ COMPLETED│
                   └──────────┘
```

### Agent Details

| # | Agent               | Purpose                                          | Tools Used                             |
|---|---------------------|--------------------------------------------------|----------------------------------------|
| 1 | **Intake**          | Extract & normalize incoming request              | —                                      |
| 2 | **Classification**  | Categorize into one of 10 request types           | —                                      |
| 3 | **Priority**        | Assign urgency level (deterministic + AI)         | —                                      |
| 4 | **Research**        | Retrieve relevant KB articles & past requests     | `search_knowledge`, `get_related_requests` |
| 5 | **Routing**         | Assign to department and potential assignee        | `get_department`, `get_user`           |
| 6 | **Analysis**        | Generate structured action recommendations        | `get_request`, `get_department`        |
| 7 | **Verification**    | Safety check — approve, reject, or escalate       | —                                      |
| 8 | **Action**          | Execute approved actions through tools            | `create_ticket`, `update_request`, `assign_request`, `create_notification` |
| 9 | **Communication**   | Generate messages for users, staff, admins        | `create_notification`                  |

### Safety Model

```
┌────────────────────────────────────────────────────┐
│                  SAFETY LAYERS                      │
├────────────────────────────────────────────────────┤
│                                                    │
│  1. TOOL RESTRICTION                               │
│     Agents call explicit tools only.               │
│     No free-form SQL or OS commands.               │
│                                                    │
│  2. VERIFICATION AGENT                             │
│     Checks classification, routing, proposed        │
│     actions for consistency and safety.            │
│                                                    │
│  3. HUMAN-IN-THE-LOOP GATE                         │
│     High-risk actions pause for admin review.      │
│     Admin sees: request, AI reasoning, proposed    │
│     action, risk level, and audit context.         │
│                                                    │
│  4. AUDIT LOGGING                                  │
│     Every agent execution, tool call, and state    │
│     change is recorded with timestamps.            │
│                                                    │
│  5. RETRY LIMITS                                   │
│     Failed agents have bounded retry counts.       │
│     Failures propagate to workflow status.         │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## Getting Started

### Prerequisites

- **Python** 3.11+
- **Node.js** 18+
- **PostgreSQL** 14+
- **Docker** & Docker Compose (recommended)

### Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/CampusOS-Platform.git
cd CampusOS-Platform

# Copy environment template
cp .env.example .env

# Start all services (PostgreSQL + Backend + Frontend)
docker-compose up -d

# The app is now running at:
#   Frontend: http://localhost:5173
#   Backend:  http://localhost:5000
#   Database: localhost:5432
```

### Manual Setup

#### 1. Database

```bash
# Using Docker just for PostgreSQL
docker run -d --name campusos-db \
  -e POSTGRES_USER=campusos \
  -e POSTGRES_PASSWORD=campusos \
  -e POSTGRES_DB=campusos \
  -p 5432:5432 \
  postgres:15-alpine

# Or using an existing PostgreSQL instance
createdb campusos
```

#### 2. Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (or use .env file)
export DATABASE_URL=postgresql://campusos:campusos@localhost:5432/campusos
export JWT_SECRET_KEY=your-jwt-secret
export SECRET_KEY=your-flask-secret
export FLASK_ENV=development

# Initialize migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Seed the database
python seed.py

# Start the backend
python run.py
# Backend runs at http://localhost:5000
```

#### 3. Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
# Frontend runs at http://localhost:5173
```

The Vite dev server automatically proxies `/api` requests to `http://localhost:5000`.

---

## Environment Variables

### Backend (Flask)

| Variable                    | Required | Default                  | Description                              |
|-----------------------------|----------|--------------------------|------------------------------------------|
| `DATABASE_URL`              | ✅       | `postgresql://campusos:campusos@localhost:5432/campusos` | PostgreSQL connection string |
| `SECRET_KEY`                | ✅       | `dev-secret-key`         | Flask secret key for sessions            |
| `JWT_SECRET_KEY`            | ✅       | `jwt-dev-secret`         | Secret key for signing JWT tokens        |
| `JWT_ACCESS_TOKEN_EXPIRES`  | ❌       | `3600`                   | Access token TTL in seconds              |
| `JWT_REFRESH_TOKEN_EXPIRES` | ❌       | `2592000` (30 days)     | Refresh token TTL in seconds             |
| `FLASK_ENV`                 | ❌       | `development`            | `development` or `production`            |
| `CORS_ORIGINS`              | ❌       | `*`                      | Comma-separated allowed origins          |
| `FRONTEND_URL`              | ❌       | `http://localhost:5173`  | Frontend URL for CORS / reference        |
| `LLM_API_KEY`               | ❌       | —                        | OpenAI API key (blank = demo mode)       |
| `LLM_MODEL`                 | ❌       | `gpt-3.5-turbo`          | LLM model name                          |
| `LLM_BASE_URL`              | ❌       | —                        | Custom LLM base URL (for proxies)        |

### Frontend (Vercel)

| Variable       | Required | Description                                    |
|----------------|----------|------------------------------------------------|
| `BACKEND_URL`  | ✅       | Full URL of the deployed backend (e.g. `https://campusos-backend.onrender.com`) |

---

## API Documentation

### Base URL

```
Production:  https://campusos-backend.onrender.com
Local:       http://localhost:5000
```

### Response Format

All endpoints follow a consistent response format:

**Success:**
```json
{
  "success": true,
  "data": { ... },
  "message": "Description of what happened"
}
```

**Error:**
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {}
  }
}
```

### Authentication Endpoints

| Method | Endpoint                    | Auth | Description                    |
|--------|-----------------------------|------|--------------------------------|
| POST   | `/api/auth/register`        | No   | Register new user              |
| POST   | `/api/auth/login`           | No   | Login and get JWT tokens       |
| POST   | `/api/auth/refresh`         | Refresh | Refresh access token       |
| GET    | `/api/auth/me`              | Yes  | Get current user profile       |
| POST   | `/api/auth/change-password` | Yes  | Change password                |

**Login Request:**
```json
POST /api/auth/login
{
  "email": "student@campusos.local",
  "password": "Student123!"
}
```

**Login Response:**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "user": {
      "id": 1,
      "name": "Student User",
      "email": "student@campusos.local",
      "role": { "name": "STUDENT", "permissions": [...] },
      "department": { "name": "Academics" }
    }
  }
}
```

### Request Endpoints

| Method | Endpoint                        | Auth | Description              |
|--------|---------------------------------|------|--------------------------|
| POST   | `/api/requests`                 | Yes  | Create a new request     |
| GET    | `/api/requests`                 | Yes  | List requests (filtered) |
| GET    | `/api/requests/:id`             | Yes  | Get request details      |
| PATCH  | `/api/requests/:id`             | Yes  | Update request           |
| DELETE | `/api/requests/:id`             | Yes  | Cancel request           |
| POST   | `/api/requests/:id/process`     | Yes  | Process through AI       |

### Workflow Endpoints

| Method | Endpoint                | Auth | Description              |
|--------|-------------------------|------|--------------------------|
| GET    | `/api/workflows`        | Yes  | List all workflows       |
| GET    | `/api/workflows/:id`    | Yes  | Get workflow details     |

### Approval Endpoints

| Method | Endpoint                          | Auth | Description          |
|--------|-----------------------------------|------|----------------------|
| GET    | `/api/approvals`                  | Yes  | List pending approvals|
| POST   | `/api/approvals/:id/approve`      | Yes  | Approve action        |
| POST   | `/api/approvals/:id/reject`       | Yes  | Reject action         |

### Dashboard Endpoints

| Method | Endpoint                   | Auth | Description               |
|--------|----------------------------|------|---------------------------|
| GET    | `/api/dashboard/student`   | Yes  | Student dashboard data    |
| GET    | `/api/dashboard/admin`     | Yes  | Admin dashboard data      |

### Admin Endpoints

| Method | Endpoint                    | Auth   | Description              |
|--------|-----------------------------|--------|--------------------------|
| GET    | `/api/users`                | Admin  | List all users           |
| POST   | `/api/users`                | Admin  | Create user              |
| GET    | `/api/admin/roles`          | Admin  | List roles               |
| GET    | `/api/departments`          | Admin  | List departments         |
| POST   | `/api/departments`          | Admin  | Create department        |
| GET    | `/api/knowledge`            | Admin  | List knowledge docs      |
| GET    | `/api/audit-logs`           | Admin  | List audit logs          |

### Notification Endpoints

| Method | Endpoint                          | Auth | Description           |
|--------|-----------------------------------|------|-----------------------|
| GET    | `/api/notifications`              | Yes  | List notifications    |
| PATCH  | `/api/notifications/:id/read`     | Yes  | Mark as read          |

### Agent Endpoints

| Method | Endpoint                | Auth | Description            |
|--------|-------------------------|------|------------------------|
| GET    | `/api/agents`           | Yes  | List agents            |
| GET    | `/api/agents/status`    | Yes  | Get agent statuses     |
| GET    | `/api/agents/runs`      | Yes  | List agent runs        |
| GET    | `/api/agents/runs/:id`  | Yes  | Get agent run details  |

### Health Check

| Method | Endpoint       | Auth | Description    |
|--------|----------------|------|----------------|
| GET    | `/api/health`  | No   | Backend health  |

**Response:**
```json
{
  "status": "ok",
  "database": "connected",
  "message": "CampusOS API is running"
}
```

---

## Frontend Pages

### Public Pages

| Path        | Component  | Description                   |
|-------------|------------|-------------------------------|
| `/login`    | `Login`    | Sign in form with email/password |
| `/register` | `Register` | Create new account            |

### Authenticated Pages

| Path                | Component         | Access        | Description                      |
|---------------------|-------------------|---------------|----------------------------------|
| `/dashboard`        | `Dashboard`       | All           | Role-aware dashboard with metrics |
| `/create-request`   | `CreateRequest`   | All           | Submit a new campus request      |
| `/my-requests`      | `MyRequests`      | All           | View and filter own requests     |
| `/requests/:id`     | `RequestDetail`   | All           | Full request view with workflow  |
| `/notifications`    | `Notifications`   | All           | Notification center              |
| `/profile`          | `Profile`         | All           | User profile and settings        |

### Admin/Manager Pages

| Path                   | Component           | Access               | Description                |
|------------------------|---------------------|----------------------|----------------------------|
| `/admin/users`         | `AdminUsers`        | Admin, Manager       | User management            |
| `/admin/departments`   | `AdminDepartments`  | Admin, Manager       | Department management      |
| `/admin/workflows`     | `AdminWorkflows`    | Admin, Manager       | Workflow inspection        |
| `/admin/approvals`     | `AdminApprovals`    | Admin, Manager       | Approval queue             |
| `/admin/knowledge`     | `AdminKnowledge`    | Admin                | Knowledge base CRUD        |
| `/admin/audit`         | `AdminAudit`        | Admin                | Audit log viewer           |
| `/admin/analytics`     | `AdminAnalytics`    | Admin                | Analytics dashboard        |

---

## Deployment

### Backend on Render

1. Go to [Render](https://dashboard.render.com) → **New Web Service**
2. Connect your GitHub repository
3. Configure:
   - **Root Directory:** `backend`
   - **Runtime:** Python 3.11
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn wsgi:app --bind 0.0.0.0:$PORT`
4. Add environment variables (see [Environment Variables](#environment-variables))
5. Deploy and note the Render URL

**Initialize the database:**
```bash
# Via Render Shell
cd backend
python seed.py
```

**Verify:**
```bash
curl https://campusos-backend.onrender.com/api/health
# → {"status": "ok", "database": "connected", "message": "CampusOS API is running"}
```

### Frontend on Vercel

1. Go to [Vercel](https://vercel.com) → **Import Project**
2. Connect your GitHub repository
3. Configure:
   - **Framework:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
4. Add environment variable: `BACKEND_URL` = your Render backend URL
5. Deploy

---

## Testing

```bash
cd backend

# Install test dependencies
pip install pytest

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --tb=short
```

### Test Coverage

| Area              | What's Tested                                          |
|-------------------|--------------------------------------------------------|
| Authentication    | Register, login, invalid credentials, token validation |
| Authorization     | Role restrictions, protected routes                    |
| Requests          | CRUD operations, validation, filtering                 |
| Workflows         | Pipeline execution, approval flow, failure handling    |
| Agents            | Individual agent execution, structured outputs         |
| Database          | Model relationships, constraints                       |

---

## Demo Credentials

| Role                | Email                       | Password     |
|---------------------|-----------------------------|--------------|
| 🔑 Admin           | `admin@campusos.local`      | `Admin123!`  |
| 👔 Manager         | `manager@campusos.local`    | `Manager123!`|
| 🛠️ Staff           | `staff@campusos.local`      | `Staff123!`  |
| 🎓 Student         | `student@campusos.local`    | `Student123!`|
| 📚 Faculty         | `faculty@campusos.local`    | `Faculty123!`|

> ⚠️ **These credentials are for local development and demo only.**

---

## Project Structure

```
CampusOS-Platform/
├── backend/
│   ├── app/
│   │   ├── __init__.py              # Flask app factory
│   │   ├── config.py                # Configuration classes
│   │   ├── extensions.py            # SQLAlchemy, Migrate, JWT
│   │   │
│   │   ├── models/                  # SQLAlchemy ORM models
│   │   │   ├── user.py              #   User (auth, profile)
│   │   │   ├── role.py              #   Role (RBAC)
│   │   │   ├── department.py        #   Department
│   │   │   ├── request.py           #   Campus request
│   │   │   ├── workflow.py          #   AI workflow state
│   │   │   ├── workflow_task.py     #   Individual agent tasks
│   │   │   ├── agent_run.py         #   Agent execution history
│   │   │   ├── approval.py          #   Human approval requests
│   │   │   ├── notification.py      #   In-app notifications
│   │   │   ├── audit_log.py         #   Audit trail
│   │   │   ├── feedback.py          #   User feedback
│   │   │   └── knowledge_document.py#   Knowledge base
│   │   │
│   │   ├── routes/                  # Flask blueprints (API)
│   │   │   ├── auth.py              #   Authentication endpoints
│   │   │   ├── users.py             #   User management
│   │   │   ├── requests.py          #   Request CRUD + processing
│   │   │   ├── workflows.py         #   Workflow inspection
│   │   │   ├── agents.py            #   Agent status & runs
│   │   │   ├── approvals.py         #   Approval queue
│   │   │   ├── departments.py       #   Department management
│   │   │   ├── notifications.py     #   Notifications
│   │   │   ├── dashboard.py         #   Dashboard metrics
│   │   │   ├── audit.py             #   Audit log viewer
│   │   │   ├── knowledge.py         #   Knowledge base CRUD
│   │   │   ├── feedback.py          #   Feedback endpoints
│   │   │   └── admin.py             #   Admin-only operations
│   │   │
│   │   ├── services/                # Business logic layer
│   │   │   ├── auth_service.py      #   Registration, login, tokens
│   │   │   ├── request_service.py   #   Request operations
│   │   │   ├── workflow_service.py  #   Workflow management
│   │   │   ├── agent_service.py     #   Agent orchestration
│   │   │   ├── approval_service.py  #   Approval logic
│   │   │   ├── notification_service.py # Notification delivery
│   │   │   ├── audit_service.py     #   Audit logging
│   │   │   ├── knowledge_service.py #   Knowledge base search
│   │   │   └── dashboard_service.py #   Dashboard aggregation
│   │   │
│   │   ├── agents/                  # AI agent pipeline
│   │   │   ├── state.py             #   Shared WorkflowState (TypedDict)
│   │   │   ├── graph.py             #   Pipeline definition & navigation
│   │   │   ├── workforce_manager.py #   Pipeline orchestrator
│   │   │   ├── intake_agent.py      #   Request normalization
│   │   │   ├── classification_agent.py # Category classification
│   │   │   ├── priority_agent.py    #   Urgency determination
│   │   │   ├── research_agent.py    #   Knowledge retrieval
│   │   │   ├── routing_agent.py     #   Department assignment
│   │   │   ├── analysis_agent.py    #   Action recommendations
│   │   │   ├── verification_agent.py#   Safety verification
│   │   │   ├── action_agent.py      #   Execute approved actions
│   │   │   └── communication_agent.py # Message generation
│   │   │
│   │   ├── tools/                   # Agent tool functions
│   │   │   ├── database_tools.py    #   Query helpers
│   │   │   ├── ticket_tools.py      #   Ticket operations
│   │   │   ├── department_tools.py  #   Department lookups
│   │   │   ├── notification_tools.py#   Notification creation
│   │   │   ├── knowledge_tools.py   #   KB search
│   │   │   └── audit_tools.py       #   Audit logging
│   │   │
│   │   ├── schemas/                 # Input validation
│   │   │   ├── auth.py              #   Auth validation rules
│   │   │   └── requests.py          #   Request validation rules
│   │   │
│   │   └── utils/                   # Shared utilities
│   │       ├── decorators.py        #   @require_role, etc.
│   │       ├── errors.py            #   Error handlers
│   │       ├── validators.py        #   Email, password validation
│   │       ├── security.py          #   Password hashing
│   │       └── logger.py            #   Logging setup
│   │
│   ├── tests/                       # Backend tests
│   ├── migrations/                  # Alembic migrations
│   ├── seed.py                      # Database seeder
│   ├── run.py                       # Dev server entry
│   ├── wsgi.py                      # Production WSGI
│   ├── render.yaml                  # Render deployment config
│   ├── Dockerfile                   # Backend container
│   ├── requirements.txt             # Python dependencies
│   └── start.sh                     # Container startup script
│
├── frontend/
│   ├── api/
│   │   └── [[proxy]].js             # Vercel serverless API proxy
│   ├── src/
│   │   ├── pages/                   # React page components
│   │   │   ├── Login.jsx            #   Sign in
│   │   │   ├── Register.jsx         #   Sign up
│   │   │   ├── Dashboard.jsx        #   Main dashboard
│   │   │   ├── CreateRequest.jsx    #   New request form
│   │   │   ├── MyRequests.jsx       #   Request list
│   │   │   ├── RequestDetail.jsx    #   Request + workflow view
│   │   │   ├── Notifications.jsx    #   Notification center
│   │   │   ├── Profile.jsx          #   User profile
│   │   │   ├── AdminUsers.jsx       #   User management
│   │   │   ├── AdminDepartments.jsx #   Department management
│   │   │   ├── AdminWorkflows.jsx   #   Workflow inspector
│   │   │   ├── AdminApprovals.jsx   #   Approval queue
│   │   │   ├── AdminKnowledge.jsx   #   Knowledge base
│   │   │   ├── AdminAudit.jsx       #   Audit log viewer
│   │   │   └── AdminAnalytics.jsx   #   Analytics charts
│   │   │
│   │   ├── layouts/
│   │   │   └── Layout.jsx           #   App shell (sidebar + topbar)
│   │   │
│   │   ├── context/
│   │   │   └── AuthContext.jsx       #   Auth state provider
│   │   │
│   │   ├── services/
│   │   │   └── api.js               #   Axios instance + interceptors
│   │   │
│   │   ├── App.jsx                  #   Route definitions
│   │   └── main.jsx                 #   Entry point
│   │
│   ├── vercel.json                  # Vercel deployment config
│   ├── Dockerfile                   # Frontend container
│   └── package.json                 # Node dependencies
│
├── docker-compose.yml               # Full stack orchestration
├── .env.example                     # Environment template
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

---

## Troubleshooting

### "Unable to connect to server" on login

1. **Check `BACKEND_URL`** in Vercel environment variables
2. **Verify backend is running:** `curl https://your-backend.onrender.com/api/health`
3. **Check Render logs** for crashes or database connection errors
4. **Ensure CORS** is configured: `CORS_ORIGINS` must include your Vercel URL

### Backend returns 500 errors

1. **Database connection:** Ensure `DATABASE_URL` is correct and the database exists
2. **Run migrations:** `flask db upgrade`
3. **Seed data:** `python seed.py`

### Frontend shows blank page

1. **Check browser console** for JavaScript errors
2. **Verify build:** `npm run build` should complete without errors
3. **Check Vercel deployment logs** for build failures

### API proxy not working

1. Ensure `BACKEND_URL` is set in Vercel environment variables
2. The proxy in `api/[[proxy]].js` extracts the request path and forwards to `BACKEND_URL`
3. Check Vercel function logs for proxy errors

### Docker issues

```bash
# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Check logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

---

## Future Improvements

- [ ] **Email notifications** for request status changes
- [ ] **File upload support** for attaching images/documents
- [ ] **WebSocket real-time updates** for live workflow progress
- [ ] **Vector database integration** for semantic knowledge base search
- [ ] **Rate limiting** on API endpoints
- [ ] **OpenAPI/Swagger documentation** auto-generation
- [ ] **Mobile-responsive** navigation improvements
- [ ] **Multi-language support** (i18n)
- [ ] **SSO integration** (Google, Microsoft)
- [ ] **Advanced analytics** with exportable reports

---

## License

Built for hackathon use. CampusOS — Making campus operations smarter with autonomous AI.
