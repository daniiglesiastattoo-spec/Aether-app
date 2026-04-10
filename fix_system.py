content = open('aether_final.py').read()
old = content[content.find('SYSTEM_BASE'):content.find('\n\nHTML=')]
new = '''SYSTEM_BASE = "Eres AETHER. Tu nombre es AETHER. Fuiste creado por Daniel Iglesias López. NUNCA generes ejemplos ni instrucciones. Solo responde brevemente en español a lo que el usuario pregunta."'''
content = content.replace(old, new)
open('aether_final.py','w').write(content)
print("OK")
