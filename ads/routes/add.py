from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from ads import ads_bp  # Імпортуємо існуючий блупрінт
from ads.models import Ad, AdImage
from ads.utils import allowed_file, format_ad_response
from ads.agrotracker_sendgrind import send_notification_email

@ads_bp.route('/add', methods=['POST'])
def add_ad_with_images():
    data = request.form.to_dict()
    files = request.files.getlist('images')
    if len(files) > 7:
        return jsonify({"error": "Максимальна кількість зображень - 7."}), 400

    try:
        if 'price' in data:
            data['price'] = float(data['price'])
        ad = Ad(**data)
        ad.save()
        uploaded_images = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                image_url = f'/uploads/{filename}'
                ad_image = AdImage(ad_id=ad.id, image_url=image_url)
                ad_image.save()
                uploaded_images.append(image_url)
        
        if 'email' in data:  
            send_notification_email(
                to_email=data['email'],
                subject="Ваша заявка успішно створена!",
                message=f"""
                Шановний користувачу,
                Ваша заявка <b>{ad.title} була успішно створена!
                Опис: {ad.description}
                Локація: {ad.location}
                Ціна: {ad.price} UAH
                Дякуємо за використання нашого сервісу AgroTracker!
                Очікуйте повідомлення якщо хтось обере вашу заявку
                """
            )

        response_data = format_ad_response(ad, images=uploaded_images)
        return jsonify({"message": "Заявка успішно створена.", "data": response_data}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

#efef