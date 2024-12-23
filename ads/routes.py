from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from . import ads_bp
from .models import Ad, AdImage  # Імпортуємо модель Ad

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

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
    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Маршрут для завантаження зображень
@ads_bp.route('/add', methods=['POST'])
def add_ad():
    """Додати заявку з можливістю завантаження зображень."""
    data = request.form.to_dict()  # Дані заявки
    files = request.files.getlist('images')  # Отримання файлів

    if len(files) > 7:
        return jsonify({"error": "Максимальна кількість зображень - 7."}), 400

    ad = Ad(**data)
    ad.save()

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            image_url = f'/uploads/{filename}'
            ad_image = AdImage(ad_id=ad.id, image_url=image_url)
            ad_image.save()

    return jsonify({"message": "Заявка успішно додана з зображеннями."}), 201