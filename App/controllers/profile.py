from App.models import Profile
import sqlalchemy 
from sqlalchemy.exc import SQLAlchemyError
from App.database import db

def get_all_profiles():
    profiles = Profile.query.all()
    if not profiles:
        return []
    return profiles

def get_all_profiles_JSON():
    profiles = get_all_profiles()
    if not profiles:
        return []
    profiles = [profile.toJSON() for profile in profiles]
    return profiles

def get_profile(id):
    profile = Profile.query.filter_by(id = id).first()
    if not profile:
        return []
    return profile

def get_profile_JSON(id):
    profile = get_profile(id)
    if not profile:
        return []
    return profile.toJSON()

def create_profile(user_id,rating,tier,view_count,first_view_date):
        newProfile = Profile(user_id,rating,tier,view_count,first_view_date)
        db.session.add(newProfile)
        db.session.commit()
        return newProfile
    
     

def rate_profile(profile_id, rating):
    profile = get_profile(profile_id)
    if not profile:
        return []
    try:
        profile.rating = profile.rating + rating
        db.session.add(profile)
        db.commit()
        return profile
    except sqlalchemy.exc.SQLAlchemyError:
        db.session.rollback()
        return []

    