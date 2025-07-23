from flask import Flask, jsonify, request
from flask_cors import CORS
from logic import build_graph_and_paths

app = Flask(__name__)
CORS(app)

@app.route("/simulate", methods=["POST"])
def simulate():
    data = request.get_json()
    start = data.get("start")
    end = data.get("end")
    paths = build_graph_and_paths(start, end)
    if paths:
        return jsonify({"success": True, "paths": paths})
    else:
        return jsonify({"success": False, "message": "未找到路径"}), 404

if __name__ == "__main__":
    app.run(debug=True)
