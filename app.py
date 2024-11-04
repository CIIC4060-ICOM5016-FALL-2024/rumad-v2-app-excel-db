from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
from handler.handler import Handler

app = Flask(__name__)
CORS(app)

handler = Handler()

@app.route("/excel_db")
def excel_db():
    return "Welcome to the Excel DB page!"

@app.route("/")
def home():
    return redirect("/excel_db", code=302)

###################### CLASS ######################

@app.route('/excel_db/class', methods=["GET", "POST"])
def handleClasses():
    return

@app.route('/excel_db/class/<int:cid>', methods=["GET", "PUT", "DELETE"])
def handleClassesByID(cid):
    return

#################### REQUISITE ####################

@app.route('/excel_db/requisite', methods=["GET", "POST"])
def handleRequisites():
    return

@app.route('/excel_db/requisite/<int:reqid>', methods=["GET", "PUT", "DELETE"])
def handleRequisitesByID(reqid):
    return

##################### SECTION #####################

@app.route('/excel_db/section', methods=["GET", "POST"])
def handleSections():
    return

@app.route('/excel_db/section/<int:sid>', methods=["GET", "PUT", "DELETE"])
def handleSectionsByID(sid):
    return

##################### MEETING #####################

@app.route('/excel_db/meeting', methods=["GET", "POST"])
def handleMeetings():
    return

@app.route('/excel_db/meeting/<int:mid>', methods=["GET", "PUT", "DELETE"])
def handleMeetingsByID(mid):
    return

###################### ROOM ######################

@app.route('/excel_db/room', methods=["GET", "POST"])
def handleRooms():
    return

@app.route('/excel_db/room/<int:rid>', methods=["GET", "PUT", "DELETE"])
def handleRoomsByID(rid):
    return

################ LOCAL STATISTICS ################

@app.route('/excel_db/room/<int:rid>/<string:type>', methods=["POST"])
def handleLocalStatisticsByID(rid, type):
    if not request.is_json:
        return jsonify(f"The request does not contain JSON data"), 400

    if type == 'capacity':
        return
    elif type == 'ratio':
        return
    else:
        return jsonify(f"LocalStatistic: {type} does not exist!"), 404

@app.route('/excel_db/classes/<int:rid>/<varchar:semester>', methods=["POST"])
def handleLocalStatistics(rid, term):
    if not request.is_json:
        return jsonify(f"The request does not contain JSON data"), 400

    return

################ GLOBAL STATISTICS ###############

@app.route('/excel_db/most/<string:type>', methods=["POST"])
def handleMostGlobalStatistics(type):
    if not request.is_json:
        return jsonify(f"The request does not contain JSON data"), 400

    if type == 'meeting':
        return
    elif type == 'prerequisite':
        return
    else:
        return jsonify(f"GlobalStatistic: {type} does not exist!"), 404

@app.route('/excel_db/least/<string:type>', methods=["POST"])
def handleLeastGlobalStatistics(type):
    if not request.is_json:
        return jsonify(f"The request does not contain JSON data"), 400

    if type == 'classes':
        return
    else:
        return jsonify(f"GlobalStatistic: {type} does not exist!"), 404

@app.route('/excel_db/section/year', methods=["POST"])
def handleGlobalStatistics():
    if not request.is_json:
        return jsonify(f"The request does not contain JSON data"), 400

    return


if __name__ == '__main__':
    app.run(debug=True)