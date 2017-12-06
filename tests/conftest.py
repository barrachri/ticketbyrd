import pytest
from app import app
from ticketbyrd import models, schema
from factory import db
import json


@pytest.fixture(scope='module')
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    db.create_all(app=app)
    new_ticket = {
        "name": "Christian",
        "email": "my@email.com",
        "subject": "why is not working?",
        "type": "Bug",
        "urgency": "Low",
        "message": "ciao"
    }
    new_comment = {
        "message": "Thanks for your message this should be resolved."
    }
    ticket_schema, err = schema.Ticket().load(new_ticket)
    with app.app_context():
        ticket = models.Ticket(**ticket_schema)
        comment = models.Comment(**new_comment)
        ticket.comments.append(comment)
        db.session.add(ticket)
        db.session.commit()

    with app.test_client() as c:
        yield c

@pytest.fixture(scope='module')
def valid_jwt(client):
    """Generate a valid jwt token to use during the tests."""
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
    yield data['user']['token']
