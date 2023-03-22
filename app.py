from flask import Flask, jsonify, render_template, request

from gpt import GPTStructuredReporting

app = Flask(__name__)

# Global variable to store the API key
api_key = None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/reports")
def reports():
    return render_template("reports.html")


@app.route("/process", methods=["POST"])
def process():
    report = request.form["report"]
    api_key = request.form["api_key"]
    if report == "test":
        response = jsonify({"test": "yes"})
        response.headers["Content-Type"] = "application/json"
        return response
    gpt = GPTStructuredReporting(api_key, "static/report_templates.json")
    structured_report = gpt(report)
    response = jsonify(structured_report)
    response.headers["Content-Type"] = "application/json"
    return response


if __name__ == "__main__":
    app.run(debug=True)
