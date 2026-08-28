You are the lead software architect, senior full-stack engineer, AI engineer, database engineer, security engineer, UI/UX engineer, and QA engineer for this project.

Your task is to BUILD THE ENTIRE CAMPUSOS PROJECT as a fully working, production-style hackathon application.

DO NOT merely generate a prototype, UI mockup, pseudo-code, placeholder architecture, or incomplete scaffold.

IMPLEMENT THE ACTUAL APPLICATION.

You must create the complete source code, database models, APIs, frontend, authentication, authorization, AI agent workflow, audit logging, human approval workflow, validation, error handling, tests, seed data, documentation, and local development setup.

The final application must be runnable locally from a clean machine using the provided setup instructions.

==================================================
PROJECT
==================================================

Project Name:
CampusOS

Tagline:
An Autonomous AI Workforce for Smarter Campus Operations

Hackathon Theme:
Build the Next Generation Autonomous AI Workforce

Core Concept:

CampusOS is an autonomous multi-agent AI workforce for university/campus operations.

It must NOT behave like a simple chatbot.

The system must be able to:

1. Accept a high-level user request.
2. Understand the request.
3. Classify the request.
4. Determine priority.
5. Retrieve relevant campus information.
6. Plan the workflow.
7. Route work to the appropriate department.
8. Delegate tasks to specialized AI agents.
9. Use tools and database information.
10. Verify outputs.
11. Ask for human approval when required.
12. Execute approved/routine actions.
13. Generate a response/report.
14. Notify relevant users.
15. Store complete audit logs.
16. Store feedback and corrections.
17. Maintain workflow state.
18. Track the request from creation to resolution.

Example:

"The water cooler near Block B has not worked for 3 days."

CampusOS should be able to determine:

Issue:
Broken Water Cooler

Priority:
High

Department:
Facilities / Maintenance

Action:
Create maintenance ticket

Then:

1. create the maintenance workflow
2. verify the generated decision
3. determine whether human approval is required
4. execute the action if allowed
5. notify the requester
6. store the entire workflow in the audit trail

==================================================
IMPORTANT ENGINEERING RULE
==================================================

DO NOT FAKE FUNCTIONALITY.

If a feature is displayed in the UI, the backend must support it.

If an API endpoint is displayed, implement it.

If an agent is displayed, implement it.

If a database entity is displayed, create the database model.

If an action claims to be executed, create the corresponding service/function and database update.

Do not create buttons that do nothing.

Do not create fake dashboards with hard-coded values.

Do not use static JSON pretending to be a backend.

Demo data is allowed ONLY through database seed scripts.

==================================================
TECHNOLOGY STACK
==================================================

MANDATORY STACK:

Frontend:
- React
- JavaScript
- HTML5
- CSS3

Backend:
- Python
- Flask

API:
- REST API
- JSON
- HTTP

Database:
- PostgreSQL

ORM:
- SQLAlchemy

AI / Agent Framework:
- LangGraph
- LLM API

Authentication:
- JWT

Authorization:
- Role-Based Access Control

Version Control:
- Git
- GitHub compatible repository structure

Configuration:
- Environment variables
- .env
- .env.example

DO NOT replace Flask with FastAPI, Django, Node.js, or another backend framework.

DO NOT replace SQLAlchemy with another ORM.

DO NOT replace PostgreSQL with MongoDB or another database as the primary database.

==================================================
HIGH-LEVEL ARCHITECTURE
==================================================

Implement this architecture:

React Frontend
       |
       v
REST API
       |
       v
Flask Backend
       |
       v
Authentication / Authorization
       |
       v
CampusOS Service Layer
       |
       v
AI Workforce Manager
       |
       v
LangGraph Agent Orchestration
       |
       +----------------------+
       |          |           |
       v          v           v
Research     Analysis      Action
 Agent        Agent        Agent
       \          |           /
        \         |          /
         +--------+---------+
                  |
                  v
          Verification Agent
                  |
                  v
          Human Approval Gate
             /          \
            /            \
           v              v
   Human Review      Autonomous Execute
           \              /
            \            /
             +----------+
                  |
                  v
       SQLAlchemy ORM Layer
                  |
                  v
             PostgreSQL
                  |
                  v
         Audit / Workflow Logs
                  |
                  v
          Response / Report
                  |
                  v
             React UI

==================================================
APPLICATION MODULES
==================================================

Organize the project cleanly.

Recommended backend structure:

backend/
    app/
        __init__.py
        config.py

        extensions.py

        models/
            user.py
            role.py
            department.py
            request.py
            workflow.py
            workflow_task.py
            agent_run.py
            approval.py
            notification.py
            audit_log.py
            feedback.py
            knowledge_document.py

        routes/
            auth.py
            users.py
            requests.py
            workflows.py
            agents.py
            approvals.py
            departments.py
            notifications.py
            dashboard.py
            audit.py
            knowledge.py
            feedback.py
            admin.py

        services/
            auth_service.py
            request_service.py
            workflow_service.py
            agent_service.py
            approval_service.py
            notification_service.py
            audit_service.py
            knowledge_service.py
            dashboard_service.py

        agents/
            state.py
            graph.py
            workforce_manager.py

            intake_agent.py
            classification_agent.py
            priority_agent.py
            research_agent.py
            routing_agent.py
            analysis_agent.py
            action_agent.py
            verification_agent.py
            communication_agent.py
            analytics_agent.py
            feedback_agent.py

        tools/
            database_tools.py
            ticket_tools.py
            department_tools.py
            notification_tools.py
            knowledge_tools.py
            audit_tools.py

        schemas/
            auth.py
            users.py
            requests.py
            workflows.py
            approvals.py
            agents.py

        utils/
            decorators.py
            security.py
            validators.py
            errors.py
            logger.py

        migrations/

    tests/

    seed.py
    run.py
    requirements.txt

frontend/
    src/
        components/
        pages/
        layouts/
        services/
        hooks/
        context/
        utils/
        routes/
        assets/
        App.jsx
        main.jsx

    package.json

docker-compose.yml
.env.example
README.md

You may improve this structure when necessary, but keep clear separation between:

- routes
- models
- services
- agent logic
- tools
- schemas
- utilities

==================================================
DATABASE
==================================================

Use PostgreSQL with SQLAlchemy.

Create proper relational models.

At minimum implement:

USER

Fields:
- id
- name
- email
- password_hash
- role_id
- department_id
- is_active
- created_at
- updated_at
- last_login

ROLE

Examples:
- STUDENT
- FACULTY
- STAFF
- ADMIN
- DEPARTMENT_MANAGER

DEPARTMENT

Examples:
- Hostel
- Facilities
- Maintenance
- Academics
- Finance
- Administration
- IT Support

REQUEST

Fields:
- id
- requester_id
- title
- description
- category
- priority
- status
- department_id
- assigned_to
- created_at
- updated_at
- resolved_at

WORKFLOW

Fields:
- id
- request_id
- state
- current_agent
- status
- requires_human_approval
- created_at
- completed_at

WORKFLOW_TASK

Fields:
- id
- workflow_id
- agent_name
- task_type
- input_data
- output_data
- status
- started_at
- completed_at
- error_message

AGENT_RUN

Store:
- agent
- input
- output
- execution status
- duration
- errors
- timestamp

APPROVAL

Fields:
- id
- workflow_id
- requested_by
- reviewed_by
- status
- reason
- reviewer_comment
- created_at
- reviewed_at

NOTIFICATION

Store:
- recipient
- message
- type
- read/unread
- timestamp

AUDIT_LOG

Store:
- user
- request
- workflow
- action
- actor_type
- old_value
- new_value
- metadata
- timestamp

FEEDBACK

Store:
- request
- workflow
- submitted_by
- rating
- comment
- correction
- timestamp

KNOWLEDGE_DOCUMENT

Store:
- title
- content
- category
- department
- metadata
- created_at
- updated_at

Implement proper relationships, foreign keys, indexes, timestamps, constraints and cascading behavior where appropriate.

Use SQLAlchemy migrations.

DO NOT use raw SQL everywhere.

==================================================
AUTHENTICATION
==================================================

Implement secure JWT authentication.

Required features:

- Register
- Login
- Logout/token invalidation strategy
- Access token
- Refresh token
- Password hashing
- Password validation
- Token expiration
- Protected routes
- Current-user endpoint
- Password change
- Account activation/deactivation

Never store plain-text passwords.

Use a secure password hashing algorithm.

JWT should contain:
- user id
- role
- issued time
- expiration
- appropriate security claims

Implement authentication middleware/decorators.

==================================================
AUTHORIZATION
==================================================

Implement proper Role-Based Access Control.

Roles:

1. STUDENT
2. FACULTY
3. STAFF
4. DEPARTMENT_MANAGER
5. ADMIN

Permissions must be enforced BOTH:

1. in backend APIs
2. in frontend route/UI visibility

Examples:

STUDENT:
- create request
- view own requests
- view request status
- receive notifications
- provide feedback

FACULTY:
- create requests
- view requests allowed to faculty
- provide feedback

STAFF:
- view assigned workflows
- update assigned operational tasks
- add comments
- resolve permitted requests

DEPARTMENT_MANAGER:
- review department requests
- assign staff
- approve department actions
- access department analytics

ADMIN:
- manage users
- manage departments
- manage roles
- manage system configurations
- view all requests
- view all audit logs
- manage knowledge base
- approve sensitive workflows
- access analytics

Never trust frontend authorization alone.

The backend must reject unauthorized actions with proper HTTP status codes.

==================================================
SECURITY
==================================================

Implement:

- Password hashing
- JWT authentication
- RBAC
- Input validation
- SQL injection protection through SQLAlchemy
- CORS configuration
- Secure error responses
- Request validation
- Rate limiting if practical
- Environment-variable secrets
- No secrets committed to Git
- .env.example
- Secure logging
- Audit logging
- Proper HTTP status codes

Never expose:
- password hashes
- JWT secrets
- API keys
- internal stack traces
- sensitive database information

==================================================
AI WORKFORCE
==================================================

Use LangGraph to orchestrate the AI workflow.

Create a shared workflow state.

The workflow state should contain information such as:

- request_id
- user_id
- raw_request
- category
- priority
- department
- relevant_context
- analysis
- proposed_action
- verification_result
- approval_required
- approval_status
- execution_result
- notification_result
- final_response
- audit_information
- errors
- retry_count

==================================================
AGENTS
==================================================

Implement the following agents.

------------------------------------------
1. INTAKE AGENT
------------------------------------------

Responsibilities:

- read the incoming request
- extract useful information
- normalize the request
- identify entities
- create structured input for downstream agents

------------------------------------------
2. CLASSIFICATION AGENT
------------------------------------------

Classify requests into categories such as:

- Hostel
- Maintenance
- Facilities
- Academics
- Finance
- Administration
- IT
- Lost and Found
- Student Grievance
- Other

Return structured JSON.

------------------------------------------
3. PRIORITY AGENT
------------------------------------------

Determine:

- LOW
- MEDIUM
- HIGH
- CRITICAL

Use clear rules.

Do NOT allow an LLM to arbitrarily invent priority without constraints.

Use deterministic rules combined with AI reasoning where useful.

------------------------------------------
4. RESEARCH AGENT
------------------------------------------

Retrieve relevant information from:

- campus knowledge base
- database
- department information
- previous related requests

Create reusable tools for retrieval.

------------------------------------------
5. ROUTING AGENT
------------------------------------------

Determine:

- department
- responsible role
- potential assignee
- routing reason

Use database information.

------------------------------------------
6. ANALYSIS AGENT
------------------------------------------

Analyze:

- issue
- context
- urgency
- required actions
- dependencies

Generate structured recommendations.

------------------------------------------
7. ACTION AGENT
------------------------------------------

Perform allowed actions through tools.

Examples:

- create maintenance ticket
- create internal task
- update request
- assign request
- create notification
- change status
- create workflow task

NEVER allow arbitrary destructive actions from an LLM.

All actions must go through explicitly defined tools.

------------------------------------------
8. VERIFICATION AGENT
------------------------------------------

This is a critical safety layer.

Verify:

- classification
- priority
- routing
- proposed action
- data consistency
- required fields
- authorization
- action safety

Return:

approved / rejected / needs_human_review

Explain why.

------------------------------------------
9. COMMUNICATION AGENT
------------------------------------------

Generate:

- user acknowledgement
- status update
- staff message
- admin summary
- final response

Keep messages clear and professional.

------------------------------------------
10. ANALYTICS AGENT
------------------------------------------

Analyze historical workflow information.

Provide:

- request trends
- department workload
- resolution status
- common categories
- priority distribution

------------------------------------------
11. FEEDBACK AGENT
------------------------------------------

Process:

- user feedback
- admin corrections
- approval/rejection outcomes
- workflow mistakes

Store corrections in the database.

Use them as future context where appropriate.

==================================================
LANGGRAPH WORKFLOW
==================================================

Build an actual LangGraph graph.

Suggested workflow:

START
  |
  v
INTAKE
  |
  v
CLASSIFICATION
  |
  v
PRIORITY
  |
  v
RESEARCH
  |
  v
ROUTING
  |
  v
ANALYSIS
  |
  v
ACTION PLAN
  |
  v
VERIFICATION
  |
  v
HUMAN APPROVAL CHECK
     /       \
    /         \
   YES         NO
   |            |
   v            v
HUMAN REVIEW   AUTONOMOUS EXECUTION
   |            |
   +------->----+
            |
            v
       COMMUNICATION
            |
            v
        AUDIT LOGGING
            |
            v
          RESPONSE
            |
            v
          FEEDBACK
            |
           END

Implement conditional graph transitions.

The graph must support:

- successful completion
- rejection
- retries
- failures
- human approval pauses
- resume after approval
- execution errors
- fallback paths

==================================================
HUMAN-IN-THE-LOOP
==================================================

Sensitive actions MUST NOT always execute automatically.

Create an approval mechanism.

Examples that require approval:

- high-impact financial changes
- privileged account changes
- potentially destructive database/system operations
- actions exceeding configurable thresholds
- administrative decisions

The workflow should pause when approval is needed.

Admin/authorized reviewer should see:

- request
- AI reasoning
- proposed action
- verification result
- risk level
- relevant context
- agent history

Reviewer options:

- Approve
- Reject
- Request modification

After approval, resume the workflow.

==================================================
TOOL SYSTEM
==================================================

Create explicit tools for agents.

At minimum:

1. get_request()
2. update_request()
3. create_task()
4. assign_request()
5. get_department()
6. get_user()
7. search_knowledge()
8. create_notification()
9. create_approval_request()
10. log_audit_event()
11. get_related_requests()
12. update_workflow_status()

Agents must call tools rather than directly manipulating arbitrary application state.

Validate every tool input.

Enforce authorization inside tools where appropriate.

==================================================
REQUEST MANAGEMENT
==================================================

Users must be able to:

- create requests
- edit permitted requests
- view requests
- filter requests
- search requests
- track status
- see assigned department
- see priority
- see workflow progress
- receive updates
- submit feedback

Request statuses:

- NEW
- CLASSIFYING
- ANALYZING
- ROUTING
- WAITING_FOR_APPROVAL
- APPROVED
- IN_PROGRESS
- COMPLETED
- REJECTED
- FAILED
- CANCELLED

==================================================
DASHBOARD
==================================================

Create a real CampusOS dashboard.

Student dashboard:

- Total requests
- Open requests
- Resolved requests
- Pending requests
- Recent requests
- Notifications

Admin dashboard:

- Active requests
- Agents online/status
- Resolved today
- Pending approvals
- Department workload
- Priority distribution
- Recent agent activity
- Failed workflows
- Average resolution time if calculable from actual data

Do NOT fabricate metrics.

Everything displayed on the dashboard must come from the database.

==================================================
ADMIN PANEL
==================================================

Implement a complete admin section.

Admin should be able to:

- create users
- edit users
- activate/deactivate users
- assign roles
- assign departments
- view requests
- filter requests
- inspect workflows
- inspect agent runs
- approve/reject sensitive actions
- view audit logs
- manage knowledge documents
- view analytics
- review feedback

==================================================
AUDITABILITY
==================================================

Every meaningful operation must generate an audit event.

Examples:

USER_CREATED
LOGIN
REQUEST_CREATED
REQUEST_UPDATED
REQUEST_CLASSIFIED
PRIORITY_ASSIGNED
REQUEST_ROUTED
AGENT_EXECUTED
TOOL_EXECUTED
VERIFICATION_COMPLETED
APPROVAL_REQUESTED
APPROVAL_APPROVED
APPROVAL_REJECTED
ACTION_EXECUTED
NOTIFICATION_SENT
REQUEST_RESOLVED

Audit records should contain enough information to reconstruct what happened.

==================================================
KNOWLEDGE BASE
==================================================

Implement a basic campus knowledge base.

Admins should be able to:

- add documents
- edit documents
- delete documents
- categorize documents
- associate documents with departments

Agents should be able to search this information.

Possible documents:

- hostel rules
- maintenance procedures
- department contacts
- scholarship policies
- academic procedures
- IT support instructions
- campus policies

Do not require an external vector database unless genuinely necessary.

For the hackathon MVP, a PostgreSQL/SQLAlchemy-backed retrieval layer is acceptable.

Structure the code so semantic/vector retrieval can be added later.

==================================================
NOTIFICATIONS
==================================================

Implement an internal notification system.

Events:

- request created
- request assigned
- approval required
- request approved
- action executed
- request completed
- request rejected
- workflow failed

Frontend should show:

- unread notification count
- notification dropdown/page
- mark as read

==================================================
FRONTEND
==================================================

Build a polished React application.

Use a professional modern dashboard design.

Pages:

Public:

- Login
- Register

Authenticated:

- Dashboard
- Create Request
- My Requests
- Request Details
- Notifications
- Profile

Staff:

- Assigned Requests
- Tasks
- Department Queue

Manager:

- Department Dashboard
- Approval Queue
- Analytics

Admin:

- Admin Dashboard
- Users
- Roles
- Departments
- Requests
- Workflows
- Agent Runs
- Approvals
- Audit Logs
- Knowledge Base
- Analytics
- Feedback

==================================================
REQUEST DETAILS PAGE
==================================================

Create a detailed request view.

Show:

- request title
- description
- requester
- category
- priority
- department
- assigned user
- current status
- workflow stage
- timeline
- agent activity
- verification
- approval
- action performed
- notifications
- audit events

The workflow visualization should show progression such as:

INTAKE
→ CLASSIFICATION
→ PRIORITY
→ RESEARCH
→ ROUTING
→ ANALYSIS
→ VERIFICATION
→ APPROVAL
→ EXECUTION
→ COMPLETION

==================================================
UI/UX
==================================================

Design language:

- professional
- modern
- clean
- technical
- enterprise dashboard
- hackathon-ready

Use:

- cards
- tables
- status badges
- workflow timelines
- agent status indicators
- charts
- filters
- search
- modals
- confirmation dialogs
- loading states
- error states
- empty states

Responsive design is required.

Desktop should be the primary target but make the interface usable on tablet/mobile.

==================================================
API DESIGN
==================================================

Implement REST endpoints.

Examples:

AUTH

POST /api/auth/register
POST /api/auth/login
POST /api/auth/refresh
POST /api/auth/logout
GET  /api/auth/me
POST /api/auth/change-password

USERS

GET /api/users
GET /api/users/:id
POST /api/users
PATCH /api/users/:id
DELETE /api/users/:id

REQUESTS

POST /api/requests
GET /api/requests
GET /api/requests/:id
PATCH /api/requests/:id
DELETE /api/requests/:id
POST /api/requests/:id/process
POST /api/requests/:id/cancel

WORKFLOWS

GET /api/workflows
GET /api/workflows/:id
POST /api/workflows/:id/resume

APPROVALS

GET /api/approvals
GET /api/approvals/:id
POST /api/approvals/:id/approve
POST /api/approvals/:id/reject
POST /api/approvals/:id/request-changes

AGENTS

GET /api/agents
GET /api/agents/status
GET /api/agents/runs
GET /api/agents/runs/:id

DASHBOARD

GET /api/dashboard/student
GET /api/dashboard/staff
GET /api/dashboard/manager
GET /api/dashboard/admin

AUDIT

GET /api/audit-logs

KNOWLEDGE

GET /api/knowledge
POST /api/knowledge
GET /api/knowledge/:id
PATCH /api/knowledge/:id
DELETE /api/knowledge/:id

FEEDBACK

POST /api/feedback
GET /api/feedback

NOTIFICATIONS

GET /api/notifications
PATCH /api/notifications/:id/read

Use consistent:

- status codes
- JSON structures
- error responses
- validation responses

==================================================
API RESPONSE FORMAT
==================================================

Use predictable JSON.

Success:

{
  "success": true,
  "data": {...},
  "message": "..."
}

Error:

{
  "success": false,
  "error": {
      "code": "...",
      "message": "...",
      "details": {}
  }
}

==================================================
LLM INTEGRATION
==================================================

Use environment variables for LLM configuration.

Example:

LLM_API_KEY=
LLM_MODEL=
LLM_BASE_URL=

Do not hard-code credentials.

Create a provider abstraction so the LLM provider can be changed later.

If no API key is configured, the application should still start.

For local/demo mode, implement a deterministic fallback/mock reasoning provider that clearly indicates DEMO MODE.

Do not make the entire application unusable because an LLM key is missing.

==================================================
AI SAFETY
==================================================

AI should never have unrestricted access to the database or operating system.

Implement:

- structured outputs
- validation
- explicit tools
- tool authorization
- verification
- human approval
- retry limits
- error handling
- audit logs

Never allow free-form generated text to become direct SQL or arbitrary commands.

==================================================
ERROR HANDLING
==================================================

Implement:

- centralized Flask error handlers
- validation errors
- authentication errors
- authorization errors
- database errors
- AI errors
- workflow errors
- tool execution errors
- timeout handling
- retry mechanisms

Use appropriate HTTP codes:

400
401
403
404
409
422
429
500
503

==================================================
LOGGING
==================================================

Implement application logging.

Log:

- API errors
- workflow execution
- agent execution
- tool usage
- failures
- retries
- approvals
- important security events

Never log passwords, secrets, JWT secrets, or sensitive tokens.

==================================================
TESTING
==================================================

DO NOT skip testing.

Create backend tests.

At minimum test:

AUTHENTICATION
- registration
- login
- invalid credentials
- token validation
- refresh
- protected routes

AUTHORIZATION
- student restrictions
- staff restrictions
- manager permissions
- admin permissions

REQUESTS
- create
- update
- list
- filters
- validation

WORKFLOW
- successful workflow
- verification failure
- human approval path
- autonomous execution path
- retry path
- workflow failure

AGENTS
- each agent can execute
- structured outputs
- invalid outputs rejected

DATABASE
- relationships
- constraints

API:
- successful responses
- errors
- permissions

Also create basic frontend tests where practical.

==================================================
SEED DATA
==================================================

Create a seed script.

Create example users:

admin@campusos.local
manager@campusos.local
staff@campusos.local
student@campusos.local

Use safe demo passwords clearly documented for LOCAL DEVELOPMENT ONLY.

Seed:

- departments
- users
- roles
- knowledge documents
- sample requests
- sample notifications
- sample audit logs

Include realistic CampusOS requests such as:

1. Broken water cooler
2. Scholarship query
3. Lab equipment issue
4. Hostel complaint
5. Event permission
6. IT support request

==================================================
DEMO MODE
==================================================

The project MUST be easy to demonstrate during a hackathon.

Create a demo-ready flow:

LOGIN
→ CREATE REQUEST
→ AI PROCESSING
→ AGENT WORKFLOW
→ VERIFICATION
→ APPROVAL IF REQUIRED
→ EXECUTION
→ NOTIFICATION
→ AUDIT LOG
→ RESOLUTION

Make this workflow reliable enough for a live presentation.

==================================================
DOCKER / LOCAL SETUP
==================================================

Create:

docker-compose.yml

Services:

- PostgreSQL
- backend
- frontend

The project should also support running without Docker if possible.

Provide:

backend setup
frontend setup
database setup
migration commands
seed command
test command
development command

==================================================
ENVIRONMENT VARIABLES
==================================================

Create .env.example.

Include appropriate variables such as:

DATABASE_URL=
JWT_SECRET_KEY=
JWT_ACCESS_TOKEN_EXPIRES=
JWT_REFRESH_TOKEN_EXPIRES=
LLM_API_KEY=
LLM_MODEL=
LLM_BASE_URL=
FRONTEND_URL=
FLASK_ENV=

Never commit .env.

Add .gitignore.

==================================================
DATABASE MIGRATIONS
==================================================

Use Flask-Migrate/Alembic with SQLAlchemy.

Provide:

initial migration

Commands:

flask db init
flask db migrate
flask db upgrade

Do not require users to manually create every database table.

==================================================
DOCUMENTATION
==================================================

Write a complete README.md.

Include:

1. Project overview
2. Problem statement
3. Solution
4. Architecture
5. Agent architecture
6. Technology stack
7. Features
8. Authentication
9. Authorization
10. Database schema overview
11. API documentation
12. Setup instructions
13. Environment variables
14. Docker usage
15. Seed data
16. Testing
17. Demo credentials
18. Example workflow
19. Project structure
20. Troubleshooting
21. Future improvements

==================================================
API DOCUMENTATION
==================================================

Create OpenAPI/Swagger documentation if practical.

Document:

- endpoints
- parameters
- request bodies
- authentication
- responses
- error codes

==================================================
DATABASE DESIGN
==================================================

Make database relationships clear.

At minimum:

User
  |
  +---- Role
  |
  +---- Department
  |
  +---- Requests
           |
           +---- Workflow
           |       |
           |       +---- WorkflowTasks
           |       +---- AgentRuns
           |       +---- Approval
           |
           +---- Notifications
           +---- AuditLogs
           +---- Feedback

==================================================
PERFORMANCE
==================================================

Use proper:

- indexes
- pagination
- query filtering
- eager/lazy relationship strategy where appropriate
- connection management
- caching only when useful

Do not load thousands of rows into memory unnecessarily.

==================================================
FRONTEND STATE
==================================================

Implement sensible state management.

Authentication state should persist appropriately.

Handle:

- loading
- success
- failure
- expired tokens
- refresh
- logout
- unauthorized access

Create protected frontend routes.

==================================================
AUTHORIZATION UX
==================================================

Frontend must dynamically show relevant navigation based on role.

Example:

STUDENT:
Dashboard
My Requests
Create Request
Notifications
Profile

STAFF:
Dashboard
Assigned Requests
Tasks
Notifications
Profile

MANAGER:
Dashboard
Requests
Approvals
Analytics
Notifications

ADMIN:
Dashboard
Users
Requests
Workflows
Agents
Approvals
Audit Logs
Knowledge Base
Analytics
Settings

But remember:

FRONTEND VISIBILITY IS NOT SECURITY.

The backend MUST enforce authorization.

==================================================
AGENT OBSERVABILITY
==================================================

Create an Agent Activity view.

Show:

- agent name
- status
- execution time
- task
- input summary
- output summary
- success/failure
- timestamp

Allow authorized users/admins to inspect workflow execution.

==================================================
WORKFLOW TIMELINE
==================================================

Create a visual timeline.

Example:

✓ Request Created
✓ Intake Completed
✓ Classified as Maintenance
✓ Priority = High
✓ Routed to Facilities
✓ Analysis Completed
✓ Verification Passed
⚠ Human Approval Required
✓ Approved by Manager
✓ Maintenance Task Created
✓ Student Notified
✓ Audit Logged
✓ Request Resolved

==================================================
NOTIFICATION FLOW
==================================================

When a request changes state:

1. persist notification
2. update notification status
3. show it in frontend
4. create audit log

Email is optional.

Do not make email infrastructure mandatory for MVP.

==================================================
ANALYTICS
==================================================

Use actual database data.

Create charts for:

- requests by category
- requests by department
- requests by priority
- request status
- workflow success/failure
- approvals
- resolution trends

Do not fabricate metrics.

For an empty database, display an appropriate empty state.

==================================================
ADMIN AUDIT VIEW
==================================================

Create filters:

- actor
- action
- date
- request
- workflow
- department
- severity/type

Add pagination.

==================================================
QUALITY REQUIREMENTS
==================================================

Code must be:

- modular
- typed where practical
- documented
- readable
- maintainable
- secure
- testable

Avoid giant files.

Avoid duplicated logic.

Use service layers rather than putting everything in Flask route handlers.

Use environment-based configuration.

Use constants/enums where appropriate.

==================================================
IMPORTANT: REAL IMPLEMENTATION
==================================================

Do not stop after creating the architecture.

Actually create:

- backend
- frontend
- database models
- migrations
- API endpoints
- authentication
- authorization
- LangGraph workflow
- agents
- tools
- verification
- human approval
- audit logging
- notifications
- dashboard
- admin panel
- tests
- seed script
- README
- Docker configuration

==================================================
DEVELOPMENT PROCESS
==================================================

Follow this order:

PHASE 1
Analyze requirements.

PHASE 2
Create the complete repository structure.

PHASE 3
Implement configuration and environment handling.

PHASE 4
Implement SQLAlchemy models.

PHASE 5
Implement migrations.

PHASE 6
Implement authentication.

PHASE 7
Implement RBAC authorization.

PHASE 8
Implement REST APIs.

PHASE 9
Implement CampusOS services.

PHASE 10
Implement LangGraph state and workflow.

PHASE 11
Implement agents.

PHASE 12
Implement tools and tool authorization.

PHASE 13
Implement verification.

PHASE 14
Implement human approval.

PHASE 15
Implement audit logging.

PHASE 16
Implement notifications.

PHASE 17
Implement knowledge base.

PHASE 18
Implement React frontend.

PHASE 19
Implement role-based dashboards.

PHASE 20
Implement workflow visualization.

PHASE 21
Implement admin panel.

PHASE 22
Implement analytics.

PHASE 23
Implement seed/demo data.

PHASE 24
Implement tests.

PHASE 25
Run all tests.

PHASE 26
Run backend.

PHASE 27
Run frontend.

PHASE 28
Fix all errors.

PHASE 29
Verify authentication/authorization.

PHASE 30
Verify end-to-end request workflow.

PHASE 31
Verify database persistence.

PHASE 32
Verify human approval flow.

PHASE 33
Verify audit logging.

PHASE 34
Update README with exact commands.

==================================================
SELF-TEST REQUIREMENT
==================================================

After implementation, ACTUALLY TEST THE APPLICATION.

Perform at minimum:

1. Start PostgreSQL.
2. Run migrations.
3. Seed database.
4. Start Flask backend.
5. Test health endpoint.
6. Register a user.
7. Login.
8. Obtain JWT.
9. Access protected route.
10. Verify unauthorized route rejection.
11. Create a request.
12. Process request through LangGraph.
13. Verify classification.
14. Verify routing.
15. Verify priority.
16. Verify verification.
17. Trigger human approval when appropriate.
18. Approve workflow.
19. Execute action.
20. Generate notification.
21. Generate audit log.
22. Confirm database records.
23. Open React application.
24. Login through UI.
25. Create request through UI.
26. Observe workflow.
27. View request details.
28. View notifications.
29. View audit information as authorized user.
30. Verify role restrictions.

Fix any errors discovered during these steps.

==================================================
NO FAKE COMPLETION
==================================================

Do not say:

"Implemented"

unless the feature actually exists.

Do not say:

"Tests pass"

unless you actually ran them.

Do not claim:

"production ready"

unless you have genuinely verified the application.

At the end, provide:

1. what was implemented
2. exact commands to run it
3. demo credentials
4. test results
5. known limitations
6. files/folders created
7. next recommended steps

==================================================
PREMIUM UI / UX REQUIREMENTS — VERY IMPORTANT
==================================================

CampusOS must look like a PREMIUM, MODERN, ENTERPRISE-GRADE
UNIVERSITY OPERATIONS PLATFORM.

The application must NOT look like a typical "AI agent" application.

IMPORTANT:

The AI and multi-agent architecture should exist primarily
behind the scenes.

Users should experience CampusOS as a polished,
professional campus operations platform.

DO NOT make the UI look:

- robotic
- futuristic
- overly AI-themed
- filled with glowing effects
- filled with neon colors
- cyberpunk
- overly technical
- like an LLM playground
- like a developer agent console

Avoid excessive:

- robot icons
- brain icons
- AI sparkles
- animated neural networks
- glowing borders
- neon gradients
- excessive purple/pink AI styling
- agent cards everywhere
- "AI thinking" animations
- terminal-like interfaces

The AI should feel like an invisible intelligent infrastructure
powering the platform.

==================================================
VISUAL DESIGN DIRECTION
==================================================

Design CampusOS like a premium combination of:

- modern university portal
- enterprise workflow management platform
- ServiceNow-style operations interface
- Linear-style clean workflow management
- modern SaaS administration dashboard

The visual experience should communicate:

TRUST
CLARITY
EFFICIENCY
SECURITY
PROFESSIONALISM
INTELLIGENCE

NOT:

"LOOK, THIS USES AI!"

The goal is:

"CampusOS is a professional system that happens to
be intelligently automated."

==================================================
COLOR SYSTEM
==================================================

Use a sophisticated professional color palette.

Primary:

Deep Navy / Midnight Blue

Secondary:

Professional Blue

Supporting colors:

White
Light Gray
Slate Gray

Status colors:

Green → Successful / Completed
Amber → Pending / Waiting
Red → Critical / Failed
Blue → Informational

Use accent colors sparingly.

Avoid excessive gradients.

Avoid neon colors.

Avoid rainbow UI.

==================================================
TYPOGRAPHY
==================================================

Use a premium modern sans-serif typography system.

Prefer:

Inter
Poppins
Manrope
or another clean professional sans-serif.

Use:

- clear hierarchy
- strong page titles
- readable body text
- compact labels
- consistent spacing

Do not use decorative/futuristic fonts.

==================================================
LAYOUT
==================================================

Use a polished application shell.

Desktop:

------------------------------------------------
| CampusOS | Sidebar                 Top Bar    |
|           |                              🔔   |
|           |                              👤   |
|           |----------------------------------|
|           |                                  |
|           |         MAIN CONTENT              |
|           |                                  |
------------------------------------------------

Left Sidebar:

CampusOS logo

Dashboard
Requests
Create Request
My Requests
Notifications

Role-specific:

Assigned Tasks
Department
Approvals
Analytics

Admin:

Users
Departments
Workflows
Knowledge Base
Audit Logs
System Settings

Bottom:

Profile
Logout

==================================================
TOP NAVIGATION
==================================================

Top bar should contain:

- page title
- breadcrumbs where useful
- search
- notification icon
- user profile
- role indicator
- logout/profile menu

Keep it minimal.

==================================================
LOGIN PAGE
==================================================

Create a PREMIUM login page.

Do NOT create a generic developer login page.

Include:

CampusOS logo/name

"Welcome back"

Email

Password

Show/hide password

Remember me

Forgot password

Sign In button

AND VERY IMPORTANT:

A visible Sign Up option.

Example:

"Don't have an account? Sign up"

The Sign Up link must route to:

/register

==================================================
SIGN UP / REGISTRATION PAGE
==================================================

Implement a complete registration page.

Do NOT only create a login page.

Users must be able to create accounts.

Registration fields:

Full Name
Email
Password
Confirm Password
Phone Number (optional)
Role
Department (when applicable)

Do NOT allow normal users to freely assign themselves
privileged roles such as ADMIN.

IMPORTANT SECURITY RULE:

The frontend may show a role field only for roles that the
current registration policy allows.

A public user must NEVER be able to register themselves
as ADMIN or DEPARTMENT_MANAGER.

Recommended public registration:

Student
Faculty

Staff/Manager/Admin accounts should be created by authorized
administrators.

==================================================
USER CREATION
==================================================

Implement TWO user creation mechanisms.

1. Self Registration

Students / faculty can register themselves.

2. Admin User Management

Authorized administrators can create:

- students
- faculty
- staff
- department managers
- administrators

Admin user creation should include:

Name
Email
Password / invitation mechanism
Role
Department
Account status

==================================================
REGISTRATION FLOW
==================================================

Public:

SIGN UP
  ↓
Validate input
  ↓
Check duplicate email
  ↓
Hash password
  ↓
Create user
  ↓
Assign allowed default role
  ↓
Create audit log
  ↓
Redirect to Login
  ↓
User signs in

Admin-created:

ADMIN
 ↓
Users
 ↓
Add User
 ↓
Select Role
 ↓
Select Department
 ↓
Create Account
 ↓
Audit Log

==================================================
FORGOT PASSWORD
==================================================

Implement a proper forgot-password flow.

Pages:

/forgot-password

/reset-password

For local/demo mode, provide a safe development mechanism
without requiring an external email provider.

Do not expose password reset tokens in production logs.

==================================================
USER PROFILE
==================================================

Create a polished profile page.

Display:

- profile photo/avatar
- name
- email
- role
- department
- account status
- joined date

Actions:

Edit Profile
Change Password
Logout

==================================================
DASHBOARD DESIGN
==================================================

Do NOT make the dashboard look like an AI control center.

Instead create a clean operations dashboard.

Student dashboard:

Welcome message

"Good morning, Tanmay"

Summary cards:

Open Requests
In Progress
Resolved
Pending

Recent Requests table.

Quick Action:

"+ Create New Request"

Notifications section.

==================================================
ADMIN DASHBOARD
==================================================

Admin dashboard should focus on OPERATIONS.

Top metrics:

Total Requests
Open Requests
Pending Approvals
Resolved Today

Then:

Request Trends
Department Workload
Priority Distribution
Recent Requests
Recent Activity

Charts should look like normal enterprise analytics.

Do not put:

"10 AI agents running"

as the dominant feature.

Agent execution should be secondary.

==================================================
REQUEST CREATION UX
==================================================

Make creating a request extremely simple.

Page:

Create Request

Fields:

Request Title
Description
Category
Priority (optional / system-assisted)
Department (optional)

Attachment support where practical.

Example categories:

Hostel
Maintenance
Facilities
Academics
Finance
IT Support
Administration
Lost & Found
Student Grievance
Other

CTA:

Submit Request

After submission:

Show a clean workflow status page.

==================================================
REQUEST TRACKING
==================================================

Request tracking should feel like a professional
ticket/work-order system.

Show:

Request ID
Title
Category
Priority
Department
Assigned Staff
Created Date
Last Updated
Current Status

Status timeline:

Submitted
Under Review
Assigned
In Progress
Pending Approval
Completed

Do NOT expose every low-level LLM operation to normal users.

Instead of:

"Research Agent → Analysis Agent → Action Agent"

show:

"CampusOS is reviewing your request..."

"Request routed to Facilities."

"Maintenance action approved."

"Request completed."

This keeps the experience professional.

==================================================
AI TRANSPARENCY
==================================================

AI activity should be visible ONLY where useful.

For normal users:

Show simple explanations.

Example:

"CampusOS identified this as a Maintenance request
and routed it to Facilities."

For administrators:

Provide an optional:

"View AI Processing Details"

section.

There administrators can inspect:

- classification reasoning
- routing reasoning
- priority reasoning
- verification
- proposed action
- agent execution history

This information must remain secondary to the main workflow.

==================================================
AGENT UI
==================================================

Do NOT create a dedicated "AI Agent Wall" as the primary
dashboard.

Agents should instead appear as supporting infrastructure.

For administrators, create:

Agent Activity

with a clean table:

Agent
Task
Request
Status
Started
Completed
Duration

Example:

Research Agent
Knowledge Retrieval
REQ-1042
Completed

Verification Agent
Action Validation
REQ-1042
Passed

Keep this subtle.

==================================================
REQUEST DETAILS
==================================================

The Request Details page should be the central experience.

Structure:

------------------------------------------------
Request #1042
Broken Water Cooler
------------------------------------------------

Status: In Progress

Priority: High

Department: Facilities

Assigned To: Maintenance Team

------------------------------------------------

Description

The water cooler near Block B
has not worked for 3 days.

------------------------------------------------

Progress

✓ Submitted
✓ Classified
✓ Routed
✓ Verified
● Action in Progress
○ Completed

------------------------------------------------

Updates

Maintenance ticket created.
Facilities team notified.

------------------------------------------------

Activity

Timestamp | Action | Actor

------------------------------------------------

At the bottom:

Feedback

"How was this request handled?"

★★★★★

Comment box

Submit Feedback

==================================================
TABLE DESIGN
==================================================

Tables should look premium and readable.

Use:

- rounded corners
- subtle borders
- whitespace
- status pills
- compact rows
- pagination
- search
- filters
- sorting

Example:

REQUEST ID
REQ-1042

REQUEST
Broken Water Cooler

DEPARTMENT
Facilities

PRIORITY
HIGH

STATUS
In Progress

Use subtle status badges.

==================================================
FORMS
==================================================

All forms should have:

- clear labels
- helpful placeholder text
- inline validation
- error messages
- loading state
- success state
- disabled state

Do not rely only on browser validation.

Backend validation is mandatory.

==================================================
EMPTY STATES
==================================================

Do not leave blank screens.

Example:

"No requests yet."

"You haven't submitted any campus requests.
Create your first request to get started."

Provide CTA buttons.

==================================================
LOADING STATES
==================================================

Use professional skeleton loaders and progress indicators.

Avoid:

"AI IS THINKING..."

Avoid robot animations.

Instead:

"Processing request..."

"Analyzing request details..."

"Routing to the appropriate department..."

==================================================
ERROR STATES
==================================================

Use clear human-readable messages.

Bad:

ERR_AGENT_NODE_FAILURE_329

Good:

"We couldn't process this request right now.
Please try again."

Admins may see technical details separately.

==================================================
NOTIFICATIONS
==================================================

Use a standard SaaS notification system.

Bell icon in top navigation.

Notifications:

"Your maintenance request has been assigned."

"Your request is awaiting approval."

"Your request has been completed."

Keep notifications professional.

==================================================
ADMIN USER MANAGEMENT UI
==================================================

Create:

/admin/users

Features:

- Search users
- Filter by role
- Filter by department
- Filter by status
- Create user
- Edit user
- Activate/deactivate
- Change role
- Assign department
- Reset password where authorized

Table:

Name
Email
Role
Department
Status
Created
Actions

Add User button.

==================================================
ROLE MANAGEMENT
==================================================

Create:

/admin/roles

Show:

Role
Description
Permissions

Do not allow arbitrary privilege escalation.

Admin should control authorization policies.

==================================================
DEPARTMENT MANAGEMENT
==================================================

Create:

/admin/departments

Admin can:

- create department
- edit department
- deactivate department
- assign managers
- assign staff
- view workload

==================================================
APPROVAL UI
==================================================

For managers/admins:

Create an Approval Queue.

Example:

------------------------------------------------
Approval Required

Request: Student fee adjustment
Risk: High

Reason:
This action modifies financial information.

Proposed Action:
Update fee record.

Verification:
Passed

[ Approve ] [ Reject ] [ Request Changes ]
------------------------------------------------

Make this look like a professional approval workflow.

==================================================
AUDIT LOG UI
==================================================

Do not expose audit logs to ordinary users.

Admin-only.

Display:

Timestamp
Actor
Role
Action
Request
Workflow
Result

Filters:

Date
User
Action
Department

==================================================
RESPONSIVE DESIGN
==================================================

The application must work on:

Desktop
Laptop
Tablet
Mobile

On mobile:

Sidebar becomes a drawer.

Tables become horizontally scrollable or card-based.

Forms stack vertically.

==================================================
ACCESSIBILITY
==================================================

Implement:

- keyboard navigation
- visible focus states
- semantic HTML
- appropriate labels
- accessible buttons
- readable contrast
- accessible form errors
- ARIA attributes where needed

==================================================
MICRO-INTERACTIONS
==================================================

Use subtle, premium micro-interactions:

- button hover
- card hover
- smooth transitions
- dropdown animation
- modal animation
- status transitions

Keep animations subtle.

Do NOT use excessive animated AI effects.

==================================================
PREMIUM DESIGN RULE
==================================================

The first impression should be:

"This looks like a serious university operations platform."

NOT:

"This looks like an AI demo."

AI is the intelligence layer.

CampusOS is the product.

==================================================
AUTHENTICATION UX REQUIREMENT
==================================================

The authentication system MUST include:

/login
/register
/forgot-password
/reset-password
/profile

There must be an obvious path between:

LOGIN ↔ SIGN UP

Example:

Login page:

"Don't have an account? Create one"

Register page:

"Already have an account? Sign in"

==================================================
REGISTRATION SECURITY
==================================================

Public registration must NOT allow:

ADMIN
DEPARTMENT_MANAGER

as self-selected roles.

Default public role:

STUDENT

Faculty registration can either:

- allow FACULTY registration
OR
- require admin approval

Implement the safer approach.

Admin can create privileged accounts.

==================================================
FINAL UI ACCEPTANCE CRITERIA
==================================================

[ ] Premium SaaS-like design
[ ] Looks like university operations software
[ ] NOT overly agentic
[ ] NOT overly AI-themed
[ ] Clean navigation
[ ] Professional dashboard
[ ] Professional tables
[ ] Professional forms
[ ] Request tracking
[ ] Notifications
[ ] User profile
[ ] Login page
[ ] Sign Up page
[ ] Forgot Password
[ ] Reset Password
[ ] Admin user creation
[ ] Role management
[ ] Department management
[ ] RBAC
[ ] Responsive design
[ ] Accessible interface
[ ] Proper loading states
[ ] Proper error states
[ ] Empty states
[ ] Human approval interface
[ ] Audit interface
[ ] AI details hidden behind secondary views
[ ] No fake buttons
[ ] No static fake dashboard values

MOST IMPORTANT:

Build the application so that a student, faculty member,
staff member, manager, or administrator can use CampusOS
without needing to understand anything about LangGraph,
LLMs, agents, orchestration, prompts, or AI internals.

The AI should make CampusOS smarter.

It should NOT make CampusOS harder to use.
==================================================
HACKATHON DEMO PRIORITY
==================================================

Prioritize a reliable end-to-end demo.

The most important demo path is:

Student Login
      ↓
Create Request
      ↓
CampusOS receives request
      ↓
AI Workforce Manager
      ↓
Classification Agent
      ↓
Priority Agent
      ↓
Research Agent
      ↓
Routing Agent
      ↓
Analysis Agent
      ↓
Verification Agent
      ↓
Human Approval if needed
      ↓
Action Agent
      ↓
Database update
      ↓
Notification
      ↓
Audit Log
      ↓
Student sees resolution

Example request:

"The water cooler near Block B has not worked for 3 days."

Expected result:

Category:
Maintenance

Priority:
High

Department:
Facilities / Maintenance

Suggested Action:
Create maintenance ticket

Verification:
Passed

Execution:
Maintenance task created

Notification:
Student notified

Audit:
Complete workflow recorded

==================================================
FINAL ACCEPTANCE CRITERIA
==================================================

The project is considered complete ONLY when:

[ ] Flask backend works
[ ] React frontend works
[ ] PostgreSQL works
[ ] SQLAlchemy models work
[ ] Database migrations work
[ ] JWT authentication works
[ ] RBAC authorization works
[ ] User roles work
[ ] Request management works
[ ] LangGraph workflow works
[ ] AI agents work
[ ] Agent tools work
[ ] Verification works
[ ] Human approval works
[ ] Autonomous execution works for allowed tasks
[ ] Notifications work
[ ] Audit logs work
[ ] Knowledge base works
[ ] Admin dashboard works
[ ] Role-specific dashboards work
[ ] Analytics work
[ ] Workflow timeline works
[ ] Error handling works
[ ] Logging works
[ ] Seed script works
[ ] Tests exist
[ ] Tests have been executed
[ ] Docker setup works
[ ] README exists
[ ] .env.example exists
[ ] .gitignore exists
[ ] No secrets are hard-coded
[ ] No fake dashboard statistics
[ ] No fake functionality
[ ] No dead buttons
[ ] No unimplemented critical endpoints

==================================================
FINAL INSTRUCTION
==================================================

START BUILDING THE PROJECT NOW.

Do not spend the entire response explaining what you would build.

Actually create the files and implement the application.

Work incrementally.

After each major phase:

1. inspect the code
2. run relevant tests
3. fix errors
4. continue

Do not stop at scaffolding.

Do not skip the backend.

Do not skip the database.

Do not skip authentication.

Do not skip authorization.

Do not skip LangGraph.

Do not skip the agents.

Do not skip human approval.

Do not skip audit logs.

Do not skip testing.

Build CampusOS as a genuinely functional autonomous AI workforce platform.
