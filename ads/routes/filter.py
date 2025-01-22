from flask import request, jsonify
from ads import ads_bp
from ads.models import Ad
<<<<<<< HEAD
from ads.utils import format_ad_response
=======
>>>>>>> master


@ads_bp.route('/filter', methods=['GET'])
def filter_ads():
    """
    Функція для фільтрації оголошень за location, region та district.
    """
    try:
        # Отримання параметрів фільтрації
        location = request.args.get('location', '').lower()
<<<<<<< HEAD
=======
        region = request.args.get('region', '').lower()
        district = request.args.get('district', '').lower()
>>>>>>> master

        # Базовий запит для фільтрації
        query = Ad.query

        # Додавання умов залежно від параметрів
        if location:
            query = query.filter(Ad.location.ilike(f"%{location}%"))
<<<<<<< HEAD
=======

        if region:
            query = query.filter(Ad.region.ilike(f"%{region}%"))

        if district:
            query = query.filter(Ad.district.ilike(f"%{district}%"))

>>>>>>> master
        # Виконання запиту
        ads = query.all()

        # Якщо оголошення не знайдено
        if not ads:
            return jsonify({"message": "Оголошення не знайдені."}), 404

        # Формування результатів
        results = []
        for ad in ads:
<<<<<<< HEAD
            # Отримання URL зображень для оголошення
            images = [image.image_url for image in ad.images]
            # Форматування відповіді
            ad_response = format_ad_response(ad, images)
            results.append(ad_response)

=======
            results.append({
                "id": ad.id,
                "title": ad.title,
                "description": ad.description,
                "location": ad.location,
                "region": ad.region,
                "district": ad.district,
                "price": ad.price
            })

        # Повернення результатів
>>>>>>> master
        return jsonify({"message": "Результати фільтрації:", "data": results}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
