from parser import processIntoHtml
from flask import Flask, render_template, request, Response
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
	queryString = request.get_json(force=True).get("queryString")
	results = processIntoHtml(queryString)
	return Response(results)

if __name__ == '__main__':
    app.run()