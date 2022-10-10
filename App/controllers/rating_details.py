from App.models import Rating_Details
from App.database import db 

def create_rating_details(rater_user_id,ratee_profile_id, rating):
    newRatingDetails = Rating_Details(rater_user_id,ratee_profile_id, rating)
    db.session.add(newRatingDetails)
    db.session.commit()

def get_rating_detail(rater_user_id,ratee_profile_id):
    rating_detail = Rating_Details.query.filter_by(rater_user_id = rater_user_id, ratee_profile_id = ratee_profile_id).first()

    if not rating_detail:
        return []
    return rating_detail