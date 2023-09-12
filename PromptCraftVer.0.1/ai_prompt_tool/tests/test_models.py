## tests/test_models.py
import pytest
from app.models import User, Document, Commit
from app import db, bcrypt

@pytest.fixture(scope='module')
def new_user():
    user = User(username='testuser', email='testuser@test.com', password='testpassword')
    return user

def setup_module(module):
    db.create_all()

def teardown_module(module):
    db.session.remove()
    db.drop_all()

def test_user_model(new_user):
    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # Retrieve the user
    user = User.query.filter_by(username='testuser').first()

    # Check if the user was created correctly
    assert user is not None
    assert user.username == 'testuser'
    assert user.email == 'testuser@test.com'
    assert bcrypt.check_password_hash(user.password_hash, 'testpassword')

def test_document_model(new_user):
    # Create a new document
    new_document = Document(title='test document', content='this is a test document', owner=new_user)
    db.session.add(new_document)
    db.session.commit()

    # Retrieve the document
    document = Document.query.filter_by(title='test document').first()

    # Check if the document was created correctly
    assert document is not None
    assert document.title == 'test document'
    assert document.content == 'this is a test document'
    assert document.user_id == new_user.id

def test_commit_model(new_user):
    # Create a new commit
    document = Document.query.filter_by(title='test document').first()
    new_commit = Commit(message='initial commit', document=document)
    db.session.add(new_commit)
    db.session.commit()

    # Retrieve the commit
    commit = Commit.query.filter_by(message='initial commit').first()

    # Check if the commit was created correctly
    assert commit is not None
    assert commit.message == 'initial commit'
    assert commit.document_id == document.id
