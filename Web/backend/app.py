# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from logic import build_graph_and_path

app = Flask(__name__)
CORS(app)

@app.route("/simulate", methods=["POST"])
def simulate():
    data = request.get_json()
    start = data.get("start")
    end = data.get("end")
    path = build_graph_and_path(start, end)
    if path:
        return jsonify({"success": True, "path": path})
    else:
        return jsonify({"success": False, "message": "未找到路径"}), 404

if __name__ == "__main__":
    # 在开发环境下默认监听 127.0.0.1:5000
    app.run(debug=True)
