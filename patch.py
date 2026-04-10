c = open('aether_final.py').read()
old = '''    def generate():
        full_response = []
        try:
            req = urllib.request.Request(
                "http://127.0.0.1:8080/v1/chat/completions",
                data=payload,
                headers={"Content-Type":"application/json"}
            )
            with urllib.request.urlopen(req, timeout=300) as resp:
                for line in resp:
                    decoded = line.decode()
                    if decoded.startswith("data:"):
                        try:
                            j = json.loads(decoded[5:].strip())
                            t = (j.get("choices",[{}])[0]
                                  .get("delta",{})
                                  .get("content",""))
                            if t:
                                full_response.append(t)
                        except: pass
                    yield decoded
        except Exception as e:
            yield "data: [DONE]\\n\\n"
        # Guardar en memoria
        try:
            mind.update(msg, "".join(full_response), session)
        except: pass

    return Response(generate(),
                    content_type="text/event-stream",
                    headers={"Cache-Control":"no-cache",
                             "X-Accel-Buffering":"no"})'''

new = '''    try:
        payload2 = json.dumps({
            "messages":[
                {"role":"system","content":system},
                {"role":"user","content":msg}
            ],
            "max_tokens":150,
            "stream":False,
            "temperature":0.7
        }).encode()
        req = urllib.request.Request(
            "http://127.0.0.1:8080/v1/chat/completions",
            data=payload2,
            headers={"Content-Type":"application/json"}
        )
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read().decode())
            answer = result["choices"][0]["message"]["content"]
        try:
            mind.update(msg, answer, session)
        except: pass
        return jsonify({"a": answer})
    except Exception as e:
        return jsonify({"a": "Error: "+str(e)})'''

c = c.replace(old, new)
open('aether_final.py','w').write(c)
print("OK" if new in c else "NO ENCONTRADO")
