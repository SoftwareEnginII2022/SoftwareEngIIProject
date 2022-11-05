import os, tempfile, pytest, logging, unittest

from App.main import create_app
from App.database import create_db
from App.models import (
    Picture
)
from App.controllers import (
    create_user,
    create_profile,
    upload_picture,
    get_picture,
    like_picture,
    dislike_picture
)

from wsgi import app

LOGGER = logging.getLogger(__name__)

class PictureUnitTests(unittest.TestCase):
    def test_new_picture(self):
        new_picture = Picture(1, 1, 'https://i.imgur.com/YsItLyD.jpeg')
        assert new_picture.user_id == 1
        assert new_picture.profile_id == 1 
        assert new_picture.url == 'https://i.imgur.com/YsItLyD.jpeg' 
        assert new_picture.likes == 0
        assert new_picture.dislikes == 0


    def test_picture_toJSON(self):
        new_picture = Picture(1, 1, 'https://i.imgur.com/YsItLyD.jpeg')
        expected_json = {
            'id': None,
            'user_id':1,
            'profile_id': 1,
            'url': 'https://i.imgur.com/YsItLyD.jpeg',
            'likes':0,
            'dislikes':0
        }
    
class PictureIntegrationTests(unittest.TestCase):
    @pytest.fixture(autouse=True, scope="class")
    def empty_db(self):
        app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
        create_db(app)
        yield app.test_client()
        os.unlink(os.getcwd()+'/App/test.db')

    def test_add_picture(self):
        user = create_user("bob", "pass","Bob","Marley")
        profile = create_profile(user.id)
        picture = upload_picture(user.id, profile.id, 'https://i.imgur.com/YsItLyD.jpeg')
        view_picture = get_picture(picture.id)
        picture_json = view_picture.toJSON()
        expected_dict = {
            'id': 1,
            'user_id': 1,
            'profile_id': 1,
            'url':'https://i.imgur.com/YsItLyD.jpeg',
            'likes': 0,
            'dislikes': 0
        }

        self.assertDictEqual(expected_dict, picture_json)
    
    def test_dislike_picture(self):
        picture = dislike_picture(1, 1)
        view_picture = get_picture(picture.id)
        picture_json = view_picture.toJSON()
        expected_dict = {
            'id': 1,
            'user_id': 1,
            'profile_id': 1,
            'url':'https://i.imgur.com/YsItLyD.jpeg',
            'likes': 0,
            'dislikes': 1
        }

        self.assertDictEqual(expected_dict, picture_json)

    def test_like_picture(self):
        picture = like_picture(1, 1)
        view_picture = get_picture(picture.id)
        picture_json = view_picture.toJSON()
        expected_dict = {
            'id': 1,
            'user_id': 1,
            'profile_id': 1,
            'url':'https://i.imgur.com/YsItLyD.jpeg',
            'likes': 1,
            'dislikes': 0
        }

        self.assertDictEqual(expected_dict, picture_json)