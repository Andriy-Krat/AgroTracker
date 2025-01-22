<<<<<<< HEAD
from flask import jsonify, request
from ads import ads_bp
from ads.models import Ad
from ads.utils import format_ad_response

@ads_bp.route('/ads', methods=['GET'])
def get_all_ads():
    try:
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=5, type=int)

        if page < 1 or per_page < 1:
            return jsonify({"error": "Параметри 'page' і 'per_page' повинні бути більшими за 0."}), 400

        paginated_ads = Ad.query.paginate(page=page, per_page=per_page, error_out=False)

        if not paginated_ads.items:
            return jsonify({"message": "Оголошення не знайдені."}), 404

        results = [
            format_ad_response(ad, [image.image_url for image in ad.images])
            for ad in paginated_ads.items
        ]

        return jsonify({
            "message": "Це головна сторінка з оголошеннями.",
            "data": results,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": paginated_ads.total,
                "pages": paginated_ads.pages
=======
from flask import request, jsonify
from ads import ads_bp
from ads.models import Ad

@ads_bp.route('/paginate', methods=['GET'])
def paginate_ads():
    """
    Функція для пагінації оголошень.
    """
    try:
        # Отримання параметрів пагінації
        page = int(request.args.get('page', 1))  # Номер сторінки (за замовчуванням 1)
        per_page = int(request.args.get('per_page', 10))  # Кількість елементів на сторінку (за замовчуванням 10)

        # Перевірка коректності параметрів
        if page < 1 or per_page < 1:
            return jsonify({"error": "Параметри page і per_page повинні бути більшими за 0."}), 400

        # Виконання запиту з пагінацією
        paginated_ads = Ad.query.paginate(page=page, per_page=per_page, error_out=False)

        # Якщо оголошення не знайдено
        if not paginated_ads.items:
            return jsonify({"message": "Оголошення не знайдені."}), 404

        # Формування результатів
        results = []
        for ad in paginated_ads.items:
            results.append({
                "id": ad.id,
                "title": ad.title,
                "description": ad.description,
                "location": ad.location,
                "region": ad.region,
                "district": ad.district,
                "price": ad.price
            })

        # Повернення результатів із даними про пагінацію
        return jsonify({
            "message": "Результати пагінації:",
            "data": results,
            "pagination": {
                "page": paginated_ads.page,
                "per_page": paginated_ads.per_page,
                "total_items": paginated_ads.total,
                "total_pages": paginated_ads.pages
>>>>>>> master
            }
        }), 200

    except Exception as e:
<<<<<<< HEAD
        return jsonify({"error": f"Виникла помилка: {str(e)}"}), 500
=======
        return jsonify({"error": str(e)}), 400
>>>>>>> master
