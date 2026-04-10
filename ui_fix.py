import re
content = open('aether_v2.py').read()

new_js = """
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
    lm.innerHTML = '<div class=\\"tag\\">AETHER</div>pensando...';
    chat.appendChild(lm);
    chat.scrollTop = chat.scrollHeight;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/chat', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
      var d = JSON.parse(xhr.responseText);
      lm.innerHTML = '<div class=\\"tag\\">AETHER</div>' + d.output.replace(/\\n/g,'<br>');
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
"""

content = re.sub(r'<script>.*?</script>', '<script>' + new_js + '</script>', content, flags=re.DOTALL)
open('aether_v2.py','w').write(content)
print("OK")
