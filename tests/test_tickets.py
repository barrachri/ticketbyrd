import json

def test_invalid_ticket(client):
    data = {
        "name": 2,
        "email": 2,
        "subject": 3,
        "type": "helloThere",
        "message": "ciao"
    }

    response = client.post(
        '/api/tickets',
        data=json.dumps(data),
        content_type='application/json'
        )
    assert response.status_code == 400

def test_empty_ticket(client):
    response = client.post(
        '/api/tickets',
        data=json.dumps({}),
        content_type='application/json'
        )
    assert response.status_code == 400

def test_new_ticket(client):
    data = {
        "name": "Christian",
        "email": "my@email.com",
        "subject": "why is not working?",
        "type": "Bug",
        "urgency": "Low",
        "message": "ciao"
    }
    response = client.post(
        '/api/tickets',
        data=json.dumps(data),
        content_type='application/json'
        )
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "id" in data['ticket']

def test_update_ticket(client, valid_jwt):
    headers = {'Authorization': 'Bearer %s' % valid_jwt}
    data = {
        "name": "Christian",
        "email": "my@email.com",
        "subject": "why is not working?",
        "type": "Bug",
        "urgency": "Low",
        "message": "ciao"
    }
    response = client.post(
        '/api/tickets',
        data=json.dumps(data),
        content_type='application/json'
        )
    data = json.loads(response.data)

    uri = '/api/tickets/%d' % data['ticket']['id']
    data = {
        "urgency": "High",
    }
    response = client.put(
        uri,
        headers=headers,
        data=json.dumps(data),
        content_type='application/json'
        )
    assert response.status_code == 200
    response = client.get(
        uri,
        headers=headers
    )
    assert response.status_code == 200
    assert "High" in data['urgency']

def test_get_tickets(client, valid_jwt):
    headers = {'Authorization': 'Bearer %s' % valid_jwt}
    response = client.get('/api/tickets', headers=headers)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "tickets" in data
    assert len(data['tickets']) > 0

def test_get_ticket(client, valid_jwt):
    headers = {'Authorization': 'Bearer %s' % valid_jwt}
    response = client.get('/api/tickets/1', headers=headers)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "message" in data['ticket']

def test_get_jwt(client):
    data = {
        "email": "Christian",
        "password": "my@email.com",
    }
    response = client.post(
        '/api/login',
        data=json.dumps(data),
        content_type='application/json'
        )
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "token" in data['user']
