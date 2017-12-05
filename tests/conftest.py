import pytest
from ticketbyrd.main import app



@pytest.fixture(scope='module')
def client():
    with app.test_client() as c:
        yield c
