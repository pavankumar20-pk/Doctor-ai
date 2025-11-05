# app.py
from flask import Flask, render_template_string, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Static Dolo 650 info (will be shown after upload)
DOLO_INFO = {
    "name": "Dolo 650 (Paracetamol 650 mg)",
    "purpose": "Reduces fever and relieves mild to moderate pain (headache, body ache, cold/flu).",
    "how_it_works": "Lowers body temperature and blocks pain signals in the brain.",
    "dosage": "Usually 1 tablet every 6 hours as needed. Do not exceed 4 tablets (2600 mg) in 24 hours.",
    "advantages": "Fast-acting, gentle on stomach when taken correctly, widely used.",
    "precautions": "Avoid alcohol; consult a doctor if you have liver/kidney issues or are on other medicines.",
    "summary": "Dolo 650 is a paracetamol-based medicine for fever and pain relief. Use only as directed."
}

# Simple HTML template (upload + display)
HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Medicine Info Uploader</title>
  <style>
    body{font-family:Arial, sans-serif; background:#f5f7fb; display:flex; align-items:center; justify-content:center; height:100vh;}
    .card{width:720px; background:white; border-radius:8px; box-shadow:0 6px 18px rgba(0,0,0,0.08); padding:20px;}
    .row{display:flex; gap:20px;}
    .left{flex:1;}
    .right{flex:1;}
    img{max-width:100%; border-radius:6px; border:1px solid #e6e9ef;}
    h2{margin-top:0;}
    .info{margin-bottom:8px;}
    .btn{background:#0078d7;color:white;padding:8px 14px;border:none;border-radius:6px;cursor:pointer;}
    .note{font-size:0.9rem;color:#666;}
  </style>
</head>
<body>
  <div class="card">
    <h2>Upload Medicine Image</h2>
    <p class="note">Upload a tablet blister or pill image (e.g. Dolo 650). For this demo, the app will display Dolo 650 info after upload.</p>

    <form method="POST" action="/upload" enctype="multipart/form-data">
      <input type="file" name="file" accept="image/*" required>
      <button class="btn" type="submit">Upload & Get Info</button>
    </form>

    {% if filename %}
    <hr>
    <div class="row">
      <div class="left">
        <h3>Uploaded Image</h3>
        <img src="{{ url_for('uploaded_file', filename=filename) }}" alt="uploaded">
      </div>
      <div class="right">
        <h3>Detected Medicine</h3>
        <p class="info"><strong>Name:</strong> {{ info.name }}</p>
        <p class="info"><strong>Purpose:</strong> {{ info.purpose }}</p>
        <p class="info"><strong>How it works:</strong> {{ info.how_it_works }}</p>
        <p class="info"><strong>Dosage:</strong> {{ info.dosage }}</p>
        <p class="info"><strong>Advantages:</strong> {{ info.advantages }}</p>
        <p class="info"><strong>Precautions:</strong> {{ info.precautions }}</p>
        <hr>
        <p><strong>Summary:</strong> {{ info.summary }}</p>
      </div>
    </div>
    {% endif %}
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML, filename=None, info=None)

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return redirect(url_for("index"))

    file = request.files["file"]
    if file.filename == "":
        return redirect(url_for("index"))

    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)

    # For demo: we always return the Dolo 650 info.
    # (You can replace this with real image recognition later.)
    return render_template_string(HTML, filename=filename, info=DOLO_INFO)

@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return app.send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)
