def test_process_request(client, auth_headers):
    # Create a request
    create_res = client.post('/api/requests', json={
        'title': 'Broken Water Cooler',
        'description': 'The water cooler near Block B has not worked for 3 days.',
        'category': 'Maintenance',
        'priority': 'HIGH'
    }, headers=auth_headers)
    req_id = create_res.get_json()['data']['id']

    # Process through AI workflow
    res = client.post(f'/api/requests/{req_id}/process', headers=auth_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert 'category' in data['data']
    assert 'priority' in data['data']


def test_workflow_created(client, auth_headers):
    create_res = client.post('/api/requests', json={
        'title': 'Workflow Test',
        'description': 'Test workflow creation',
        'category': 'IT Support'
    }, headers=auth_headers)
    req_id = create_res.get_json()['data']['id']

    res = client.get(f'/api/requests/{req_id}', headers=auth_headers)
    data = res.get_json()['data']
    assert 'workflow' in data
    assert data['workflow']['state'] == 'INTAKE'


def test_list_workflows(client, admin_headers):
    res = client.get('/api/workflows', headers=admin_headers)
    assert res.status_code == 200


def test_agent_status(client, admin_headers):
    res = client.get('/api/agents/status', headers=admin_headers)
    assert res.status_code == 200
    data = res.get_json()['data']
    assert len(data) > 0
