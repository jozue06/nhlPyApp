import json
import os

from flask import Flask, Response, render_template, request, send_from_directory
from flask_cors import CORS

from queryParser import processIntoHtml, processQueryStringJSON

app = Flask(__name__, static_url_path="/static", static_folder="static")

# Enable CORS for all domains on all routes
CORS(app)


@app.route("/react", methods=["GET"])
def indexReact():
    return send_from_directory("../frontend/build", "index.html")


@app.route("/assets/<path:filename>", methods=["GET"])
def reactAssets(filename):
    return send_from_directory("../frontend/build/assets", filename)


@app.route("/", methods=["GET"])
def indexHtml():
    return render_template("index.html")


@app.route("/api/html/search", methods=["POST"])
def searchHtml():
    queryString = request.form.get("queryString")
    results = processIntoHtml(queryString)
    return render_template("index.html", results=results)


@app.route("/api/json/search", methods=["POST"])
def searchJson():
    queryString = request.get_json(force=True).get("queryString")
    results = processQueryStringJSON(queryString)
    return Response(json.dumps(results), content_type='application/json')


if __name__ == "__main__":
    # Use PORT environment variable for Heroku, fallback to 5001 for local development
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
