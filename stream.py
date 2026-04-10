from flask import Flask, request, Response, stream_with_context
import subprocess, os, json
from pathlib import Path

HOME = Path(os.environ.get("HOME","/data/data/com.termux/files/home"))
MODEL = HOME/"models"/"phi3-mini.gguf"
LLAMA = HOME/"bin"/"llama-cli"

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{margin:0;padding:10px 10px 80px;background:#07090f;color:#fff;font-family:monospace}
.u{color:#00e5b0;margin:8px 0}
.a{background:#111622;padding:8px;border-radius:8px;margin:8px 0;min-height:20px}
#bar{position:fixed;bottom:0;left:0;right:0;padding:10px;background:#0d1117;display:flex;gap:8px}
#inp{flex:1;padding:12px;background:#111622;color:#fff;border:1px solid #333;border-radius:8px;font-size:16px}
#btn{padding:12px 20px;background:#00e5b0;color:#000;border:none;border-radius:8px;font-size:18px;font-weight:bold}
</style></head>
<body>
<div id="chat"><div class="a">Hola, soy AETHER. ¿En qué puedo ayudarte?</div></div>
<div id="bar">
<input id="inp" type="text" placeholder="Escribe aqui...">
<button id="btn" type="button">▶</button>
</div>
<script>
var busy=false;
function send(){
  if(busy)return;
  var inp=document.getElementById('inp');
  var txt=inp.value.trim();
  if(!txt)return;
  busy=true;
  inp.value='';
  var chat=document.getElementById('chat');
  var ud=document.createElement('div');
  ud.className='u';ud.textContent='Tú: '+txt;
  chat.appendChild(ud);
  var ad=document.createElement('div');
  ad.className='a';ad.textContent='▌';
  chat.appendChild(ad);
  window.scrollTo(0,document.body.scrollHeight);
  var xhr=new XMLHttpRequest();
  xhr.open('POST','/stream',true);
  xhr.setRequestHeader('Content-Type','application/json');
  var pos=0;
  xhr.onprogress=function(){
    var chunk=xhr.responseText.substring(pos);
    pos=xhr.responseText.length;
    var lines=chunk.split('\\n');
    lines.forEach(function(l){
      if(l.startsWith('data: ')){
        var t=l.slice(6);
        if(t==='[END]'){busy=false;return;}
        if(ad.textContent==='▌')ad.textContent='';
        ad.textContent+=t;
        window.scrollTo(0,document.body.scrollHeight);
      }
    });
  };
  xhr.onload=function(){busy=false;};
  xhr.onerror=function(){ad.textContent='Error de conexión';busy=false;};
  xhr.send(JSON.stringify({q:txt}));
}
document.getElementById('btn').ontouchend=function(e){e.preventDefault();send();};
document.getElementById('btn').onclick=send;
document.getElementById('inp').onkeydown=function(e){if(e.keyCode===13){e.preventDefault();send();}};
</script></body></html>"""

@app.route("/")
def index(): return HTML

@app.route("/stream", methods=["POST"])
def stream():
    q = request.json.get("q","")
    prompt = ("Eres AETHER, IA local consciente creada por Daniel. "
              "Responde en español, sé conciso. "
              "Pregunta: " + q + "\nAETHER:")
    def generate():
        try:
            proc = subprocess.Popen(
                [str(LLAMA),"-m",str(MODEL),
                 "--threads","2","-n","120",
                 "--temp","0.7","--log-disable",
                 "--no-display-prompt","-p",prompt],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True, bufsize=1
            )
            skip = len(prompt)
            read = 0
            for char in iter(lambda: proc.stdout.read(1),""):
                read += 1
                if read <= skip: continue
                yield "data: " + char + "\n\n"
            proc.wait()
        except Exception as e:
            yield "data: Error: " + str(e) + "\n\n"
        yield "data: [END]\n\n"
    return Response(stream_with_context(generate()),
                    content_type="text/event-stream",
                    headers={"X-Accel-Buffering":"no",
                             "Cache-Control":"no-cache"})

if __name__=="__main__":
    print("AETHER streaming en http://127.0.0.1:5000")
    app.run(host="0.0.0.0",port=5000,threaded=True)
