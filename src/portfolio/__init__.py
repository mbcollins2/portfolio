import tomllib
from flask import Flask, render_template
from flask_caching import Cache

# parse toml config file
with open("pyproject.toml", "rb") as f:
    config = tomllib.load(f)


app = Flask(__name__)
cache = Cache(app, config={"CACHE_TYPE": "SimpleCache"})


@app.context_processor
def context():
    return dict(
        version = config["project"]["version"],
    )


@app.route("/")
# @cache.cached(timeout=60)
def home():
    return render_template("pages/home.html")


@app.route("/projects")
# @cache.cached(timeout=60)
def projects():
    return render_template("pages/projects.html")


@app.route("/projects/portfolio-website")
# @cache.cached(timeout=60)
def project_page():
    return render_template("pages/projects/portfolio_website.html")


# TODO - set up slugs for project page templates
# @app.route("/projects/<slug>")
# # @cache.cached(timeout=60)
# def project_page(slug):
#     return render_template("pages/projects/portfolio_website.html", slug=slug)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
