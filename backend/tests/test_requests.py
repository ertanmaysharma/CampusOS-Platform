def test_create_request(client, auth_headers):
    res = client.post('/api/requests', json={
        'title': 'Test Request',
        'description': 'This is a test request description',
        'category': 'Maintenance',
        'priority': 'MEDIUM'
    }, headers=auth_headers)
    assert res.status_code == 201
    data = res.get_json()
    assert data['success'] is True
    assert data['data']['title'] == 'Test Request'
    assert 'request_number' in data['data']


def test_create_request_validation(client, auth_headers):
    res = client.post('/api/requests', json={
        'title': '',
        'description': ''
    }, headers=auth_headers)
    assert res.status_code == 422


def test_create_request_unauthenticated(client):
    res = client.post('/api/requests', json={
        'title': 'Test',
        'description': 'Test'
    })
    assert res.status_code == 401


def test_list_requests(client, auth_headers, sample_user):
    # Create a request first
    client.post('/api/requests', json={
        'title': 'List Test',
        'description': 'Test description',
        'category': 'IT Support'
    }, headers=auth_headers)

    res = client.get('/api/requests', headers=auth_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert 'items' in data['data']
    assert data['data']['total'] >= 1


def test_get_request(client, auth_headers):
    create_res = client.post('/api/requests', json={
        'title': 'Get Test',
        'description': 'Test description',
        'category': 'Finance'
    }, headers=auth_headers)
    req_id = create_res.get_json()['data']['id']

    res = client.get(f'/api/requests/{req_id}', headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()['data']['title'] == 'Get Test'


def test_get_request_not_found(client, auth_headers):
    res = client.get('/api/requests/99999', headers=auth_headers)
    assert res.status_code == 404


def test_update_request(client, auth_headers):
    create_res = client.post('/api/requests', json={
        'title': 'Update Test',
        'description': 'Original',
        'category': 'Maintenance'
    }, headers=auth_headers)
    req_id = create_res.get_json()['data']['id']

    res = client.patch(f'/api/requests/{req_id}', json={
        'title': 'Updated Title'
    }, headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()['data']['title'] == 'Updated Title'


def test_cancel_request(client, auth_headers):
    create_res = client.post('/api/requests', json={
        'title': 'Cancel Test',
        'description': 'To be cancelled',
        'category': 'Other'
    }, headers=auth_headers)
    req_id = create_res.get_json()['data']['id']

    res = client.delete(f'/api/requests/{req_id}', headers=auth_headers)
    assert res.status_code == 200


def test_request_filters(client, auth_headers):
    client.post('/api/requests', json={
        'title': 'Filter Test',
        'description': 'Test',
        'category': 'Hostel'
    }, headers=auth_headers)

    res = client.get('/api/requests?category=Hostel', headers=auth_headers)
    assert res.status_code == 200
