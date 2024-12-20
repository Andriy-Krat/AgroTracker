from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
from ads import ads_bp
app.register_blueprint(ads_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)