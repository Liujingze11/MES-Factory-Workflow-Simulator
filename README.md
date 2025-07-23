# 🏭 MES-Factory-Workflow-Simulator

**MES-Factory-Workflow-Simulator** is a lightweight factory workflow simulator designed for visualizing and querying logistics paths in a manufacturing environment. It is built with a Flask backend and a static HTML frontend, ideal for prototyping MES (Manufacturing Execution System) or digital twin scenarios.

---

## 📁 Project Structure

```

MES-Factory-Workflow-Simulator/
├── backend/                      # Flask backend server
│   ├── app.py                   # Entry point with /simulate API
│   └── logic.py                 # Core logic: node graph and pathfinding (DFS)
│
├── frontend/                    # Frontend assets (static)
│   ├── images/                  # Image resources
│   │   ├── factory\_line.png
│   │   └── forklift.png
│   └── factory\_simulator\_oop.html  # Visual simulation interface
│
├── .gitignore                   # Git ignore rules
├── README.md                    # Project documentation

````

---

## 🚀 Getting Started

### 1️⃣ Install Dependencies

```bash
pip install flask flask-cors
````

---

### 2️⃣ Run the Backend Server

```bash
cd backend
python app.py
```

The API will be available at:
`http://127.0.0.1:5000/simulate`

---

### 3️⃣ Test the API

Use `curl`, Postman or any HTTP client:

```bash
curl -X POST http://127.0.0.1:5000/simulate \
-H "Content-Type: application/json" \
-d '{"start": "A70 收货区", "end": "生产线"}'
```

**Response example:**

```json
{
  "success": true,
  "paths": [
    ["A70 收货区", "A70 转包区", "A70 转运", "大件立体库", "大件备货站", ...],
    ...
  ]
}
```

---

### 4️⃣ View the Frontend

Open the following file directly in your browser:

```
frontend/factory_simulator_oop.html
```

> This page displays a static factory layout. You can enhance it to highlight paths dynamically based on the API response.

---

## 💡 Features

* ✔️ Object-oriented graph structure for logistics simulation
* 🔁 Multi-branch DFS pathfinding algorithm
* 🔗 API-ready: easy to integrate with visual dashboards
* 🔍 Designed for smart factory / MES system prototyping

---

## 🧩 Nodes Covered

The internal graph includes (but is not limited to):

* A60 flow: 收货区 → 地堆 → MSU → 超市1.0 → 生产线
* A70 flow: 收货区 → 转包 → 转运 → 多分支（立体库、地堆、小件站点等）
* Special areas: 小件拆垛站、小件异常处理站、SKLTOVERSIZE货区, etc.

---

## 🛠️ Future Plans

* [ ] Interactive frontend with path highlighting
* [ ] Node metadata popups
* [ ] Graph editor for dynamic node creation
