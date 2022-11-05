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
    get_all_profiles_JSON,
)

from wsgi import app

LOGGER = logging.getLogger(__name__)

class ProfileUnitTest(unittest.TestCase):
    def test_new_profile(self):
        user = User("bob", "bobpass","bob","bobbert")
        user.Profile = Profile(user.id)
        assert (
            user.Profile.user_id == None and user.Profile.rating == 0
            and user.Profile.tier == 0 and user.Profile.daily_views == 0
        )

    def test_profile_toJSON(self):
        user = User("bob", "bobpass","bob","bobbert")
        user.Profile = Profile(user.id)
        profile_json = user.Profile.toJSON()
        expected_json = {
                'daily_views':0,
                'id': None,
                'pictures':[],
                'rating':0,
                'tier':'Bronze',
                'tier_points': 0,
                'user_id':None
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
        user = create_user("bob", "bobpass","bob","bobbert")
        profile = create_profile(user.id)
        assert profile.user_id == 1 and profile.rating == 0 and profile.tier == 0 
        
    def test_display_view_profile(self):
        user = create_user("rick", "rickpass","rick","ricardo")
        profile = create_profile(user.id)
        view_profile = get_profile(user.id)
        self.assertDictEqual({'id':2, 'user_id':2, 'rating':0,'tier':'Bronze','tier_points':0,'daily_views':0,'pictures':[] },view_profile.toJSON())

    def test_rank_profile(self):
        user = create_user("amit", "amitpass","amit","amit")
        profile = create_profile(user.id)
        rating = rate_profile(profile.id,user.id,5)
        view_profile = get_profile(user.id)
        assert view_profile.rating == 5
        
    def test_exploring_profiles(self):
        explore_profile = get_all_profiles_JSON()
        expected_list= [
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
            }]

        self.assertListEqual(expected_list ,explore_profile)

    def test_get_top_ten(self):
        user = create_user("paul", "paulpass","paul","pauloole")
        profile = create_profile(user.id)
        top_ten = get_top_ten()
        top_ten = [p.toJSON() for p in top_ten]
        expected_list = [{
            'daily_views': 0,
            'id': 1,
            'pictures': [],
            'rating': 0,
            'tier': 'Bronze',
            'tier_points': 0,
            'user_id': 1},
        {
            'daily_views': 0,
            'id': 2,
            'pictures': [],
            'rating': 0,
            'tier': 'Bronze',
            'tier_points': 0,
            'user_id': 2},
        {
            'daily_views': 0,
            'id': 3,
            'pictures': [],
            'rating': 0,
            'tier': 'Bronze',
            'tier_points': 0,
            'user_id': 3}]
            
        self.assertListEqual(expected_list ,top_ten)
    
