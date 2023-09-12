## tests/test_routes.py
import pytest
from flask import url_for
from app import app, db
from app.models import User, Document

@pytest.fixture(scope='module')
def test_client():
    with app.test_client() as test_client:
        with app.app_context():
            yield test_client

@pytest.fixture(scope='module')
def init_database():
    db.create_all()
    user1 = User(username='testuser1', email='testuser1@test.com', password='testpassword1')
    user2 = User(username='testuser2', email='testuser2@test.com', password='testpassword2')
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    yield db

    db.drop_all()

def login(test_client, username, password):
    return test_client.post('/login', data=dict(username=username, password=password), follow_redirects=True)

def logout(test_client):
    return test_client.get('/logout', follow_redirects=True)

def test_register(test_client, init_database):
    response = test_client.post('/register', data=dict(username='testuser3', email='testuser3@test.com', password='testpassword3', confirm_password='testpassword3'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Your account has been created! You are now able to log in' in response.data

def test_login_logout(test_client, init_database):
    response = login(test_client, 'testuser1', 'testpassword1')
    assert response.status_code == 200
    assert b'Logged in successfully.' in response.data

    response = logout(test_client)
    assert response.status_code == 200
    assert b'You have been logged out.' in response.data

def test_create_document(test_client, init_database):
    login(test_client, 'testuser1', 'testpassword1')
    response = test_client.post('/document', data=dict(title='test document', content='this is a test document'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Document created successfully' in response.data

def test_get_document(test_client, init_database):
    login(test_client, 'testuser1', 'testpassword1')
    response = test_client.get('/document?title=test document', follow_redirects=True)
    assert response.status_code == 200
    assert b'test document' in response.data
    assert b'this is a test document' in response.data

def test_update_document(test_client, init_database):
    login(test_client, 'testuser1', 'testpassword1')
    response = test_client.put('/document', data=dict(title='test document', new_content='this is an updated test document'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Document updated successfully' in response.data

def test_delete_document(test_client, init_database):
    login(test_client, 'testuser1', 'testpassword1')
    response = test_client.delete('/document?title=test document', follow_redirects=True)
    assert response.status_code == 200
    assert b'Document deleted successfully' in response.data
