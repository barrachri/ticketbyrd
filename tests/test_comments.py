import json


def test_get_comments(client, valid_jwt):
    headers = {'Authorization': 'Bearer %s' % valid_jwt}
    response = client.get('/api/tickets/1/comments', headers=headers)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "comments" in data
    assert len(data['comments']) > 0

def test_new_add_comment(client, valid_jwt):
    headers = {'Authorization': 'Bearer %s' % valid_jwt}
    response = client.get('/api/tickets/1', headers=headers)
    data = {
        "message": "Can you resolve this asap?",
    }
    response = client.post(
        '/api/tickets/1/comments',
        data=json.dumps(data),
        headers=headers,
        content_type='application/json'
        )
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "id" in data['comment']

