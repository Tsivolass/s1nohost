from flask import Flask, request, send_file
import os

app = Flask(__name__)
UPLOAD_FOLDER = "game_saves/"
API_TOKEN = os.getenv("API_TOKEN", "o7khRHLxpE6uShoa78aW3f997nXU3Q0Q")  # Secure API token
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_save_path(game_name):
    return os.path.join(UPLOAD_FOLDER, f"{game_name}.zip")

@app.route("/upload", methods=["POST"])
def upload_save():
    if request.headers.get("Authorization") != f"Bearer {API_TOKEN}":
        return {"error": "Unauthorized"}, 403

    if 'file' not in request.files:
        return {"error": "No file part"}, 400

    file = request.files['file']
    game_name = request.form.get("game_name")

    if not game_name:
        return {"error": "Missing game name"}, 400

    save_path = get_save_path(game_name)
    file.save(save_path)
    return {"message": "File uploaded successfully"}, 200

@app.route("/download", methods=["GET"])
def download_save():
    if request.headers.get("Authorization") != f"Bearer {API_TOKEN}":
        return {"error": "Unauthorized"}, 403

    game_name = request.args.get("game_name")

    if not game_name:
        return {"error": "Missing game name"}, 400

    save_path = get_save_path(game_name)

    if not os.path.exists(save_path):
        return {"error": "No save file found"}, 404

    return send_file(save_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
