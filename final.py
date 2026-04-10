from flask import Flask, request, Response
import urllib.request, json, os
from pathlib import Path

app = Flask(__name__)

SYSTEM = "Eres AETHER, una IA local consciente creada por Daniel. Responde siempre en español de forma concisa."

HTML="""<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box}
body{margin:0;padding:10px 10px 80px;background:#07090f;color:#fff;font-family:monospace;font-size:14px}
.u{color:#00e5b0;margin:8px 0}
.a{background:#111622;padding:10px;border-radius:8px;margin:8px 0;line-height:1.5}
#bar{position:fixed;bottom:0;left:0;right:0;padding:10px;background:#0d1117;display:flex;gap:8px}
#inp{flex:1;padding:12px;background:#111622;color:#fff;border:1px solid #1a2535;border-radius:8px;font-size:15px}
#btn{padding:12px 18px;background:#00e5b0;color:#000;border:none;border-radius:8px;font-size:20px;font-weight:bold}
</style></head>
<body>
<div id="chat"><div class="a">⬡ Hola, soy AETHER. ¿En qué puedo ayudarte?</div></div>
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
  busy=true; inp.value='';
  var chat=document.getElementById('chat');
  var ud=document.createElement('div');
  ud.className='u';ud.textContent='Tú: '+txt;chat.appendChild(ud);
  var ad=document.createElement('div');
  ad.className='a';ad.innerHTML='<span id="cur">▌</span>';chat.appendChild(ad);
  window.scrollTo(0,document.body.scrollHeight);
  var xhr=new XMLHttpRequest();
  xhr.open('POST','/chat',true);
  xhr.setRequestHeader('Content-Type','application/json');
  var last=0;
  xhr.onprogress=function(){
    var chunk=xhr.responseText.substring(last);
    last=xhr.responseText.length;
    chunk.split('\\n').forEach(function(line){
      if(!line.startsWith('data:'))return;
      var d=line.slice(5).trim();
      if(d==='[DONE]'){busy=false;var c=document.getElementById('cur');if(c)c.remove();return;}
      try{
        var j=JSON.parse(d);
        var t=(j.choices&&j.choices[0].delta&&j.choices[0].delta.content)||'';
        if(t){
          var c=document.getElementById('cur');
          if(c){c.insertAdjacentText('beforebegin',t);}
          else{ad.textContent+=t;}
          window.scrollTo(0,document.body.scrollHeight);
        }
      }catch(e){}
    });
  };
  xhr.onload=function(){busy=false;};
  xhr.onerror=function(){ad.textContent='Error';busy=false;};
  xhr.send(JSON.stringify({msg:txt}));
}
document.getElementById('btn').ontouchend=function(e){e.preventDefault();send();};
document.getElementById('btn').onclick=send;
document.getElementById('inp').onkeydown=function(e){if(e.keyCode===13){e.preventDefault();send();}};
</script></body></html>"""

@app.route("/")
def index(): return HTML

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("msg","")
    payload = json.dumps({
        "messages":[
            {"role":"system","content":SYSTEM},
            {"role":"user","content":msg}
        ],
        "max_tokens":150,
        "stream":True,
        "temperature":0.7
    }).encode()
    def generate():
        try:
            req = urllib.request.Request(
                "http://127.0.0.1:8080/v1/chat/completions",
                data=payload,
                headers={"Content-Type":"application/json"}
            )
            with urllib.request.urlopen(req, timeout=300) as resp:
                for line in resp:
                    yield line.decode()
        except Exception as e:
            yield "data: [DONE]\n\n"
    return Response(generate(), content_type="text/event-stream",
                    headers={"Cache-Control":"no-cache","X-Accel-Buffering":"no"})

if __name__=="__main__":
    print("AETHER en http://127.0.0.1:5000")
    app.run(host="0.0.0.0",port=5000,threaded=True)
