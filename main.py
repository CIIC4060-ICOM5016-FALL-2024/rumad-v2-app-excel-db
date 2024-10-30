from flask import Flask, jsonify, request, redirect
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/excel_db.com")
def excel_db():
    return "Welcome to the Excel DB page!"

@app.route("/")
def home():
    return redirect("/excel_db.com", code=302)

# Routes --------------------------------------------------------------+
# TODO POST /<entity>

# TODO GET /<entity>

# TODO GET /<entity>/<id>

# TODO PUT /<entity>/<id>

# TODO Delete /<entity>/<id>

# Routes Local Statistics ----------------------------------------------+
# TODO /room/<id>/capacity

# TODO /room/<id>/ratio

# TODO /room/<id>/classes

# TODO /classes/<year>/<semester>

# Routes Global Statistics ----------------------------------------------+
# TODO /most/meeting

# TODO /most/prerequisite

# TODO /least/classes

# TODO /section/year

if __name__ == '__main__':
    app.run(debug=True)