from queryParser import processIntoHtml
from flask import Flask, render_template, send_from_directory, request, Response
from flask_cors import CORS

import json
app = Flask(__name__, static_url_path='', static_folder='app/build')

# Enable CORS for all domains on all routes
CORS(app)

@app.route("/react", methods=["GET"])
def indexReact():
	return send_from_directory(app.static_folder, 'index.html')

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
	results = processIntoHtml(queryString)

	return Response(json.dumps(results))

if __name__ == '__main__':
    app.run()