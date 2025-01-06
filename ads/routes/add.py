from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from ads import ads_bp  # Імпортуємо існуючий блупрінт
from ads.models import Ad, AdImage
from ads.utils import allowed_file, format_ad_response
from ads.agrotracker_mailgun import send_notification_email

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
                <p>Шановний користувачу,</p>
                <p>Ваша заявка <b>{ad.title}</b> була успішно створена!</p>
                <p>Опис: {ad.description}</p>
                <p>Локація: {ad.location}</p>
                <p>Ціна: {ad.price} UAH</p>
                <p>Дякуємо за використання нашого сервісу AgroTracker!</p>
                <p>Очікуйте повідомлення якщо хтось обере вашу заявку</p>
                """
            )

        response_data = format_ad_response(ad, images=uploaded_images)
        return jsonify({"message": "Заявка успішно створена.", "data": response_data}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400
