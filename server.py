from flask import Flask, render_template
import json

app = Flask(__name__, static_url_path="/static")

@app.route("/activities/<grade>", methods = ["GET"])
def activities(grade):
    with open("activities/" + grade + ".json") as file:
        data = json.load(file)
        return json.dumps(data)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port="8081")
