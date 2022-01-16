from parser import process
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/", methods=["POST"])
def search():
	queryString = request.form.get("queryString")
	results = process(queryString)
	return render_template("index.html", results=results)

if __name__ == '__main__':
    app.run()