from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from .. import user_bp
from ..models import User

@user_bp.route('/profile/<int:user_id>', methods=['GET'])
@jwt_required()  # Додаємо захист за допомогою JWT
def get_profile(user_id):
    # Отримання ID поточного користувача з JWT
    current_user_id = get_jwt_identity()

    # Отримання claims з JWT токена
    jwt_claims = get_jwt()

    # Отримання ролі користувача з токена
    user_role = jwt_claims.get("role") 

    if not user_role:
        return jsonify({"error": "Role is missing in the token"}), 403

    # Перевірка доступу: роль має бути "admin" або користувач має доступ до власного профілю
    if user_role == "admin":
        # Адмін може отримати доступ до всіх профілів
        pass
    elif user_role == "user" and int(user_id) == int(current_user_id):
        # Користувач може отримати доступ лише до свого профілю
        pass
    else:
        return jsonify({"error": "Access denied"}), 403

    # Спроба знайти користувача в базі даних
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Отримуємо оголошення користувача
    ads_data = [
        {
            "title": ad.title,
            "location": ad.location,
            "price": ad.price,
            "description": ad.description
        }
        for ad in user.ads
    ]

    # Повернення даних про користувача (спочатку користувач, потім оголошення)
    user_data = {
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "ads": ads_data  # Інформація про оголошення після користувача
    }

    return jsonify(user_data)
