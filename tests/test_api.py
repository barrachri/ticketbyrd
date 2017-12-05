import json

def test_new_invalid_ticket(client):
    data = {
        "name": 2,
        "email": 2,
        "subject": 3,
        "type": "helloThere",
        "message": "ciao"
    }

    response = client.post(
        '/tickets',
        data=json.dumps(data),
        content_type='application/json'
        )
    assert response.status_code == 400

def test_new_empty_ticket(client):
    response = client.post(
        '/tickets',
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
        '/tickets',
        data=json.dumps(data),
        content_type='application/json'
        )
    assert response.status_code == 200

def test_get_ticket(client):
    response = client.get('/tickets/0')
    assert response.status_code == 200

def test_get_comments(client):
    response = client.get('/comments/0')
    assert response.status_code == 200

def test_new_add_comment(client):
    data = {
        "message": "Can you resolve this asap?",
    }
    response = client.post(
        '/comments/0',
        data=json.dumps(data),
        content_type='application/json'
        )
    assert response.status_code == 200
