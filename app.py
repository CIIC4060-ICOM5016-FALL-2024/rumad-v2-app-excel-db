from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
from dal.handler.handler import Handler

app = Flask(__name__)
CORS(app)

handler = Handler()


@app.route("/excel_db")
def excel_db():
    return jsonify(f"Welcome")


@app.route("/")
def home():
    return redirect("/excel_db", code=302)


###################### CLASS ######################


@app.route("/excel_db/class", methods=["GET", "POST"])
def classes():
    if request.method == "GET":
        return handler.get_classes()
    if request.method == "POST":
        return handler.post_class(request.json)


@app.route("/excel_db/class/<int:cid>", methods=["GET", "PUT", "DELETE"])
def classes_by_id(cid):
    if request.method == "GET":
        return handler.get_class_by_id(cid)
    if request.method == "PUT":
        return handler.put_class_by_id(cid, request.json)
    if request.method == "DELETE":
        return handler.delete_class_by_id(cid)


#################### REQUISITE ####################


@app.route("/excel_db/requisite", methods=["GET", "POST"])
def requisites():
    if request.method == "GET":
        return handler.get_requisites()
    if request.method == "POST":
        return handler.post_requisite(request.json)


@app.route(
    "/excel_db/requisite/<int:classid>/<int:reqid>", methods=["GET", "PUT", "DELETE"]
)
def requisites_by_id(classid, reqid):
    if request.method == "GET":
        return handler.get_requisite_by_id(classid, reqid)
    if request.method == "PUT":
        return handler.put_requisite_by_classid_reqid(classid, reqid, request.json)
    if request.method == "DELETE":
        return handler.delete_requisite(classid, reqid)


##################### SECTION #####################


@app.route("/excel_db/section", methods=["GET", "POST"])
def sections():
    if request.method == "GET":
        return handler.get_sections()
    if request.method == "POST":
        return handler.post_section(request.json)


@app.route("/excel_db/section/<int:sid>", methods=["GET", "PUT", "DELETE"])
def sections_by_id(sid):
    if request.method == "GET":
        return handler.get_section_by_id(sid)
    if request.method == "PUT":
        return handler.put_section_by_id(sid, request.json)
    if request.method == "DELETE":
        return handler.delete_section(sid)


##################### MEETING #####################


@app.route("/excel_db/meeting", methods=["GET", "POST"])
def meetings():
    if request.method == "GET":
        return handler.get_meetings()
    if request.method == "POST":
        return handler.post_meeting(request.json)


@app.route("/excel_db/meeting/<int:mid>", methods=["GET", "PUT", "DELETE"])
def meetings_by_id(mid):
    if request.method == "GET":
        return handler.get_meeting_by_id(mid)
    if request.method == "PUT":
        return handler.put_meeting_by_id(mid, request.json)
    if request.method == "DELETE":
        return handler.delete_meeting(mid)


###################### ROOM ######################


@app.route("/excel_db/room", methods=["GET", "POST"])
def rooms():
    if request.method == "GET":
        return handler.get_rooms()
    if request.method == "POST":
        return handler.post_rooms(request.json)


@app.route("/excel_db/room/<int:rid>", methods=["GET", "PUT", "DELETE"])
def rooms_by_id(rid):
    if request.method == "GET":
        return handler.get_room_by_id(rid)
    if request.method == "PUT":
        return handler.put_room_by_id(rid, request.json)
    if request.method == "DELETE":
        return handler.delete_room_by_id(rid)


################ LOCAL STATISTICS ################


@app.route("/excel_db/room/<string:building>/capacity", methods=["POST"])
def top_rooms_by_capacity(building):
    return handler.top_room_capacity_by_building(building)


@app.route("/excel_db/room/<int:rid>/<string:stat>", methods=["POST"])
def local_statistics_by_id(rid, stat):
    if stat == "ratio":
        return handler.top_ratio_rooms(rid)
    elif stat == "classes":
        return handler.top_classes_per_room(rid)
    else:
        return jsonify(f"LocalStatistic: {type} does not exist!"), 404


@app.route("/excel_db/classes/<string:year>/<string:semester>", methods=["POST"])
def top_classes_per_semester_year(year, semester):
    return handler.top_classes_per_semester(year, semester)


################ GLOBAL STATISTICS ###############


@app.route("/excel_db/most/<string:stat>", methods=["POST"])
def most_global_statistics(stat):
    if stat == "meeting":
        return handler.top_meeting()
    elif stat == "prerequisite":
        return handler.top_pre_requisite()
    else:
        return jsonify(f"GlobalStatistic: {stat} does not exist!"), 404


@app.route("/excel_db/least/classes", methods=["POST"])
def least_global_statistics():
    return handler.top_least_classes()


@app.route("/excel_db/section/year", methods=["POST"])
def total_sections_per_year():
    return handler.total_sections()


if __name__ == "__main__":
    app.run(debug=True)
