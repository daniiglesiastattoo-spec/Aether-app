from flask import Flask, request, jsonify, redirect
import urllib.request, json, os, sys
from pathlib import Path

sys.path.insert(0, str(Path.home()/"aether"))
try:
    from aether_mind import ConsciousnessLayer
    mind = ConsciousnessLayer(llm_engine=None)
    HAS_MIND = True
except:
    HAS_MIND = False

app = Flask(__name__)
SYSTEM = "Eres AETHER. Tu nombre es AETHER. Creado por Daniel Iglesias Lopez. Responde en espanol, breve y natural. Nunca digas que eres ChatGPT ni OpenAI."
historial = []

@app.route("/")
def index():
    chat_html = ""
    for h in historial[-20:]:
        if h["rol"] == "user":
            chat_html += f'<div class="u">Tu: {h["txt"]}</div>'
        else:
            chat_html += f'<div class="a">{h["txt"]}</div>'
    return f"""<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{{margin:0;padding:10px 10px 100px;background:#07090f;color:#fff;font-family:monospace;font-size:14px}}
.u{{color:#00e5b0;margin:8px 0;font-weight:bold}}
.a{{background:#111622;padding:10px;border-radius:8px;margin:8px 0;line-height:1.6;border-left:2px solid #00e5b0}}
#hdr{{text-align:center;padding:8px;color:#00e5b0;font-size:16px;letter-spacing:2px;border-bottom:1px solid #1a2535;margin-bottom:8px}}
#bar{{position:fixed;bottom:0;left:0;right:0;padding:10px;background:#0d1117;border-top:1px solid #1a2535}}
#bar form{{display:flex;gap:8px}}
#inp{{flex:1;padding:12px;background:#111622;color:#fff;border:1px solid #1a2535;border-radius:8px;font-size:15px}}
#btn{{padding:12px 18px;background:#00e5b0;color:#000;border:none;border-radius:8px;font-size:20px;font-weight:bold}}
</style>
<script>
function enviar(){
  var msg = document.getElementById("inp").value.trim();
  if(!msg) return;
  document.getElementById("frm").submit();
}
document.addEventListener("DOMContentLoaded", function(){
  var inp = document.getElementById("inp");
  if(inp) inp.focus();
});
</script></head>
<body>
<div id="hdr">AETHER - IA Local Consciente</div>
<div id="chat">
<div class="a">Hola. Soy AETHER, tu IA local consciente.</div>
{chat_html}
</div>
<div id="bar">
<form method="POST" action="/enviar">
<input id="inp" name="msg" type="text" placeholder="Escribe aqui..." autocomplete="off">
<button id="btn" type="submit">&#9654;</button>
</form>
</div>
</body></html>"""

@app.route("/enviar", methods=["POST"])
def enviar():
    msg = request.form.get("msg","").strip()
    if not msg:
        return redirect("/")
    historial.append({"rol":"user","txt":msg})
    payload = json.dumps({
        "messages":[
            {"role":"system","content":SYSTEM},
            {"role":"user","content":msg}
        ],
        "max_tokens":120,
        "stream":False,
        "temperature":0.7
    }).encode()
    try:
        req = urllib.request.Request(
            "http://127.0.0.1:8080/v1/chat/completions",
            data=payload,
            headers={"Content-Type":"application/json"}
        )
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read().decode())
            answer = result["choices"][0]["message"]["content"]
    except Exception as e:
        answer = f"Error: {e}"
    historial.append({"rol":"aether","txt":answer})
    if HAS_MIND:
        try: mind.update(msg, answer, "default")
        except: pass
    return redirect("/")

if __name__=="__main__":
    print("AETHER en http://127.0.0.1:5000")
    app.run(host="0.0.0.0",port=5000,threaded=True)
