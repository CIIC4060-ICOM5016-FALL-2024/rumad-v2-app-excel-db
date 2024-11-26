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

""" USER CRUD ROUTES """
@app.route("/excel_db/user", methods=["GET"])
def get_user():
    return handler.get_users()

@app.route("/excel_db/user", methods=["POST"])
def post_user():
    return handler.post_user(request.json)

@app.route("/excel_db/user/<int:uid>", methods=["GET"])
def get_user_by_id(uid):
    return handler.get_user_by_id(uid)

@app.route("/excel_db/user/<string:username>", methods=["GET"])
def get_user_by_username(username):
    return handler.get_user_by_name(username)

@app.route("/excel_db/user/<int:uid>", methods=["PUT"])
def put_user_by_id(uid):
    return handler.put_user_by_id(uid, request.json)

@app.route("/excel_db/user/<int:uid>", methods=["DELETE"])
def delete_user_by_id(uid):
    return handler.delete_user_by_id(uid)

@app.route("/excel_db/user/login", methods=["POST"])
def login_user():
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid content type. JSON required."}), 400

        data = request.get_json(silent=True)
        if data is None:
            return jsonify({"error": "Invalid JSON payload"}), 400

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        response_data, status_code = handler.validate_user_login(username, password)
        return jsonify(response_data), status_code
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


""" CLASS CRUD ROUTES """
@app.route("/excel_db/class", methods=["GET"])
def get_classes():
    return handler.get_classes()

@app.route("/excel_db/class", methods=["POST"])
def post_classes():
    return handler.post_class(request.json)

@app.route("/excel_db/class/<int:cid>", methods=["GET"])
def get_classes_by_id(cid):
    return handler.get_class_by_id(cid)

@app.route("/excel_db/class/<int:cid>", methods=["PUT"])
def put_classes_by_id(cid):
    return handler.put_class_by_id(cid, request.json)

@app.route("/excel_db/class/<int:cid>", methods=["DELETE"])
def delete_classes_by_id(cid):
    return handler.delete_class_by_id(cid)

""" REQUISITE CRUD ROUTES """
@app.route("/excel_db/requisite", methods=["GET"])
def get_requisites():
    return handler.get_requisites()

@app.route("/excel_db/requisite", methods=["POST"])
def post_requisites():
    return handler.post_requisite(request.json)

@app.route("/excel_db/requisite/<int:classid>/<int:reqid>", methods=["GET"])
def get_requisites_by_id(classid, reqid):
    return handler.get_requisite_by_id(classid, reqid)

@app.route("/excel_db/requisite/<int:classid>/<int:reqid>", methods=["PUT"])
def put_requisites_by_id(classid, reqid):
    return handler.put_requisite_by_classid_reqid(classid, reqid, request.json)

@app.route("/excel_db/requisite/<int:classid>/<int:reqid>", methods=["DELETE"])
def delete_requisites_by_id(classid, reqid):
    return handler.delete_requisite(classid, reqid)

""" SECTION CRUD ROUTES """
@app.route("/excel_db/section", methods=["GET"])
def get_sections():
    return handler.get_sections()

@app.route("/excel_db/section", methods=["POST"])
def post_sections():
    return handler.post_section(request.json)

@app.route("/excel_db/section/<int:sid>", methods=["GET"])
def get_sections_by_id(sid):
    return handler.get_section_by_id(sid)

@app.route("/excel_db/section/<int:sid>", methods=["PUT"])
def put_sections_by_id(sid):
    return handler.put_section_by_id(sid, request.json)

@app.route("/excel_db/section/<int:sid>", methods=["DELETE"])
def delete_sections_by_id(sid):
    return handler.delete_section(sid)

""" MEETINGS CRUD ROUTES """
@app.route("/excel_db/meeting", methods=["GET"])
def get_meetings():
    return handler.get_meetings()

@app.route("/excel_db/meeting", methods=["POST"])
def post_meetings():
    return handler.post_meeting(request.json)

@app.route("/excel_db/meeting/<int:mid>", methods=["GET"])
def get_meetings_by_id(mid):
    return handler.get_meeting_by_id(mid)

@app.route("/excel_db/meeting/<int:mid>", methods=["PUT"])
def put_meetings_by_id(mid):
    return handler.put_meeting_by_id(mid, request.json)

@app.route("/excel_db/meeting/<int:mid>", methods=["DELETE"])
def delete_meetings_by_id(mid):
    return handler.delete_meeting(mid)

""" ROOM CRUD ROUTES """
@app.route("/excel_db/room", methods=["GET"])
def get_rooms():
    return handler.get_rooms()

@app.route("/excel_db/room", methods=["POST"])
def post_rooms():
    return handler.post_rooms(request.json)

@app.route("/excel_db/room/<int:rid>", methods=["GET"])
def get_rooms_by_id(rid):
    return handler.get_room_by_id(rid)

@app.route("/excel_db/room/<int:rid>", methods=["PUT"])
def put_rooms_by_id(rid):
    return handler.put_room_by_id(rid, request.json)

@app.route("/excel_db/room/<int:rid>", methods=["DELETE"])
def delete_rooms_by_id(rid):
    return handler.delete_room_by_id(rid)

""" LOCAL STATISTICS ROUTES """
@app.route("/excel_db/room/<string:building>/capacity", methods=["POST"])
def top_rooms_by_capacity(building):
    return handler.top_room_capacity_by_building(building)

@app.route("/excel_db/room/<string:building>/ratio", methods=["POST"])
def top_rooms_by_ratio(building):
    return handler.top_ratio_rooms(building)

@app.route("/excel_db/room/<int:rid>/classes", methods=["POST"])
def local_statistics_by_id(rid):
        return handler.top_classes_per_room(rid)

@app.route("/excel_db/classes/<string:year>/<string:semester>", methods=["POST"])
def top_classes_per_semester_year(year, semester):
    return handler.top_classes_per_semester(year, semester)

""" GLOBAL STATISTICS ROUTES """
@app.route("/excel_db/most/meeting", methods=["POST"])
def most_meeting_global_statistics():
    return handler.top_meeting()

@app.route("/excel_db/most/prerequisite", methods=["POST"])
def most_prerequisite_global_statistics():
    return handler.top_pre_requisite()

@app.route("/excel_db/least/classes", methods=["POST"])
def least_global_statistics():
    return handler.top_least_classes()

@app.route("/excel_db/section/year", methods=["POST"])
def total_sections_per_year():
    return handler.total_sections()

if __name__ == "__main__":
    app.run(debug=True)
