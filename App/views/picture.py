from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required, current_identity

from App.controllers import (
 upload_Picture,
 get_Picture,
 likePicture
)

picture_views = Blueprint('picture_views',__name__,template_folder='../templates')

@picture_views.route('/picture/view/<int:id>', methods=['GET'])
def retrieve_picture(id):
    picture = get_Picture(id)
    if not picture:
        return jsonify({'Message':'Image not found'},404)
    return picture.toJSON()

@picture_views.route('/picture/view/<int:id>/like', methods=['POST'])
@jwt_required()
def like_picture(id):
    picture = like_Picture(id,current_identity.id)
    if picture is []:
        return jsonify({"Message":"Picture was not found "},404)
    return jsonify({'picture': picture.toJSON()},200)
    
@picture_views.route('/picture/upload', methods=['POST'])
@jwt_required()
def upload_picture():
    profile_id = request.json.get('profile_id')
    url = request.json.get('url')
    picture = upload_Picture(user_id = 1,profile_id =1, url = url, likes= 0, dislikes= 0)

    if picture is []:
        return jsonify({'Message':'An error has occured'}, 400)
    return jsonify({'picture':picture.toJSON()}, 201)



    


