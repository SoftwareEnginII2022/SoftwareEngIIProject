import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import create_db
from App.models import User
from App.controllers import (
    create_user,
    get_all_users_json,
    profile
)

from wsgi import app

LOGGER = logging.getLogger(__name__)



'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass","bob","bobbert")
        assert user.username == "bob"

    def test_toJSON(self):
        user = User("bob", "bobpass","bob","bobbert")
        user_json = user.toJSON()
        self.assertDictEqual(user_json, {"id":None, "username":"bob","first_name":"bob", "last_name":"bobbert","profile":[]})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password,"bob","bobbert")
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password,"bob","bobbert")
        assert user.check_password(password)

'''
    Integration Tests
'''



class UserIntegrationTests(unittest.TestCase):

    # This fixture creates an empty database for the test and deletes it after the test
    # scope="class" would execute the fixture once and resued for all methods in the class
    @pytest.fixture(autouse=True, scope="class")
    def empty_db(self):
        app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
        create_db(app)
        yield app.test_client()
        os.unlink(os.getcwd()+'/App/test.db')

    def test_create_user(self):
        user = create_user("bob", "bobpass","bob","bobbert")
        assert user.username == "bob"
    
    def test_get_all_users_json(self):
        create_user("rick", "rickpass","rick","ricarado")
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob","first_name":"bob", "last_name":"bobbert","profile":[]}, {"id":2, "username":"rick","first_name":"rick", "last_name":"ricarado","profile":[]}], users_json)


