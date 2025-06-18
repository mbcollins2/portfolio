import os
import tomllib
import markdown
import frontmatter
from datetime import datetime
from markupsafe import Markup
# from flask_caching import Cache
from flask import Flask, render_template

from utils.helpers import (
    markdown_add_expandable_images,
    markdown_link_formatting,
)

# parse toml config file
with open("pyproject.toml", "rb") as f:
    config = tomllib.load(f)


# parse projects
PROJECTS_DIR = "src/portfolio/templates/pages/projects"
PROJECTS_IMAGE_DIR = "../../static/images/project_cards"

project_data = dict()
for project_filename in os.listdir(PROJECTS_DIR):
    if project_filename.endswith(".md"):
        project_slug = project_filename[:-3].replace("_","-")

        project_data[project_slug] = dict()

        with open(os.path.join(PROJECTS_DIR, project_filename), "r") as f:
            project_file = frontmatter.load(f)

        project_content = markdown.markdown(project_file.content)
        project_content = markdown_add_expandable_images(project_content)
        project_content = markdown_link_formatting(
            project_content,
            class_names=["project-body-link"]
        )

        project_data[project_slug]["project_metadata"] = project_file.metadata
        project_data[project_slug]["project_content"] = project_content
        project_data[project_slug]["project_image"] = os.path.join(PROJECTS_IMAGE_DIR, f"{project_filename[:-3]}.png")

project_list = [{"title": x, "date": project_data[x]['project_metadata']['publish_month_year']} for x in project_data]
sorted_project_list = [x['title'] for x in sorted(project_list, key=lambda x: datetime.strptime(x['date'], '%B %Y'), reverse=True)]


app = Flask(__name__)
# cache = Cache(app, config={"CACHE_TYPE": "SimpleCache"})


@app.context_processor
def context():
    return dict(
        version = config["project"]["version"],
        current_year = datetime.now().year
    )


@app.route("/")
# @cache.cached(timeout=60)
def home():
    start_date = datetime(2016, 6, 13)
    yoe = int((datetime.now() - start_date).days // 365.25)
    return render_template("pages/home.html", yoe=yoe)


@app.route("/projects")
# @cache.cached(timeout=60)
def projects():

    return render_template(
        "pages/projects.html",
        project_list=sorted_project_list,
        project_data=project_data
    )


@app.route("/projects/<slug>")
# @cache.cached(timeout=60)
def project_page(slug):
    return render_template(
        "pages/project_page.html",
        project_content=Markup(project_data[slug]["project_content"]),
        project_metadata=project_data[slug]["project_metadata"]
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
