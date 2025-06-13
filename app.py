from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Для сессий

# Пример "базы данных" (замени на нормальную БД)
users = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/main/")
def main():
    # Пример простой авторизации
    if 'username' in session:
        return render_template("main.html", username=session['username'])
    else:
        return redirect(url_for('home'))

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    # Проверяем пользователя
    if username in users and users[username]['password'] == password:
        session['username'] = username
        return redirect(url_for('main'))
    else:
        flash('Неправильный логин или пароль')
        return redirect(url_for('home'))

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    # Проверяем, не занят ли логин
    if username in users:
        flash('Логин уже занят')
        return redirect(url_for('home'))
    users[username] = {'email': email, 'password': password}
    session['username'] = username
    return redirect(url_for('main'))

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
