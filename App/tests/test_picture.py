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

class PictureUnitTest(unittest.TestCase):
    def test_new_picture(self):
        new_picture = Picture('1','1','https://i.imgur.com/YsItLyD.jpeg')
        assert (
            new_picture.user_id == 1 and new_picture.profile_id == 1 
            and new_picture.url == 'https://i.imgur.com/YsItLyD.jpeg' 
            and new_picture.likes == 0, new_picture.dislikes == 0 
        )
    def test_picture_toJSON(self):
       new_picture = Picture('1','1','https://i.imgur.com/YsItLyD.jpeg')
       expected_json = {
                'id': None,
                'url':'https://i.imgur.com/YsItLyD.jpeg',
                'dislikes':0,
                'likes':0,
                'profile_id': 1,
                'user_id':1
            }
    
class PictureIntegrationTests(unittest.TestCase):
    @pytest.fixture(autouse=True, scope="class")
    def empty_db(self):
        app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
        create_db(app)
        yield app.test_client()
        os.unlink(os.getcwd()+'/App/test.db')

    def test_upload_picture(self):
        user = create_user("rick", "rickpass","rick","ricardo")
        profile = create_profile(user.id)
        picture = upload_picture(user.id,profile.id,'https://i.imgur.com/YsItLyD.jpeg')
        picture_json = picture.toJSON()
        self.assertDictEqual({'id':3,'user_id':3, 'profile_id':3,'url':'https://i.imgur.com/YsItLyD.jpeg','likes': 0, 'dislikes': 0}, picture_json)


    def test_like_picture(self):
        user = create_user("bob", "bobpass","bob","bobbert")
        profile = create_profile(user.id)
        picture = upload_picture(user.id,profile.id,'https://i.imgur.com/YsItLyD.jpeg')
        picture = like_picture(picture.id, user.id)
        picture_json = picture.toJSON()
        self.assertDictEqual({'id':2,'user_id':2, 'profile_id':2,'url':'https://i.imgur.com/YsItLyD.jpeg', \
        'likes': 1, 'dislikes': 0}, picture_json)
    
    def test_dislike_picture(self):
        user = create_user("aaron", "aaronpass","aa","ron")
        profile = create_profile(user.id)
        picture = upload_picture(user.id,profile.id,'https://i.imgur.com/YsItLyD.jpeg')
        picture = dislike_picture(picture.id, user.id)
        picture_json = picture.toJSON()
        self.assertDictEqual({'id':1,'user_id':1, 'profile_id':1,'url':'https://i.imgur.com/YsItLyD.jpeg', \
        'likes': 0, 'dislikes': 1}, picture_json)