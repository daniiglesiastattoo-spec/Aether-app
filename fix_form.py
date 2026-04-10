c = open('aether_final.py').read()
old = '''<form method="POST" action="/enviar">
<input id="inp" name="msg" type="text" placeholder="Escribe aqui..." autocomplete="off">
<button id="btn" type="submit">&#9654;</button>
</form>'''
new = '''<form method="POST" action="/enviar" id="frm">
<input id="inp" name="msg" type="text" placeholder="Escribe aqui..." autocomplete="off">
<input type="submit" value="ENVIAR" style="padding:12px 16px;background:#00e5b0;color:#000;border:none;border-radius:8px;font-size:14px;font-weight:bold;">
</form>'''
print("OK" if old in c else "NO ENCONTRADO")
c = c.replace(old, new)
open('aether_final.py','w').write(c)
