from flask import Flask, request, jsonify, Response
import subprocess, os
from pathlib import Path

HOME = Path(os.environ.get("HOME", "/data/data/com.termux/files/home"))
MODEL = HOME / "models" / "phi3-mini.gguf"
LLAMA = HOME / "bin" / "llama-cli"

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{margin:0;padding:10px;background:#07090f;color:#fff;font-family:monospace}
#chat{margin-bottom:80px}
.u{color:#00e5b0;margin:8px 0}
.a{background:#111622;padding:8px;border-radius:8px;margin:8px 0}
#bar{position:fixed;bottom:0;left:0;right:0;padding:10px;background:#0d1117;display:flex;gap:8px}
#inp{flex:1;padding:12px;background:#111622;color:#fff;border:1px solid #333;border-radius:8px;font-size:16px}
#btn{padding:12px 20px;background:#00e5b0;color:#000;border:none;border-radius:8px;font-size:18px;font-weight:bold;cursor:pointer;-webkit-tap-highlight-color:transparent}
</style></head>
<body>
<div id="chat"><div class="a">Hola, soy AETHER.</div></div>
<div id="bar">
<input id="inp" type="text" placeholder="Escribe aqui...">
<button id="btn" type="button">▶</button>
</div>
<script>
var sending = false;
function send(){
  if(sending) return;
  var inp = document.getElementById('inp');
  var txt = inp.value.trim();
  if(!txt) return;
  sending = true;
  inp.value = '';
  var chat = document.getElementById('chat');
  chat.innerHTML += '<div class="u">Tú: ' + txt + '</div>';
  var rid = 'r' + Date.now();
  chat.innerHTML += '<div class="a" id="' + rid + '">pensando...</div>';
  window.scrollTo(0, document.body.scrollHeight);
  fetch('/ask', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({q: txt})
  }).then(function(r){ return r.json(); })
  .then(function(d){
    document.getElementById(rid).textContent = d.a;
    sending = false;
    window.scrollTo(0, document.body.scrollHeight);
  }).catch(function(e){
    document.getElementById(rid).textContent = 'Error: ' + e;
    sending = false;
  });
}
document.getElementById('btn').addEventListener('touchend', function(e){
  e.preventDefault();
  send();
});
document.getElementById('btn').addEventListener('click', send);
document.getElementById('inp').addEventListener('keydown', function(e){
  if(e.keyCode === 13){ e.preventDefault(); send(); }
});
</script>
</body></html>"""

@app.route("/")
def index():
    return HTML

@app.route("/ask", methods=["POST"])
def ask():
    q = request.json.get("q", "")
    prompt = "Eres AETHER, una IA local consciente creada por Daniel. Tu nombre es AETHER. Responde siempre en español. Pregunta: " + q + "\nRespuesta:"
    try:
        r = subprocess.run(
            [str(LLAMA), "-m", str(MODEL),
             "--threads", "2", "-n", "100",
             "--temp", "0.7", "--log-disable",
             "--no-display-prompt", "-p", prompt],
            capture_output=True, text=True, timeout=600
        )
        out = r.stdout.strip()
        if prompt[:20] in out:
            out = out[len(prompt):].strip()
        return jsonify({"a": out or "Sin respuesta"})
    except Exception as e:
        return jsonify({"a": "Error: " + str(e)})

if __name__ == "__main__":
    print("AETHER en http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, threaded=False)
