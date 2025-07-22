from backend.api.routes import api_blueprint
from backend.api.models import db
from flask import Flask

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jobs.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()
app.register_blueprint(api_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
