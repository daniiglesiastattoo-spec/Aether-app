c = open('aether_final.py').read()
old = "return redirect('/')"
new = """return '''<html><head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0;url=/">
</head><body>Procesando...</body></html>'''"""
c = c.replace(old, new)
open('aether_final.py','w').write(c)
print("OK" if "Procesando" in c else "ERROR")
