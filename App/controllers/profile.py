from App.models import Profile
import sqlalchemy 
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.expression import func
from App.database import db
from datetime import date

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

def get_top_ten():
    profiles = Profile.query.order_by(Profile.rating.desc()).limit(10)
    if not profiles:
        return []
    return profiles

def create_profile(user_id):
    profile = Profile(user_id)
    db.session.add(profile)
    db.session.commit()
    return profile
    
def rate_profile(profile_id, rating):
    profile = get_profile(profile_id)
    if not profile:
        return []
    try:
        profile.rating = profile.rating + rating
        db.session.add(profile)
        db.session.commit()
        return profile
    except sqlalchemy.exc.SQLAlchemyError:
        db.session.rollback()
        return []

tiers_max_views = (7, 14, 21, 28)

def browse_viewable_profiles():
    '''
    step 1:
        obtain randomized columns from database

    step 2:
        loop through each

    step 3:
        if view_date > 24hrs:
            choose it and view count = 1;
        else
            if view_count <= max_view_tier:
                choose it and view count += 1;
    '''

    # 1
    profiles = Profile.query.order_by(func.random())

    # 2
    counter = 0
    counted = 7
    result = []

    for profile in profiles:
        now = date.today()
        first_viewed_delta = now - profile.first_view_date
        if first_viewed_delta.days >= 1:            
            try:
                profile.view_count = 1
                profile.first_view_date = now
                result.append(profile)
                counter = counter + 1
                db.session.add(profile)
                db.session.commit()
            except sqlalchemy.exc.SQLAlchemyError:
                db.session.rollback()
        else:
            if profile.view_count < tiers_max_views[profile.tier]:  
                try:
                    profile.view_count = profile.view_count + 1
                    result.append(profile)
                    counter = counter + 1
                    db.session.add(profile)
                    db.session.commit()
                except sqlalchemy.exc.SQLAlchemyError:
                    db.session.rollback()
        
        if counter >= counted:
            break

    return result