from pathlib import Path

from flask import Flask, jsonify, render_template, request

VERSION = (Path(__file__).parent / "VERSION").read_text().strip()


def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _validate(data, require_all):
    """Return an error message, or None if the data is fine."""
    if require_all and ("name" not in data or "price" not in data):
        return "name and price are required"
    if "name" in data:
        if not isinstance(data["name"], str) or not data["name"].strip():
            return "name must be a non-empty text"
    if "price" in data:
        if not _is_number(data["price"]) or data["price"] < 0:
            return "price must be a number, 0 or more"
    return None


def create_app():
    app = Flask(__name__)
    products = {}  # kept in memory: resets when the app restarts
    counter = {"next": 1}

    @app.get("/")
    def index():
        return render_template("index.html", version=VERSION)

    @app.get("/health")
    def health():
        return jsonify(status="ok", version=VERSION)

    @app.get("/products")
    def list_products():
        return jsonify(list(products.values()))

    @app.post("/products")
    def add_product():
        data = request.get_json(silent=True) or {}
        error = _validate(data, require_all=True)
        if error:
            return jsonify(error=error), 400
        pid = counter["next"]
        counter["next"] += 1
        products[pid] = {"id": pid, "name": data["name"].strip(), "price": data["price"]}
        return jsonify(products[pid]), 201

    @app.put("/products/<int:pid>")
    def update_product(pid):
        if pid not in products:
            return jsonify(error="product not found"), 404
        data = request.get_json(silent=True) or {}
        error = _validate(data, require_all=False)
        if error:
            return jsonify(error=error), 400
        if "name" in data:
            products[pid]["name"] = data["name"].strip()
        if "price" in data:
            products[pid]["price"] = data["price"]
        return jsonify(products[pid])

    @app.delete("/products/<int:pid>")
    def delete_product(pid):
        if products.pop(pid, None) is None:
            return jsonify(error="product not found"), 404
        return "", 204

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
