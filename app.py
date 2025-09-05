from flask import Flask, render_template_string, request, send_file
from gtts import gTTS
import os
from datetime import datetime

# ---------------- CONFIG ----------------
BASE_DIR = os.getcwd()
OUTPUT_DIR = os.path.join(BASE_DIR, "Output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = Flask(__name__)

# ---------------- HTML TEMPLATE ----------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AI Text → Audio Converter</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f5f5f5; padding: 40px; }
        .container { background: white; padding: 20px; border-radius: 10px; max-width: 600px; margin: auto; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        textarea { width: 100%; height: 150px; padding: 10px; font-size: 16px; }
        select, button { padding: 10px; font-size: 16px; margin-top: 10px; }
        .success { margin-top: 20px; padding: 10px; background: #d1ffd1; border: 1px solid #8bc34a; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Text → Audio Converter</h1>
        <form method="POST">
            <label>Enter your text/script:</label><br>
            <textarea name="text" required placeholder="Paste your script here..."></textarea><br>
            <label>Voice language:</label><br>
            <select name="lang">
                <option value="en" selected>English</option>
            </select><br>
            <button type="submit">Convert to MP3</button>
        </form>
        {% if audio_url %}
        <div class="success">
            ✅ Done! <a href="{{ audio_url }}">Click here to download your audio</a>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

# ---------------- ROUTES ----------------
@app.route("/", methods=["GET", "POST"])
def index():
    audio_url = None
    if request.method == "POST":
        text = request.form.get("text", "").strip()
        lang = request.form.get("lang", "en")

        if text:
            filename = f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            filepath = os.path.join(OUTPUT_DIR, filename)

            tts = gTTS(text=text, lang=lang)
            tts.save(filepath)

            audio_url = f"/download/{filename}"

    return render_template_string(HTML_TEMPLATE, audio_url=audio_url)


@app.route("/download/<filename>")
def download_file(filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    return send_file(filepath, as_attachment=True)


# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # host 0.0.0.0 needed for cloud (Render/Heroku)
    app.run(host="0.0.0.0", port=port, debug=False)


