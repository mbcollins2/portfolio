import os
import json
import tomllib
import markdown
import frontmatter
from datetime import datetime
from markupsafe import Markup
from flask_caching import Cache
from flask import Flask, render_template

# parse toml config file
with open("pyproject.toml", "rb") as f:
    config = tomllib.load(f)


PROJECTS_DIR = "src/portfolio/templates/pages/projects"


app = Flask(__name__)
# cache = Cache(app, config={"CACHE_TYPE": "SimpleCache"})


# TODO 
# load all projects in project directory
# parse all project metadata into a json with a name for the slug and then the metadata and content
# order descending by date

project_data = dict()
for project_filename in os.listdir(PROJECTS_DIR):
    if project_filename.endswith(".md"):
        project_slug = project_filename[:-3].replace("_","-")

        project_data[project_slug] = dict()

        with open(os.path.join(PROJECTS_DIR, project_filename), "r") as f:
            project_file = frontmatter.load(f)

        project_data[project_slug]["project_metadata"] = project_file.metadata
        project_data[project_slug]["project_content"] = markdown.markdown(project_file.content)

# print("project_data", project_data)

project_list = [{"title": x, "date": project_data[x]['project_metadata']['publish_month_year']} for x in project_data]
sorted_project_list = [x['title'] for x in sorted(project_list, key=lambda x: datetime.strptime(x['date'], '%B %Y'), reverse=True)]

# print("list", project_list)
# print("list", [x['title'] for x in sorted(project_list, key=lambda x: datetime.strptime(x['date'], '%B %Y'), reverse=True)])



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

    # TODO - get all of the projects in p

    return render_template("pages/projects.html")


@app.route("/projects/<slug>")
# @cache.cached(timeout=60)
def project_page(slug):

    # # load project markdown
    # project_markdown_path = os.path.join(PROJECTS_DIR, f'{slug}.md').replace("-","_")

    # with open(project_markdown_path, "r") as f:
    #     project_file = frontmatter.load(f)

    # project_metadata = project_file.metadata
    # project_content = markdown.markdown(project_file.content)

    return render_template(
        "pages/project_page.html", 
        # project_content=Markup(project_content),
        # project_metadata=project_metadata
        project_content=Markup(project_data[slug]["project_content"]),
        project_metadata=project_data[slug]["project_metadata"]
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
