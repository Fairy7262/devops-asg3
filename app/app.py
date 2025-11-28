from flask import Flask, request, render_template
from db import init_db, add_msg, get_msgs

app = Flask(__name__)

init_db()

@app.route("/")
def home():
    msgs = get_msgs()
    return render_template("index.html", msgs=msgs)

@app.route("/add", methods=["POST"])
def add():
    msg = request.form.get("msg")
    add_msg(msg)
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
