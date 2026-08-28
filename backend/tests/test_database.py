def test_user_model(db):
    from app.models.user import User
    from app.models.role import Role
    role = Role(name='STUDENT', description='Test')
    db.session.add(role)
    db.session.commit()

    user = User(name='Test', email='test@test.com', role_id=role.id)
    user.set_password('Password123!')
    db.session.add(user)
    db.session.commit()

    assert user.id is not None
    assert user.check_password('Password123!')
    assert not user.check_password('WrongPassword')
    assert user.password_hash != 'Password123!'  # Never stored plain text


def test_request_model(db):
    from app.models.request import Request
    from app.models.user import User
    from app.models.role import Role
    role = Role(name='STUDENT', description='Test')
    db.session.add(role)
    db.session.commit()

    user = User(name='Test', email='test2@test.com', role_id=role.id)
    user.set_password('Pass123!')
    db.session.add(user)
    db.session.commit()

    req = Request(
        request_number='REQ-0001',
        requester_id=user.id,
        title='Test Request',
        description='Test description',
        category='Maintenance',
        priority='HIGH',
    )
    db.session.add(req)
    db.session.commit()

    assert req.id is not None
    assert req.request_number == 'REQ-0001'
    assert req.status == 'NEW'


def test_workflow_model(db):
    from app.models.workflow import Workflow
    from app.models.request import Request
    from app.models.user import User
    from app.models.role import Role
    role = Role(name='STUDENT', description='Test')
    db.session.add(role)
    db.session.commit()

    user = User(name='Test', email='test3@test.com', role_id=role.id)
    user.set_password('Pass123!')
    db.session.add(user)
    db.session.commit()

    req = Request(
        request_number='REQ-0002',
        requester_id=user.id,
        title='Test',
        description='Test',
        category='Other',
    )
    db.session.add(req)
    db.session.commit()

    workflow = Workflow(request_id=req.id, state='INTAKE')
    db.session.add(workflow)
    db.session.commit()

    assert workflow.id is not None
    assert workflow.state == 'INTAKE'


def test_department_model(db):
    from app.models.department import Department
    dept = Department(name='IT Support', description='Tech support')
    db.session.add(dept)
    db.session.commit()
    assert dept.id is not None


def test_notification_model(db):
    from app.models.notification import Notification
    from app.models.user import User
    from app.models.role import Role
    role = Role(name='STUDENT', description='Test')
    db.session.add(role)
    db.session.commit()

    user = User(name='Test', email='test4@test.com', role_id=role.id)
    user.set_password('Pass123!')
    db.session.add(user)
    db.session.commit()

    notif = Notification(
        recipient_id=user.id,
        title='Test Notification',
        message='Test message',
        type='TEST',
    )
    db.session.add(notif)
    db.session.commit()
    assert notif.id is not None
    assert notif.is_read is False


def test_audit_log_model(db):
    from app.models.audit_log import AuditLog
    log = AuditLog(
        action='TEST_ACTION',
        actor_type='SYSTEM',
        metadata={'test': True},
    )
    db.session.add(log)
    db.session.commit()
    assert log.id is not None
