import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import create_db
from App.models import User, Profile
from App.controllers import (
    get_user,
    create_user,
    create_profile,
    get_all_users_json,
)

from wsgi import app

LOGGER = logging.getLogger(__name__)



'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        newuser = User("bob", "pass","Bob","Marley")
        assert newuser.username == "bob"
        assert newuser.first_name == "Bob"
        assert newuser.last_name == "Marley"

    def test_toJSON(self):
        user = User("bob", "pass","Bob","Marley")
        user.Profile = Profile(user.id)
        user_json = user.toJSON()
        expected_json = {
            'id':None, 
            'username':'bob',
            'first_name':'Bob', 
            'last_name':'Marley',
            'profile':{
                'id': None,
                'user_id':None,
                'rating':0,
                'tier':'Bronze',
                'tier_points': 0,
                'daily_views':0,
                'pictures':[]
            }
        }
        self.assertDictEqual(user_json, expected_json)
    
    def test_hashed_password(self):
        password = "pass"
        hashed = generate_password_hash(password, method='sha256')
        newuser = User("bob", password,"bob","bobbert")
        assert newuser.password != password

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
        user = create_user("bob", "pass","Bob","Marley")
        create_profile(user.id)
        view_user = get_user(user.id)
        assert user.username == view_user.username
        assert user.first_name == view_user.first_name
        assert user.last_name == view_user.last_name
    
    def test_get_all_users_json(self):
        user = create_user("rick", "rickpass","Rick","Ricarado")
        create_profile(user.id)
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob","first_name":"Bob", "last_name":"Marley","profile":{'id':1, 'user_id':1, 'rating':0, 'tier':'Bronze', 'tier_points':0, 'daily_views':0,'pictures':[]}}, {"id":2, "username":"rick","first_name":"Rick", "last_name":"Ricarado","profile":{'id':2, 'user_id':2, 'rating':0, 'tier':'Bronze', 'tier_points':0, 'daily_views':0,'pictures':[]}}], users_json)


