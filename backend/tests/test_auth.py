import json


def test_register(client, db):
    res = client.post('/api/auth/register', json={
        'name': 'New User',
        'email': 'new@test.com',
        'password': 'NewPass123!',
        'confirm_password': 'NewPass123!'
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data['success'] is True
    assert data['data']['email'] == 'new@test.com'


def test_register_duplicate_email(client, sample_user):
    res = client.post('/api/auth/register', json={
        'name': 'Duplicate',
        'email': 'student@test.com',
        'password': 'Pass123!',
        'confirm_password': 'Pass123!'
    })
    assert res.status_code == 422


def test_register_password_mismatch(client):
    res = client.post('/api/auth/register', json={
        'name': 'Test',
        'email': 'test@test.com',
        'password': 'Pass123!',
        'confirm_password': 'Different123!'
    })
    assert res.status_code == 422


def test_login_success(client, sample_user):
    res = client.post('/api/auth/login', json={
        'email': 'student@test.com',
        'password': 'TestPass123!'
    })
    assert res.status_code == 200
    data = res.get_json()
    assert 'access_token' in data['data']
    assert 'refresh_token' in data['data']


def test_login_invalid_credentials(client, sample_user):
    res = client.post('/api/auth/login', json={
        'email': 'student@test.com',
        'password': 'WrongPassword'
    })
    assert res.status_code == 401


def test_login_nonexistent_user(client, db):
    # Clear any existing users to ensure clean test
    from app.models.user import User
    User.query.delete()
    db.session.commit()
    res = client.post('/api/auth/login', json={
        'email': 'nonexistent@test.com',
        'password': 'Password123!'
    })
    assert res.status_code == 401


def test_me_authenticated(client, auth_headers):
    res = client.get('/api/auth/me', headers=auth_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data['data']['email'] == 'student@test.com'


def test_me_unauthenticated(client):
    res = client.get('/api/auth/me')
    assert res.status_code == 401


def test_refresh_token(client, sample_user):
    login_res = client.post('/api/auth/login', json={
        'email': 'student@test.com',
        'password': 'TestPass123!'
    })
    refresh_token = login_res.get_json()['data']['refresh_token']
    res = client.post('/api/auth/refresh', headers={
        'Authorization': f'Bearer {refresh_token}'
    })
    assert res.status_code == 200
    assert 'access_token' in res.get_json()['data']


def test_change_password(client, auth_headers):
    res = client.post('/api/auth/change-password', json={
        'current_password': 'TestPass123!',
        'new_password': 'NewPassword1!'
    }, headers=auth_headers)
    assert res.status_code == 200


def test_change_password_wrong_current(client, auth_headers):
    res = client.post('/api/auth/change-password', json={
        'current_password': 'WrongPassword',
        'new_password': 'NewPassword1!'
    }, headers=auth_headers)
    assert res.status_code == 400
