from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def index():
    return "<h1 style='color:green'>FUNCIONA</h1><p>El servidor responde.</p>"

@app.route("/test")
def test():
    return jsonify({"respuesta": "hola desde AETHER"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
