from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from ads.utils import format_ad_response
from User.models import User

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile/<int:user_id>', methods=['GET'])
@jwt_required()  
def get_profile(user_id):

    current_user_id = get_jwt_identity()


    jwt_claims = get_jwt()


    user_role = jwt_claims.get("role") 

    if not user_role:
        return jsonify({"error": "Role is missing in the token"}), 403
 

    if user_role == "admin":

        pass

    elif user_role == "user" and int(user_id) == int(current_user_id):

        pass

    else:
        return jsonify({"error": "Access denied"}), 403


    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404


    ads_data = [
        format_ad_response(ad, [image.image_url for image in ad.images])
        for ad in user.ads
    ]

    # Повернення даних про користувача (спочатку користувач, потім оголошення)
    user_data = {
        "ads": ads_data  # Інформація про оголошення після користувача
    }

    return jsonify(user_data)
# Повернення даних про користувача (спочатку користувач, потім оголошення)
   # user_data = {
        #"username": user.username,
        #"email": user.email,
        #"phone": user.phone,
       # "ads": ads_data  # Інформація про оголошення після користувача
   # }