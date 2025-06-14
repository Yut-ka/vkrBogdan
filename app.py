from flask import Flask, render_template, request, session, jsonify
from werkzeug.utils import secure_filename
import os


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


UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
already_cleared = False


@app.route('/upload', methods=['POST'])
def upload_file():
    global already_cleared

    # Очистка только при первом запросе в сессии
    if not already_cleared:
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Ошибка удаления {file_path}: {e}")
        already_cleared = True  # больше не очищаем

    # Сохраняем файл
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return 'OK', 200
    return 'No file', 400

@app.route('/reset_upload', methods=['POST'])
def reset_upload():
    global already_cleared
    already_cleared = False
    return 'reset', 200


@app.route('/results')
def results():
    chosen = request.args.get('chosen')  # путь к выбранному фото
    all_files = os.listdir(UPLOAD_FOLDER)
    photos = [f for f in all_files if f != chosen and f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return render_template('results.html', chosen=chosen, photos=photos)


@app.route('/analyze', methods=['POST'])
def analyze():
    from deepface import DeepFace
    chosen_filename = request.json.get('chosen')
    if not chosen_filename:
        return jsonify({'error': 'No chosen image provided'}), 400

    chosen_path = os.path.join(UPLOAD_FOLDER, chosen_filename)
    if not os.path.exists(chosen_path):
        return jsonify({'error': 'Chosen image not found'}), 404

    all_files = os.listdir(UPLOAD_FOLDER)
    other_files = [f for f in all_files if f != chosen_filename and f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    results = []
    for file in other_files:
        try:
            file_path = os.path.join(UPLOAD_FOLDER, file)

            # Сравнение лиц
            comparison = DeepFace.verify(
                img1_path=chosen_path,
                img2_path=file_path,
                model_name='Facenet',
                distance_metric='cosine',
                enforce_detection=False
            )
            similarity = (1 - comparison['distance']) * 100

            # Анализ атрибутов: возраст, пол, раса
            analysis = DeepFace.analyze(
                img_path=file_path,
                actions=['age', 'gender', 'race'],
                enforce_detection=False
            )[0]  # берём первый результат

            results.append({
                'filename': file,
                'distance': comparison['distance'],
                'similarity': round(similarity, 2),
                'verified': comparison['verified'],
                'age': analysis['age'],
                'gender': analysis['gender'],
                'dominant_race': analysis['dominant_race']
            })

        except Exception as e:
            results.append({
                'filename': file,
                'error': str(e)
            })

    return jsonify({'results': results})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run()