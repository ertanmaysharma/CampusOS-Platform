"""Seed the CampusOS database with demo data."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime, timedelta
from app import create_app
from app.extensions import db
from app.models.role import Role
from app.models.department import Department
from app.models.user import User
from app.models.request import Request
from app.models.knowledge_document import KnowledgeDocument
from app.models.workflow import Workflow
from app.models.notification import Notification
from app.models.audit_log import AuditLog
import random


def seed():
    app = create_app()
    with app.app_context():
        print("🌱 Seeding CampusOS database...")

        # Create roles
        roles_data = [
            ("STUDENT", "Student role", ["create_request", "view_own_requests", "provide_feedback"]),
            ("FACULTY", "Faculty role", ["create_request", "view_requests", "provide_feedback"]),
            ("STAFF", "Staff role", ["view_assigned", "update_tasks", "add_comments"]),
            ("DEPARTMENT_MANAGER", "Department Manager", ["review_requests", "assign_staff", "approve_actions"]),
            ("ADMIN", "Administrator", ["manage_users", "manage_departments", "view_all", "manage_knowledge"]),
        ]
        roles = {}
        for name, desc, perms in roles_data:
            role = Role.query.filter_by(name=name).first()
            if not role:
                role = Role(name=name, description=desc, permissions=perms)
                db.session.add(role)
            roles[name] = role
        db.session.commit()
        print(f"  ✅ Roles: {', '.join(roles.keys())}")

        # Create departments
        dept_data = [
            ("Hostel", "Hostel management and accommodation services"),
            ("Maintenance", "Campus maintenance and repairs"),
            ("Facilities", "Facility management and operations"),
            ("Academics", "Academic affairs and student records"),
            ("Finance", "Financial services and billing"),
            ("Administration", "General administration"),
            ("IT Support", "Information technology support"),
        ]
        departments = {}
        for name, desc in dept_data:
            dept = Department.query.filter_by(name=name).first()
            if not dept:
                dept = Department(name=name, description=desc)
                db.session.add(dept)
            departments[name] = dept
        db.session.commit()
        print(f"  ✅ Departments: {', '.join(departments.keys())}")

        # Create users
        users_data = [
            ("Admin User", "admin@campusos.local", "Admin123!", "ADMIN", "Administration"),
            ("Manager User", "manager@campusos.local", "Manager123!", "DEPARTMENT_MANAGER", "Maintenance"),
            ("Staff User", "staff@campusos.local", "Staff123!", "STAFF", "Maintenance"),
            ("Student User", "student@campusos.local", "Student123!", "STUDENT", None),
            ("John Faculty", "faculty@campusos.local", "Faculty123!", "FACULTY", "Academics"),
        ]
        users = {}
        for name, email, password, role_name, dept_name in users_data:
            user = User.query.filter_by(email=email).first()
            if not user:
                user = User(
                    name=name,
                    email=email,
                    role_id=roles[role_name].id,
                    department_id=departments[dept_name].id if dept_name else None,
                    is_active=True,
                )
                user.set_password(password)
                db.session.add(user)
            users[email] = user
        db.session.commit()
        print(f"  ✅ Users: {len(users)} created")

        # Create knowledge documents
        kb_docs = [
            ("Hostel Rules and Regulations", "Students must follow hostel timings. Quiet hours are 10 PM to 6 AM. Visitors are not allowed in hostel rooms. Mess timings: Breakfast 7-9 AM, Lunch 12-2 PM, Dinner 7-9 PM.", "Hostel Rules", "Hostel"),
            ("Maintenance Request Procedure", "Submit a request through CampusOS. Include location, description, and urgency. The maintenance team will respond within 24-48 hours for non-critical issues.", "Maintenance Procedures", "Maintenance"),
            ("Campus IT Support", "For WiFi issues: restart your device, forget and reconnect to campus WiFi. For software issues: contact IT helpdesk. Lab computers: report issues to lab coordinator.", "IT Support", "IT Support"),
            ("Scholarship Application Process", "Scholarship applications open in January and July. Required documents: transcript, recommendation letter, financial aid form. Submit through the Finance department.", "Scholarship Policies", "Finance"),
            ("Event Permission Guidelines", "Events require 2-week advance approval. Submit event proposal to Administration. Include expected attendance, budget, and venue requirements.", "Campus Policies", "Administration"),
        ]
        for title, content, category, dept_name in kb_docs:
            existing = KnowledgeDocument.query.filter_by(title=title).first()
            if not existing:
                doc = KnowledgeDocument(
                    title=title,
                    content=content,
                    category=category,
                    department_id=departments[dept_name].id,
                )
                db.session.add(doc)
        db.session.commit()
        print(f"  ✅ Knowledge documents: {len(kb_docs)} created")

        # Create sample requests
        student = users["student@campusos.local"]
        requests_data = [
            ("Broken Water Cooler", "The water cooler near Block B has not worked for 3 days. Students are unable to get drinking water.", "Maintenance", "HIGH", "Maintenance"),
            ("Scholarship Query", "I want to know about the scholarship application process for the upcoming semester.", "Finance", "MEDIUM", "Finance"),
            ("Lab Equipment Issue", "The projector in Computer Lab 3 is not displaying properly. It shows a blue screen.", "IT Support", "HIGH", "IT Support"),
            ("Hostel AC Not Working", "The air conditioner in Room 204, Block A has been making loud noises and not cooling.", "Hostel", "MEDIUM", "Hostel"),
            ("Event Permission Request", "We want to organize a tech fest in the auditorium next month. Need permission and logistics support.", "Administration", "LOW", "Administration"),
            ("WiFi Connectivity Issues", "The WiFi in the library has been extremely slow for the past week. Cannot access online resources.", "IT Support", "MEDIUM", "IT Support"),
        ]
        for title, desc, cat, pri, dept_name in requests_data:
            existing = Request.query.filter_by(title=title).first()
            if not existing:
                req_num = f"REQ-{random.randint(1000, 9999)}"
                req = Request(
                    request_number=req_num,
                    requester_id=student.id,
                    title=title,
                    description=desc,
                    category=cat,
                    priority=pri,
                    status="NEW",
                    department_id=departments[dept_name].id,
                )
                db.session.add(req)
                db.session.flush()

                # Create workflow
                workflow = Workflow(request_id=req.id, state="INTAKE", status="RUNNING")
                db.session.add(workflow)
        db.session.commit()
        print(f"  ✅ Sample requests: {len(requests_data)} created")

        # Create sample notifications
        notifs = [
            ("Welcome to CampusOS", "Your account has been created successfully. Start by creating your first request.", "ACCOUNT_CREATED"),
            ("Request Created", "Your maintenance request has been submitted and is being processed.", "REQUEST_CREATED"),
        ]
        for title, msg, ntype in notifs:
            notif = Notification(
                recipient_id=student.id,
                title=title,
                message=msg,
                type=ntype,
            )
            db.session.add(notif)
        db.session.commit()
        print(f"  ✅ Notifications created")

        # Create sample audit logs
        audit_entries = [
            ("USER_CREATED", "SYSTEM", {"user": "admin@campusos.local"}),
            ("REQUEST_CREATED", "USER", {"title": "Broken Water Cooler"}),
        ]
        for action, actor, meta in audit_entries:
            log = AuditLog(
                user_id=student.id,
                action=action,
                actor_type=actor,
                meta_data=meta,
            )
            db.session.add(log)
        db.session.commit()
        print(f"  ✅ Audit logs created")

        print("\n🎉 CampusOS database seeded successfully!")
        print("\n📋 Demo Credentials:")
        print("  Admin:     admin@campusos.local / Admin123!")
        print("  Manager:   manager@campusos.local / Manager123!")
        print("  Staff:     staff@campusos.local / Staff123!")
        print("  Student:   student@campusos.local / Student123!")
        print("  Faculty:   faculty@campusos.local / Faculty123!")


if __name__ == "__main__":
    seed()
