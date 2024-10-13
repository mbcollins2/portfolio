from flask import Flask, render_template 
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})


@app.route("/")
@cache.cached(timeout=60)
def home():
    return render_template("pages/home.html")


@app.route("/projects")
def projects():
    return render_template("pages/projects.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
