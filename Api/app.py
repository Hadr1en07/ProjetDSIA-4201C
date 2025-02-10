import re
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import os

app = Flask(__name__, template_folder="frontend")

# Configuration de MongoDB (avec authSource)
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "mongodb://root:example@db:27017/nintendo?authSource=admin")
mongo = PyMongo(app)

@app.route("/")
def index():
    carousel_games = list(mongo.db.games.find({"image": {"$ne": None}}).limit(5))
    for game in carousel_games:
        game['_id'] = str(game['_id'])
    return render_template("index.html", carousel_games=carousel_games)

@app.route("/search", methods=["GET"])
def search():
    """
    Recherche des jeux dans MongoDB de manière insensible à la casse.
    """
    query = request.args.get("q", "")
    games = []
    if query:
        regex = re.compile(query, re.IGNORECASE)
        games = list(mongo.db.games.find({"title": regex}))
        for game in games:
            game['_id'] = str(game['_id'])
    return render_template("search.html", query=query, games=games)

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

@app.route("/stats")
def stats():
    """
    Calcule diverses statistiques à partir des documents stockés dans MongoDB.
    """
    games = list(mongo.db.games.find())
    
    # Statistiques par genre
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
            pass

    # Statistiques par classification d'âge
    age_rating_counts = {}
    for game in games:
        rating = game.get("age_rating", "N/A")
        if rating and rating != "N/A":
            age_rating_counts[rating] = age_rating_counts.get(rating, 0) + 1

    return render_template("stats.html",
                           genre_counts=genre_counts,
                           price_buckets=price_buckets,
                           age_rating_counts=age_rating_counts)

@app.route("/api/games", methods=["GET"])
def api_games():
    games = list(mongo.db.games.find())
    for game in games:
        game['_id'] = str(game['_id'])
    return jsonify(games)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8050, debug=True)