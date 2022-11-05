import sqlalchemy 
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.expression import func
from App.database import db
from App.models import Profile, User
from App.controllers.rating_details import (
    get_rating_detail,
    create_rating_details
    )
from datetime import date

tier_points = 5
max_tier_points = 399

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

def get_profile_by_username(username):
    user = User.query.filter_by(username = username).first()
    if not user:
        return []
    
    profile = user.Profile

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
    
def rate_profile(profile_id, user_id, rating):
    profile = get_profile(profile_id)
    if not profile:
        return []
    rating_detail = get_rating_detail(user_id,profile_id)

    if rating_detail:
       rating =  rating - rating_detail.rating
       rating_detail = rating_detail.rating + rating
    else:
        create_rating_details(user_id,profile_id,rating)
    try:
        profile.rating = profile.rating + rating
        db.session.add(profile)
        db.session.commit()
        increase_tier_points(user_id)
        return profile
    except sqlalchemy.exc.SQLAlchemyError:
        db.session.rollback()
        return []

def increase_tier_points(profile_id):
    profile = get_profile(profile_id)
    if not profile:
        return []
    if profile.tier == max_tier_points:
        return []
    try:
        profile.tier = profile.tier + tier_points
        if profile.tier >= max_tier_points:
            profile.tier = max_tier_points
        db.session.add(profile)
        db.session.commit()
        return profile
    except sqlalchemy.exc.SQLAlchemyError:
        db.session.rollback()
        return []

tiers_max_views = dict(
    Bronze = 7,
    Gold = 14,
    Platinum = 21,
    Diamond = 28
)


def get_explore_profiles():
    '''
    step 1:
        obtain randomized columns from database

    step 2:
        loop through each

    step 3:
        if view_date > 24hrs:
            choose it and view count = 1;
        else
            if daily_views <= max_view_tier:
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
                profile.daily_views = 1
                profile.first_view_date = now
                result.append(profile)
                counter = counter + 1
                db.session.add(profile)
                db.session.commit()
            except sqlalchemy.exc.SQLAlchemyError:
                db.session.rollback()
        else:
            if profile.daily_views < tiers_max_views.get(profile.get_tier()):  
                try:
                    profile.daily_views = profile.daily_views + 1
                    result.append(profile)
                    counter = counter + 1
                    db.session.add(profile)
                    db.session.commit()
                except sqlalchemy.exc.SQLAlchemyError:
                    db.session.rollback()
        
        if counter >= counted:
            break

    return result