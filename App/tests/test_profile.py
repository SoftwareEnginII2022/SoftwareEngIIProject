import os, tempfile, pytest, logging, unittest

from App.main import create_app
from App.database import create_db
from App.models import (
    User,
    Profile
)
from App.controllers import (
    create_user,
    create_profile,
    rate_profile,
    get_profile,
    get_top_ten,
    get_all_profiles,
)

from wsgi import app

LOGGER = logging.getLogger(__name__)

class ProfileUnitTests(unittest.TestCase):
    def test_new_profile(self):
        user = User("bob", "pass", "Bob","Marley")
        user.Profile = Profile(user.id)
        assert user.Profile.user_id == None
        assert user.Profile.rating == 0
        assert user.Profile.tier == 0
        assert user.Profile.daily_views == 0

    def test_profile_toJSON(self):
        user = User("bob", "pass", "Bob","Marley")
        user.Profile = Profile(user.id)
        profile_json = user.Profile.toJSON()
        expected_json = {
            'id': None,
            'user_id':None,
            'rating':0,
            'tier':'Bronze',
            'tier_points': 0,
            'daily_views':0,
            'pictures':[]
        }
        self.assertDictEqual(profile_json, expected_json)
    
    
class ProfileIntegrationTests(unittest.TestCase):
    @pytest.fixture(autouse=True, scope="class")
    def empty_db(self):
        app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
        create_db(app)
        yield app.test_client()
        os.unlink(os.getcwd()+'/App/test.db')
  
    def test_create_profile(self):
        user = create_user("bob", "pass","Bob","Marley")
        profile = create_profile(user.id)
        view_profile = get_profile(profile.id)
        assert profile.user_id == view_profile.user_id
        assert profile.rating == view_profile.rating
        assert profile.tier == view_profile.tier
        assert profile.daily_views == view_profile.daily_views
        assert view_profile.user_id == user.id
        
    def test_fetching_profiles(self):
        user = create_user("rick", "rickpass","Rick","Ricardo")
        profile = create_profile(user.id)

        profiles = get_all_profiles()
        profiles = [profile.toJSON() for profile in profiles]
        expected_list = [
            {
            'daily_views': 0,
            'id': 1,
            'pictures': [],
            'rating': 0,
            'tier': 'Bronze',
            'tier_points': 0,
            'user_id': 1
            },
            {
            'daily_views': 0,
            'id': 2,
            'pictures': [],
            'rating': 0,
            'tier': 'Bronze',
            'tier_points': 0,
            'user_id': 2
            }
        ]

        self.assertListEqual(expected_list, profiles)
        
    def test_rank_profile(self):
        user = create_user("steve", "stevepass","Steve","Stevenson")
        profile = create_profile(user.id)
        rating = rate_profile(profile.id, user.id, 5)
        view_profile = get_profile(profile.id)
        assert view_profile.rating == 5

    def test_retrieve_top_ten(self):
        user = create_user("paul", "paulpass","Paul","Pauloole")
        profile = create_profile(user.id)
        top_ten = get_top_ten()
        top_ten = [p.toJSON() for p in top_ten]
        expected_list = [
            {
            'daily_views': 0,
            'id': 3,
            'pictures': [],
            'rating': 5,
            'tier': 'Bronze',
            'tier_points': 5,
            'user_id': 3
            },
            {
            'daily_views': 0,
            'id': 1,
            'pictures': [],
            'rating': 0,
            'tier': 'Bronze',
            'tier_points': 0,
            'user_id': 1
            },
            {
            'daily_views': 0,
            'id': 2,
            'pictures': [],
            'rating': 0,
            'tier': 'Bronze',
            'tier_points': 0,
            'user_id': 2
            },
            {
            'daily_views': 0,
            'id': 4,
            'pictures': [],
            'rating': 0,
            'tier': 'Bronze',
            'tier_points': 0,
            'user_id': 4
            }
        ]
            
        self.assertListEqual(expected_list, top_ten)
    
