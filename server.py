from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route("/activities")
def activities():
    with open("static/test.json") as file:
        data = json.load(file)
        return json.dumps(data)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port="8081")
