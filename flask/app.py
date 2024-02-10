from flask import Flask, render_template

app = Flask(__name__)

@app.route("/index.html", methods=["GET"])
def index():
    return render_template(
        "index.html",
        title="Homepage",
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)