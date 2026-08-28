import pytest
import sys
import os

# Set env vars before importing app
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['JWT_SECRET_KEY'] = 'test-secret-key'
os.environ['SECRET_KEY'] = 'test-secret-key'

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.config import Config

# Override config for SQLite testing
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ENGINE_OPTIONS = {}

from app import create_app
from app.extensions import db as _db
from app.models.role import Role
from app.models.department import Department
from app.models.user import User


@pytest.fixture(scope='session')
def app():
    app = create_app(config_class=TestConfig)
    with app.app_context():
        _db.create_all()
        # Seed roles and departments
        for name, desc in [('STUDENT', 'Student'), ('FACULTY', 'Faculty'), ('STAFF', 'Staff'), ('DEPARTMENT_MANAGER', 'Manager'), ('ADMIN', 'Admin')]:
            if not Role.query.filter_by(name=name).first():
                _db.session.add(Role(name=name, description=desc, permissions=[]))
        for name, desc in [('Maintenance', 'Maint'), ('IT Support', 'IT'), ('Finance', 'Finance'), ('Administration', 'Admin')]:
            if not Department.query.filter_by(name=name).first():
                _db.session.add(Department(name=name, description=desc))
        _db.session.commit()
        yield app
        _db.drop_all()


@pytest.fixture(scope='function')
def db(app):
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.rollback()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def sample_role(db):
    role = Role.query.filter_by(name='STUDENT').first()
    if not role:
        role = Role(name='STUDENT', description='Student', permissions=['create_request'])
        db.session.add(role)
        db.session.commit()
    return role


@pytest.fixture
def admin_role(db):
    role = Role.query.filter_by(name='ADMIN').first()
    if not role:
        role = Role(name='ADMIN', description='Admin', permissions=['manage_users'])
        db.session.add(role)
        db.session.commit()
    return role


@pytest.fixture
def manager_role(db):
    role = Role.query.filter_by(name='DEPARTMENT_MANAGER').first()
    if not role:
        role = Role(name='DEPARTMENT_MANAGER', description='Manager', permissions=['approve'])
        db.session.add(role)
        db.session.commit()
    return role


@pytest.fixture
def sample_user(db, sample_role):
    user = User.query.filter_by(email='student@test.com').first()
    if not user:
        user = User(name='Test Student', email='student@test.com', role_id=sample_role.id)
        user.set_password('TestPass123!')
        db.session.add(user)
        db.session.commit()
    return user


@pytest.fixture
def admin_user(db, admin_role):
    user = User.query.filter_by(email='admin@test.com').first()
    if not user:
        user = User(name='Test Admin', email='admin@test.com', role_id=admin_role.id)
        user.set_password('AdminPass123!')
        db.session.add(user)
        db.session.commit()
    return user


@pytest.fixture
def sample_dept(db):
    dept = Department.query.filter_by(name='Maintenance').first()
    if not dept:
        dept = Department(name='Maintenance', description='Campus maintenance')
        db.session.add(dept)
        db.session.commit()
    return dept


@pytest.fixture
def auth_headers(client, sample_user):
    res = client.post('/api/auth/login', json={'email': 'student@test.com', 'password': 'TestPass123!'})
    token = res.get_json()['data']['access_token']
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def admin_headers(client, admin_user):
    res = client.post('/api/auth/login', json={'email': 'admin@test.com', 'password': 'AdminPass123!'})
    token = res.get_json()['data']['access_token']
    return {'Authorization': f'Bearer {token}'}
