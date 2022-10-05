from flask import Blueprint, request, jsonify 
from flask_jwt import jwt_required,current_identity

from  App.controllers import (
    get_profile,
    rate_profile,
)
profile_views = Blueprint('profile_views', __name__, template_folder='../template' )

@profile_views.route('/profile/view/<id>',methods=['GET'])
def view_profile(id):
    user = get_profile(id)
    if user  is []:
        return jsonify({'Message':'User does not exist'},404)
    return jsonify({'user':User}, 200)

@profile_views.route('/profile/<id>/rate',methods=['POST'])
@jwt_required()
def rank_profile(id):
    ranking = request.json.get('ranking')
    profile = rate_profile(id,ranking)
    if profile is []:
        return jsonify({'message':'User does not exist'},404)
    return jsonify({'message':'sucess'},200)

