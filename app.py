from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

print("pppp")
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
from ads import ads_bp
print("Перед реєстрацією блупринта...")
app.register_blueprint(ads_bp)
print("Blueprint 'ads' зареєстровано")
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Надати доступ до завантажених файлів."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=False)