content = open('aether_v2.py').read()
old = "async function send(){"
new = "async function send(){ console.log('enviando...');"
content = content.replace(old, new)

old = "btn.addEventListener('click',send);"
new = """btn.onclick = function(){ send(); };
btn.addEventListener('click',send);"""
content = content.replace(old, new)

open('aether_v2.py','w').write(content)
print("OK")
