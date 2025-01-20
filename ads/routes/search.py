from flask import request, jsonify
from ads import ads_bp
from ads.models import Ad

@ads_bp.route('/search', methods=['GET'])
def search_ads():
    """
    Пошук оголошень за заголовком і описом.
    """
    try:
        # Отримання параметра пошуку
        query_param = request.args.get('query', '').lower().strip()

        # Якщо параметр пустий, повернути помилку
        if not query_param:
            return jsonify({"error": "Параметр 'query' не може бути порожнім."}), 400

        # Пошук за заголовком і описом (чутливість до регістру і часткове співпадіння)
        ads = Ad.query.filter(
            (Ad.title.ilike(f"%{query_param}%")) | (Ad.description.ilike(f"%{query_param}%"))
        ).all()

        # Якщо оголошення не знайдено
        if not ads:
            return jsonify({"message": "Оголошення не знайдені."}), 404

        # Формування результатів
        results = []
        for ad in ads:
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
        return jsonify({"message": "Результати пошуку:", "data": results}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
