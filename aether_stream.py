from flask import Flask, request, Response, redirect
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

HTML = """<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#07090f;color:#fff;font-family:monospace;font-size:14px;height:100vh;display:flex;flex-direction:column}
#hdr{text-align:center;padding:10px;color:#00e5b0;font-size:15px;letter-spacing:2px;border-bottom:1px solid #1a2535;flex-shrink:0}
#chat{flex:1;overflow-y:auto;padding:10px;display:flex;flex-direction:column;gap:8px}
.u{color:#00e5b0;font-weight:bold;padding:4px 0}
.a{background:#111622;padding:10px;border-radius:8px;line-height:1.6;border-left:2px solid #00e5b0;white-space:pre-wrap}
#bar{flex-shrink:0;padding:10px;background:#0d1117;border-top:1px solid #1a2535;display:flex;gap:8px}
#inp{flex:1;padding:12px;background:#111622;color:#fff;border:1px solid #1a2535;border-radius:8px;font-size:15px;font-family:monospace}
#btn{padding:12px 16px;background:#00e5b0;color:#000;border:none;border-radius:8px;font-size:15px;font-weight:bold;min-width:80px}
#btn:disabled{opacity:0.5}
#status{font-size:10px;color:#4a607a;text-align:center;padding:3px}
</style></head>
<body>
<div id="hdr">AETHER - IA Local Consciente</div>
<div id="chat">
<div class="a">Hola. Soy AETHER, tu IA local consciente. En que puedo ayudarte?</div>
</div>
<div id="status" id="st"></div>
<div id="bar">
<input id="inp" type="text" placeholder="Escribe aqui..." autocomplete="off">
<button id="btn">ENVIAR</button>
</div>
<script>
var busy = false;
var chat = document.getElementById('chat');
var inp = document.getElementById('inp');
var btn = document.getElementById('btn');

function scrollDown(){ chat.scrollTop = chat.scrollHeight; }

function send(){
  if(busy) return;
  var txt = inp.value.trim();
  if(!txt) return;
  busy = true;
  btn.disabled = true;
  btn.textContent = '...';
  inp.value = '';

  var ud = document.createElement('div');
  ud.className = 'u';
  ud.textContent = 'Tu: ' + txt;
  chat.appendChild(ud);

  var ad = document.createElement('div');
  ad.className = 'a';
  ad.textContent = '';
  chat.appendChild(ad);
  scrollDown();

  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/stream', true);
  xhr.setRequestHeader('Content-Type', 'application/json');

  var last = 0;
  xhr.onprogress = function(){
    var chunk = xhr.responseText.substring(last);
    last = xhr.responseText.length;
    var tokens = chunk.split('|||');
    tokens.forEach(function(t){
      if(t === '[FIN]'){
        busy = false;
        btn.disabled = false;
        btn.textContent = 'ENVIAR';
        return;
      }
      if(t.length > 0){
        ad.textContent += t;
        scrollDown();
      }
    });
  };

  xhr.onload = function(){
    busy = false;
    btn.disabled = false;
    btn.textContent = 'ENVIAR';
  };

  xhr.onerror = function(){
    ad.textContent = 'Error de conexion';
    busy = false;
    btn.disabled = false;
    btn.textContent = 'ENVIAR';
  };

  xhr.timeout = 300000;
  xhr.send(JSON.stringify({msg: txt}));
}

btn.addEventListener('touchend', function(e){ e.preventDefault(); send(); });
btn.addEventListener('click', send);
inp.addEventListener('keydown', function(e){
  if(e.keyCode === 13){ e.preventDefault(); send(); }
});
inp.focus();
</script>
</body></html>"""

@app.route("/")
def index(): return HTML

@app.route("/stream", methods=["POST"])
def stream():
    msg = request.json.get("msg", "")
    system = SYSTEM
    if HAS_MIND:
        try:
            ctx = mind.context_for(msg, "default")
            system = SYSTEM + "\n" + ctx[:400]
        except: pass

    payload = json.dumps({
        "messages":[
            {"role":"system","content":system},
            {"role":"user","content":msg}
        ],
        "max_tokens": 150,
        "stream": True,
        "temperature": 0.7
    }).encode()

    def generate():
        full = []
        try:
            req = urllib.request.Request(
                "http://127.0.0.1:8080/v1/chat/completions",
                data=payload,
                headers={"Content-Type":"application/json"}
            )
            with urllib.request.urlopen(req, timeout=300) as resp:
                for line in resp:
                    line = line.decode().strip()
                    if not line.startswith("data:"): continue
                    data = line[5:].strip()
                    if data == "[DONE]": break
                    try:
                        j = json.loads(data)
                        token = j["choices"][0]["delta"].get("content","")
                        if token:
                            full.append(token)
                            yield token + "|||"
                    except: pass
        except Exception as e:
            yield "Error: " + str(e) + "|||"
        if HAS_MIND:
            try: mind.update(msg, "".join(full), "default")
            except: pass
        yield "[FIN]"

    return Response(generate(),
        content_type="text/plain",
        headers={
            "Cache-Control":"no-cache",
            "X-Accel-Buffering":"no",
            "Transfer-Encoding":"chunked"
        }
    )

if __name__=="__main__":
    print("AETHER streaming en http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, threaded=True)
