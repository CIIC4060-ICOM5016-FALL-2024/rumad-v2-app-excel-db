from flask import Flask, jsonify, request, redirect
from flask_cors import CORS

from model.user_model import UserModel
from model.class_model import ClassModel
from model.requisite_model import RequisiteModel
from model.section_model import SectionModel
from model.meeting_model import MeetingModel
from model.room_model import RoomModel
from model.statistics_model import StatisticsModel
from model.syllabus_model import SyllabusModel

app = Flask(__name__)
CORS(app)

@app.route('/excel_db')
def excel_db():
    return jsonify(f"Welcome")

@app.route("/")
def home():
    return redirect('/excel_db', code=302)

""" USER CRUD ROUTES """
@app.route("/excel_db/user", methods=["POST"])
def post_user():
    handler = UserModel()
    return handler.post_user(request.json)

@app.route("/excel_db/user/<int:uid>", methods=["GET"])
def get_user_by_id(uid):
    handler = UserModel()
    return handler.get_user_by_id(uid)

@app.route("/excel_db/user/<string:username>", methods=["GET"])
def get_user_by_username(username):
    handler = UserModel()
    return handler.get_user_by_username(username)

@app.route("/excel_db/user/email/<string:email>", methods=["GET"])
def get_user_by_email(email):
    handler = UserModel()
    return handler.get_user_by_email(email)

@app.route("/excel_db/user/<int:uid>", methods=["PUT"])
def put_user_by_id(uid):
    handler = UserModel()
    return handler.put_user_by_id(uid, request.json)

@app.route("/excel_db/user/<string:username>", methods=["PUT"])
def put_user_by_username(username):
    handler = UserModel()
    return handler.put_user_by_username(username, request.json)

@app.route("/excel_db/user/email/<string:email>", methods=["PUT"])
def put_user_by_email(email):
    handler = UserModel()
    return handler.put_user_by_email(email, request.json)

@app.route("/excel_db/user/<int:uid>", methods=["DELETE"])
def delete_user_by_id(uid):
    handler = UserModel()
    return handler.delete_user_by_id(uid)

@app.route("/excel_db/user/<string:username>", methods=["DELETE"])
def delete_user_by_username(username):
    handler = UserModel()
    return handler.delete_user_by_username(username)

@app.route("/excel_db/user/email/<string:email>", methods=["DELETE"])
def delete_user_by_email(email):
    handler = UserModel()
    return handler.delete_user_by_email(email)

@app.route("/excel_db/user/login", methods=["POST"])
def login_user():
    login_data = request.get_json(silent=True)
    handler = UserModel()
    return handler.validate_user_login(login_data)

""" CLASS CRUD ROUTES """

@app.route('/excel_db/class', methods=['GET', 'POST'])
def handle_classes():
    handler = ClassModel()
    if request.method == 'GET':
        return handler.get_all_classes()
    elif request.method == 'POST':
        return handler.post_class(request.json)
    else:
        return jsonify(f"Error: {request.method} Method Not Allowed"), 405

@app.route('/excel_db/class/<int:cid>', methods=['GET', 'PUT', 'DELETE'])
def handle_classes_by_id(cid):
    handler = ClassModel()
    if request.method == 'GET':
        return handler.get_class_by_id(cid)
    elif request.method == 'PUT':
        return handler.put_class_by_id(cid, request.json)
    elif request.method == 'DELETE':
        return handler.delete_class_by_id(cid)
    else:
        return jsonify(f"Error: {request.method} Method Not Allowed"), 405

""" REQUISITE CRUD ROUTES """

@app.route('/excel_db/requisite', methods=['GET', 'POST'])
def handle_requisites():
    handler = RequisiteModel()
    if request.method == 'GET':
        return handler.get_all_requisites()
    elif request.method == 'POST':
        return handler.post_requisite(request.json)
    else:
        return jsonify(f"Error: {request.method} Method Not Allowed"), 405

@app.route('/excel_db/requisite/<int:classid>/<int:reqid>', methods=['GET', 'PUT', 'DELETE'])
def handle_requisites_by_id(classid, reqid):
    handler = RequisiteModel()
    if request.method == 'GET':
        return handler.get_requisite_by_id(classid, reqid)
    elif request.method == 'PUT':
        return handler.put_requisite_by_classid_reqid(classid, reqid, request.json)
    elif request.method == 'DELETE':
        return handler.delete_requisite(classid, reqid)
    else:
        return jsonify(f"Error: {request.method} Method Not Allowed"), 405

""" SECTION CRUD ROUTES """

@app.route('/excel_db/section', methods=['GET', 'POST'])
def handle_sections():
    handler = SectionModel()
    if request.method == 'GET':
        return handler.get_all_sections()
    elif request.method == 'POST':
        return handler.post_section(request.json)
    else:
        return jsonify(f"Error: {request.method} Method Not Allowed"), 405

@app.route('/excel_db/section/<int:sid>', methods=['GET', 'PUT', 'DELETE'])
def handle_sections_by_id(sid):
    handler = SectionModel()
    if request.method == 'GET':
        return handler.get_section_by_id(sid)
    elif request.method == 'PUT':
        return handler.put_section_by_id(sid, request.json)
    elif request.method == 'DELETE':
        return handler.delete_section(sid)
    else:
        return jsonify(f"Error: {request.method} Method Not Allowed"), 405

""" MEETINGS CRUD ROUTES """

@app.route('/excel_db/meeting', methods=['GET', 'POST'])
def handle_meetings():
    handler = MeetingModel()
    if request.method == 'GET':
        return handler.get_all_meetings()
    elif request.method == 'POST':
        return handler.post_meeting(request.json)
    else:
        return jsonify(f"Error: {request.method} Method Not Allowed"), 405

@app.route('/excel_db/meeting/<int:mid>', methods=['GET', 'PUT', 'DELETE'])
def handle_meetings_by_id(mid):
    handler = MeetingModel()
    if request.method == 'GET':
        return handler.get_meeting_by_id(mid)
    elif request.method == 'PUT':
        return handler.put_meeting_by_id(mid, request.json)
    elif request.method == 'DELETE':
        return handler.delete_meeting(mid)
    else:
        return jsonify(f"Error: {request.method} Method Not Allowed"), 405

""" ROOM CRUD ROUTES """

@app.route('/excel_db/room', methods=['GET', 'POST'])
def handle_rooms():
    handler = RoomModel()
    if request.method == 'GET':
        return handler.get_all_rooms()
    elif request.method == 'POST':
        return handler.post_rooms(request.json)
    else:
        return jsonify(f"Error: {request.method} Method Not Allowed"), 405

@app.route('/excel_db/room/<int:rid>', methods=['GET', 'PUT', 'DELETE'])
def handle_rooms_by_id(rid):
    handler = RoomModel()
    if request.method == 'GET':
        return handler.get_room_by_id(rid)
    elif request.method == 'PUT':
        return handler.put_room_by_id(rid, request.json)
    elif request.method == 'DELETE':
        return handler.delete_room_by_id(rid)
    else:
        return jsonify(f"Error: {request.method} Method Not Allowed"), 405

""" SYLLABUSES CRUD ROUTES """
@app.route('/excel_db/syllable', methods=['GET', 'POST'])
def handle_syllables():
    handler = SyllabusModel()
    if request.method == 'GET':
        return handler.get_all_syllabus()
    elif request.method == 'POST':
        return handler.post_syllabus(request.json)
    else:
        return jsonify(f"Error: {request.method} Method Not Allowed"), 405

@app.route('/excel_db/syllable/<int:chunk_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_syllables_by_id(chunk_id):
    handler = SyllabusModel()
    if request.method == 'GET':
        return handler.get_syllabus_by_id(chunk_id)
    elif request.method == 'PUT':
        return handler.put_syllabus_by_id(chunk_id, request.json)
    elif request.method == 'DELETE':
        return handler.delete_syllabus(chunk_id)
    else:
        return jsonify(f"Error: {request.method} Method Not Allowed"), 405

@app.route('/excel_db/syllable/embedding', methods=['POST'])
def handle_syllables_by_embedding():
    handler = SyllabusModel()
    if request.method == 'POST':
        return handler.get_syllabus_by_embedding(request.json)
    else:
        return jsonify(f"Error: {request.method} Method Not Allowed"), 405

""" LOCAL STATISTICS ROUTES """

@app.route('/excel_db/room/<string:building>/<string:statistic>', methods=['POST'])
def handle_room_statistics(building, statistic):
    handler = StatisticsModel()
    if statistic == 'capacity':
        return handler.top_room_capacity_by_building(building)
    elif statistic == 'ratio':
        return handler.top_ratio_rooms(building)
    else:
        return jsonify(f"Local statistic '{statistic}' not found for building '{building}'"), 404

@app.route('/excel_db/room/<int:rid>/classes', methods=['POST'])
def local_statistics_by_id(rid):
    handler = StatisticsModel()

    try:
        return handler.top_classes_per_room(rid)
    except Exception as e:
        return jsonify(f"An error occurred while fetching local statistics for room ID '{rid}': {str(e)}"), 500

@app.route('/excel_db/classes/<string:year>/<string:semester>', methods=['POST'])
def top_classes_per_semester_year(year, semester):
    handler = StatisticsModel()
    try:
        return handler.top_classes_per_semester(year, semester)
    except Exception as e:
        return jsonify(f"An error occurred while fetching local statistics for year '{year}' and semester '{semester}': {str(e)}"), 500

""" GLOBAL STATISTICS ROUTES """

@app.route('/excel_db/most/<string:statistic>', methods=['POST'])
def handle_global_statistics(statistic):
    handler = StatisticsModel()
    if statistic == 'meeting':
        return handler.top_meeting()
    elif statistic == 'prerequisite':
        return handler.top_pre_requisite()
    else:
        return jsonify(f"Most '{statistic}' global statistic not found"), 404

@app.route('/excel_db/least/classes', methods=['POST'])
def least_global_statistics():
    handler = StatisticsModel()
    try:
        return handler.top_least_classes()
    except Exception as e:
        return jsonify(f"Global Statistics: An error occurred while fetching the least classes, {str(e)}"), 500

@app.route('/excel_db/section/year', methods=['POST'])
def total_sections_per_year():
    handler = StatisticsModel()
    return handler.total_sections()

if __name__ == "__main__":
    app.run(debug=True)
