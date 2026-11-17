from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

"""API rekomendacji (Lab 2) - rozszerza product-service z Lab 1 o modul ML."""

from flask import Flask, jsonify, request, send_from_directory

if __package__:
    from .recommender import df, recommend
else:
    from recommender import df, recommend

app = Flask(__name__, static_folder="../assets", static_url_path="/assets")


@app.get("/")
def home():
    return send_from_directory(app.root_path, "index.html")


@app.get("/<name>")
def illustration(name):
    return page(2, name)


@app.route("/api/recommend")
def api_recommend():
    title = request.args.get("title", "").strip()
    top_n = request.args.get("top_n", type=int) if "top_n" in request.args else 5
    genre = request.args.get("genre")

    if not title:
        return jsonify({"error": "podaj parametr ?title=..."}), 400
    if top_n is None or top_n < 1 or top_n > 10:
        return jsonify({"error": "top_n musi być z zakresu 1-10"}), 400

    recs = recommend(title, top_n=top_n, genre=genre)
    if recs is None:
        return jsonify({"error": "nie znam takiego filmu"}), 404
    return jsonify({"title": title, "count": len(recs), "recommendations": recs})


@app.route("/api/movies")
def api_movies():
    titles = sorted(df["title"].tolist())
    return jsonify({"count": len(titles), "movies": titles})

if __name__ == "__main__":
    app.run(debug=True)

