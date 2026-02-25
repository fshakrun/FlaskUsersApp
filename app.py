from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from models import db, User

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# --- создать БД ---
with app.app_context():
    db.create_all()


# =========================
# Главная страница
# =========================
@app.route("/")
def index():
    return render_template("index.html")


# =========================
# GET /users
# =========================
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


# =========================
# GET /users/<id>
# =========================
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.to_dict())


# =========================
# POST /users  (для задания 3)
# =========================
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data or not data.get("name") or not data.get("email"):
        return jsonify({"error": "Name and email required"}), 400

    # проверка уникальности email
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400

    user = User(name=data["name"], email=data["email"])
    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201


if __name__ == "__main__":
    app.run(debug=True)