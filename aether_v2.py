import subprocess, json, time, os
from pathlib import Path
from flask import Flask, request, jsonify

HOME = Path(os.environ.get("HOME", "/data/data/com.termux/files/home"))
MODEL = HOME / "models" / "phi3-mini.gguf"
LLAMA = HOME / "bin" / "llama-cli"

app = Flask(__name__)

def run_model(prompt):
    try:
        cmd = [str(LLAMA), "-m", str(MODEL),
               "--threads", "4", "-n", "256",
               "--temp", "0.7", "--log-disable",
               "--no-display-prompt", "-p", prompt]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        out = result.stdout.strip()
        if prompt[:20] in out:
            out = out[len(prompt):].strip()
        return out or "[Sin respuesta]"
    except Exception as e:
        return f"[ERROR]: {e}"

@app.route("/")
def index():
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AETHER</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#07090f;color:#c8d8f0;font-family:monospace;height:100vh;display:flex;flex-direction:column}
header{padding:12px 16px;background:#0d1117;border-bottom:1px solid #1a2535;text-align:center}
.logo{font-size:18px;font-weight:bold;color:#00e5b0;letter-spacing:3px}
#chat{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:8px}
.msg{max-width:90%;padding:10px 13px;border-radius:12px;font-size:13px;line-height:1.5}
.user{align-self:flex-end;background:#1a2540;border:1px solid #2a3d60}
.ai{align-self:flex-start;background:#111622;border:1px solid #1a2535}
.ai .tag{font-size:9px;color:#00e5b0;margin-bottom:4px}
footer{padding:10px 12px;background:#0d1117;border-top:1px solid #1a2535}
.row{display:flex;gap:8px}
textarea{flex:1;background:#111622;border:1px solid #1a2535;border-radius:10px;
color:#c8d8f0;font-family:monospace;font-size:13px;padding:10px;resize:none;
min-height:44px;max-height:100px;outline:none}
button{background:#00e5b0;border:none;border-radius:10px;width:46px;
font-size:20px;color:#000;font-weight:bold;cursor:pointer}
.dot{display:inline-block;width:6px;height:6px;background:#00e5b0;
border-radius:50%;margin:2px;animation:b .8s ease-in-out infinite}
.dot:nth-child(2){animation-delay:.15s}.dot:nth-child(3){animation-delay:.3s}
@keyframes b{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
</style></head>
<body>
<header><div class="logo">⬡ AETHER</div></header>
<div id="chat">
<div class="msg ai"><div class="tag">AETHER · listo</div>
Hola. Soy tu IA local corriendo en tu móvil. Sin internet. Sin servidores. Todo tuyo.</div>
</div>
<footer>
<div class="row">
<textarea id="inp" placeholder="Escribe aquí..." rows="1"></textarea>
<button id="btn">↑</button>
</div>
</footer>
<script>
document.addEventListener('DOMContentLoaded', function() {
  var btn = document.getElementById('btn');
  var inp = document.getElementById('inp');
  
  function send() {
    var txt = inp.value.trim();
    if (!txt) return;
    inp.value = '';
    btn.disabled = true;
    var chat = document.getElementById('chat');
    var um = document.createElement('div');
    um.className = 'msg user';
    um.textContent = txt;
    chat.appendChild(um);
    var lm = document.createElement('div');
    lm.className = 'msg ai';
    lm.innerHTML = '<div class=\"tag\">AETHER</div>pensando...';
    chat.appendChild(lm);
    chat.scrollTop = chat.scrollHeight;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/chat', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
      var d = JSON.parse(xhr.responseText);
      lm.innerHTML = '<div class=\"tag\">AETHER</div>' + d.output.replace(/
/g,'<br>');
      btn.disabled = false;
      chat.scrollTop = chat.scrollHeight;
    };
    xhr.onerror = function() {
      lm.innerHTML = 'Error de conexion';
      btn.disabled = false;
    };
    xhr.send(JSON.stringify({message: txt}));
  }
  
  btn.ontouchend = function(e) { e.preventDefault(); send(); };
  btn.onclick = function(e) { e.preventDefault(); send(); };
  inp.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
  });
});
</script></body></html>"""

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message","")
    prompt = f"Eres AETHER, un asistente de IA local en español. Usuario: {msg}\nAETHER:"
    output = run_model(prompt)
    return jsonify({"output": output})

if __name__ == "__main__":
    print(f"Modelo: {MODEL}")
    print(f"Motor:  {LLAMA}")
    print("Abriendo en: http://localhost:5000")
    app.run(host="0.0.0.0", port=5000)

@app.route("/chat.html")
def chat_html():
    return open("/data/data/com.termux/files/home/aether/chat.html").read(), 200, {"Content-Type": "text/html"}
