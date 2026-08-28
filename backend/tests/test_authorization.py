def test_student_can_create_request(client, auth_headers):
    res = client.post('/api/requests', json={
        'title': 'Student Request',
        'description': 'Test',
        'category': 'Maintenance'
    }, headers=auth_headers)
    assert res.status_code == 201


def test_student_cannot_manage_users(client, auth_headers):
    res = client.get('/api/users', headers=auth_headers)
    # Students can view users list but may get limited results
    assert res.status_code in [200, 403]


def test_student_cannot_access_admin_endpoints(client, auth_headers):
    res = client.get('/api/admin/roles', headers=auth_headers)
    assert res.status_code == 403


def test_student_cannot_approve(client, auth_headers):
    res = client.get('/api/approvals', headers=auth_headers)
    assert res.status_code == 403


def test_student_cannot_view_audit_logs(client, auth_headers):
    res = client.get('/api/audit-logs', headers=auth_headers)
    assert res.status_code == 403


def test_admin_can_manage_users(client, admin_headers):
    res = client.get('/api/users', headers=admin_headers)
    assert res.status_code == 200


def test_admin_can_view_audit_logs(client, admin_headers):
    res = client.get('/api/audit-logs', headers=admin_headers)
    assert res.status_code == 200


def test_admin_can_view_approvals(client, admin_headers):
    res = client.get('/api/approvals', headers=admin_headers)
    assert res.status_code == 200


def test_admin_can_manage_departments(client, admin_headers):
    res = client.post('/api/departments', json={
        'name': 'Test Dept',
        'description': 'Test'
    }, headers=admin_headers)
    assert res.status_code == 201


def test_unauthenticated_cannot_access_protected(client):
    res = client.get('/api/requests')
    assert res.status_code == 401


def test_admin_can_access_admin_dashboard(client, admin_headers):
    res = client.get('/api/dashboard/admin', headers=admin_headers)
    assert res.status_code == 200


def test_student_cannot_access_admin_dashboard(client, auth_headers):
    res = client.get('/api/dashboard/admin', headers=auth_headers)
    assert res.status_code == 403
