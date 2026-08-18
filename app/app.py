from flask import Flask, jsonify
import os

app = Flask(__name__)

# النسخة دي هنغيرها لاحقًا عشان نشوف ArgoCD بيطبق التغيير تلقائيًا
VERSION = os.environ.get("APP_VERSION", "v1")

@app.route("/")
def home():
    return jsonify({
        "message": "Hello from GitOps demo app!",
        "version": VERSION
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
