from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os
import re

app = Flask(__name__, template_folder="frontend")

# --- Configuration de MongoDB ---
# On se connecte avec l'URI défini dans l'environnement ou par défaut (MongoDB avec user:root et pwd:example sur le service "db")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://root:example@db:27017/nintendo?authSource=admin")
mongo = PyMongo(app)

# --- Route d'accueil ---
@app.route("/")
def index():
    # La page d'accueil affiche un message de bienvenue et un formulaire de recherche
    return render_template("index.html")

# --- Route de recherche ---
@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    games = []
    if query:
        # Recherche dans le titre (expression régulière insensible à la casse)
        regex = re.compile(query, re.IGNORECASE)
        games = list(mongo.db.games.find({"title": regex}))
        for game in games:
            game['_id'] = str(game['_id'])
    return render_template("search.html", query=query, games=games)

# --- Page de détail d'un jeu ---
@app.route("/game/<game_id>")
def game_detail(game_id):
    try:
        game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    except Exception as e:
        return "ID invalide", 400
    if game:
        game['_id'] = str(game['_id'])
        return render_template("game_detail.html", game=game)
    else:
        return "Jeu non trouvé", 404

# --- Page de statistiques ---
@app.route("/stats")
def stats():
    games = list(mongo.db.games.find())
    # Statistiques par genre (la valeur "genre" est au format "|action|adventure|")
    genre_counts = {}
    for game in games:
        genres = game.get("genre", "")
        if genres and genres != "N/A":
            cleaned = genres.strip("|")
            if cleaned:
                genre_list = cleaned.split("|")
                for genre in genre_list:
                    if genre:
                        genre_counts[genre] = genre_counts.get(genre, 0) + 1
    # Statistiques par prix
    price_buckets = {
        "Gratuit": 0,
        "Moins de 30": 0,
        "Entre 30 et 60": 0,
        "Plus de 60": 0,
    }
    for game in games:
        price_str = game.get("price", "N/A")
        try:
            price = float(price_str)
            if price == 0:
                price_buckets["Gratuit"] += 1
            elif price < 30:
                price_buckets["Moins de 30"] += 1
            elif price <= 60:
                price_buckets["Entre 30 et 60"] += 1
            else:
                price_buckets["Plus de 60"] += 1
        except:
            pass  # On ignore les valeurs non convertibles

    return render_template("stats.html", genre_counts=genre_counts, price_buckets=price_buckets)

# --- (Optionnel) API REST pour récupérer les jeux en JSON ---
@app.route("/api/games", methods=["GET"])
def api_games():
    games = list(mongo.db.games.find())
    for game in games:
        game['_id'] = str(game['_id'])
    return jsonify(games)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8050, debug=True)