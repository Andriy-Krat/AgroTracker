from flask import request, jsonify
from . import ads_bp
from .models import Ad  # Імпортуємо модель Ad

# Маршрут для додавання заявки
@ads_bp.route('/add', methods=['POST'])
def add_ad():
    """Додати нову заявку."""
    data = request.json
    try:
        ad = Ad(**data)
        ad.save()
        return jsonify({"message": "Ad successfully added", "data": data}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Маршрут для редагування заявки
@ads_bp.route('/edit/<int:ad_id>', methods=['PUT'])
def edit_ad(ad_id):
    """Редагувати існуючу заявку."""
    data = request.json 
    ad = Ad.find_by_id(ad_id)  
    if not ad:
        return jsonify({"error": "Ad not found"}), 404
    try:
        ad.update(data)
        return jsonify({"message": f"Ad with ID {ad_id} updated", "updated_data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Маршрут для видалення заявки
@ads_bp.route('/delete/<int:ad_id>', methods=['DELETE'])
def delete_ad(ad_id):
    ad = Ad.find_by_id(ad_id)
    if not ad:
        return jsonify({"error": "Ad not found"}), 404
    try:
        ad.delete()
        return jsonify({"message": f"Ad with ID {ad_id} deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Маршрут для прийняття заявки
@ads_bp.route('/accept/<int:ad_id>', methods=['POST'])
def accept_ad(ad_id):
    ad = Ad.find_by_id(ad_id)
    if not ad:
        return jsonify({"error": "Ad not found"}), 404
    try:
        ad.accepted = True
        ad.save()
        return jsonify({"message": f"Ad with ID {ad_id} accepted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400