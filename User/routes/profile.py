from flask import jsonify
from .. import user_bp
from ..models import User

@user_bp.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    # Спроба знайти користувача в базі даних
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Отримуємо оголошення користувача
    ads_data = []
    for ad in user.ads:
        ads_data.append({
            "title": ad.title,
            "location": ad.location,
            "price": ad.price,
            "description": ad.description
        })

    # Повернення даних про користувача (спочатку користувач, потім оголошення)
    user_data = {
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "ads": ads_data  # Інформація про оголошення після користувача
    }

    return jsonify(user_data)
