from flask import Flask, render_template, request, session, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'

users_db = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/main/")
def main():
    if 'username' in session:
        return render_template("main.html", username=session['username'])
    else:
        return render_template("index.html")

@app.route("/ajax_login", methods=["POST"])
def ajax_login():
    username = request.form.get("username")
    password = request.form.get("password")
    user = users_db.get(username)
    if user and user['password'] == password:
        session['username'] = username
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="Неверный логин или пароль.")

@app.route("/ajax_register", methods=["POST"])
def ajax_register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    
    # 1. Проверка уникальности логина
    if username in users_db:
        return jsonify(success=False, message="Этот логин уже занят.")
    
    # 2. Проверка уникальности email среди всех пользователей
    for u in users_db.values():
        if u['email'].lower() == email.lower():
            return jsonify(success=False, message="Этот email уже используется.")

    # Если все ок, добавляем пользователя
    users_db[username] = {"email": email, "password": password}
    session['username'] = username
    return jsonify(success=True)

@app.route("/logout")
def logout():
    session.pop('username', None)
    return '', 204  # пустой ответ

if __name__ == "__main__":
    app.run(debug=True)
