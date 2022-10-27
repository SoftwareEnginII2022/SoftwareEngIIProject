from flask import Blueprint, request, jsonify 
from flask_jwt import jwt_required,current_identity

from  App.controllers import (
    get_profile,
    get_profile_by_username,
    rate_profile,
    get_top_ten,
    browse_viewable_profiles
)

profile_views = Blueprint('profile_views', __name__, template_folder='../template' )

# @profile_views.route('/profile/view/<int:id>',methods=['GET'])
# def view_profile(id):
#     profile = get_profile(id)
#     if not profile:
#         return jsonify({'message':'Profile does not exist'}), 404
#     return jsonify({'profile':profile.toJSON()}), 200

@profile_views.route('/profile/view/<string:username>',methods=['GET'])
def view_profile(username):
    profile = get_profile_by_username(username)
    if not profile:
        return jsonify({'message':'Profile does not exist'}), 404
    return jsonify({'profile':profile.toJSON()}), 200

@profile_views.route('/profile/rate/<int:id>',methods=['POST'])
@jwt_required()
def rank_profile(id):
    ranking = request.json.get('ranking')
    if ranking > 5 or ranking < 0:
        return jsonify({'message': 'Invalid ranking'}), 400
    profile = rate_profile(id,current_identity.id,ranking)
    if not profile:
        return jsonify({'message':'Profile does not exist'}), 404
    return jsonify({'message':'success'}), 200

@profile_views.route('/profile/popular', methods=['GET'])
def view_top_ten():
    profiles = get_top_ten()
    if not profiles:
        return jsonify({'message': 'No popular profiles available. Rate some today!'}), 200
    profiles = [profile.toJSON() for profile in profiles]
    return jsonify({"profiles":profiles}), 200

@profile_views.route('/profile/explore', methods=['GET'])
@jwt_required()
def explore_profiles():
    profiles = browse_viewable_profiles()

    if not profiles:
        return jsonify({'message': 'No profiles available at this time. Come back later.'}), 200
    profiles = [profile.toJSON() for profile in profiles]
    return jsonify({"profiles":profiles}), 200