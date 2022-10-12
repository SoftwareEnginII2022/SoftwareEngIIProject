from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required, current_identity

from App.controllers import (
 upload_picture,
 get_picture,
 like_picture,
 dislike_picture,
)

picture_views = Blueprint('picture_views',__name__,template_folder='../templates')

@picture_views.route('/picture/view/<int:id>', methods=['GET'])
def retrieve_picture(id):
    picture = get_picture(id)
    if not picture:
        return jsonify({'Message':'Picture was not found'}),404
    return picture.toJSON()

@picture_views.route('/picture/like/<int:id>', methods=['POST'])
@jwt_required()
def like_picture_action(id):
    picture = like_picture(id,current_identity.id)
    if not picture:
        return jsonify({"Message":"Picture was not found "}),404
    return jsonify({'picture': picture.toJSON()}),200

@picture_views.route('/picture/dislike/<int:id>', methods=['POST'])
@jwt_required()
def dislike_picture_action(id):
    picture = dislike_picture(id,current_identity.id)
    if not picture:
        return jsonify({"Message":"Picture was not found "}),404
    return jsonify({'picture': picture.toJSON()}),200
    
@picture_views.route('/picture/upload', methods=['POST'])
@jwt_required()
def upload_picture_action():
    picture_url = request.json.get('picture_url')
    picture = upload_picture(user_id = current_identity.id, profile_id =current_identity.id, url = picture_url)

    if not picture:
        return jsonify({'Message':'An error has occured'}), 400
    return jsonify({'picture':picture.toJSON()}), 201



    


