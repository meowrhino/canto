from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)



UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'mp3')
TL_FILE = os.path.join(os.path.dirname(__file__), 'TL.json')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def load_tl():
    if not os.path.exists(TL_FILE):
        return []
    with open(TL_FILE, 'r', encoding='utf8') as f:
        return json.load(f)

def save_tl(tl):
    with open(TL_FILE, 'w', encoding='utf8') as f:
        json.dump(tl, f, ensure_ascii=False, indent=2)

@app.route('/api/tl', methods=['GET'])
def api_tl():
    tl = load_tl()
    return jsonify(tl[::-1])

@app.route('/api/guardar', methods=['POST'])
def api_guardar():
    if 'audio' not in request.files:
        return jsonify({"ok": False, "error": "No audio file"}), 400

    audio = request.files['audio']
    titulo = request.form.get('titulo', '').strip()
    comentario = request.form.get('comentario', '').strip()
    tipo = request.form.get('tipo', '').strip()

    fecha = datetime.datetime.now().isoformat(timespec="milliseconds")
    # Nombre: canto_2024-07-29_20-55-13-845.webm
    filename = f"canto_{fecha.replace(':','-').replace('T','_').replace('.','-')}.webm"
    filename = secure_filename(filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    audio.save(filepath)

    tl = load_tl()
    entrada = {
        "filename": filename,
        "fecha": fecha,
    }
    if titulo:
        entrada["titulo"] = titulo
    if comentario:
        entrada["comentario"] = comentario
    if tipo:
        entrada["tipo"] = tipo
    tl.append(entrada)
    save_tl(tl)
    return jsonify({"ok": True})

@app.route('/mp3/<filename>')
def serve_mp3(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/')
def home():
    return "Servidor de TL Canto activo!"

if __name__ == "__main__":
    app.run(debug=True, port=5001)

