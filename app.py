from flask import Flask, jsonify, request, redirect
from flask_cors import CORS

from controller.class_controller        import Class_Controller
from controller.meeting_controller      import Meeting_Controller
from controller.requisite_controller    import Requisite_Controller
from controller.room_controller         import Room_Controller
from controller.section_controller      import Section_Controller
from controller.statistics_controller   import Statistics_Controller

app = Flask(__name__)
CORS(app)

@app.route('/excel_db')
def excel_db():
    return jsonify(f"Welcome")

@app.route("/")
def home():
    return redirect('/excel_db', code=302)

""" CLASS CRUD ROUTES """

@app.route('/excel_db/class', methods=['GET', 'POST'])
def handle_classes():
    handler = Class_Controller()
    if request.method == 'GET':
        return handler.get_classes()
    elif request.method == 'POST':
        return handler.post_class(request.json)
    else:
        return jsonify(f"Error: {request.method} Method Not Allowed"), 405

@app.route('/excel_db/class/<int:cid>', methods=['GET', 'PUT', 'DELETE'])
def handle_classes_by_id(cid):
    handler = Class_Controller()
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
    handler = Requisite_Controller()
    if request.method == 'GET':
        return handler.get_requisites()
    elif request.method == 'POST':
        return handler.post_requisite(request.json)
    else:
        return jsonify(f"Error: {request.method} Method Not Allowed"), 405

@app.route('/excel_db/requisite/<int:classid>/<int:reqid>', methods=['GET', 'PUT', 'DELETE'])
def handle_requisites_by_id(classid, reqid):
    handler = Requisite_Controller()
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
    handler = Section_Controller()
    if request.method == 'GET':
        return handler.get_sections()
    elif request.method == 'POST':
        return handler.post_section(request.json)
    else:
        return jsonify(f"Error: {request.method} Method Not Allowed"), 405

@app.route('/excel_db/section/<int:sid>', methods=['GET', 'PUT', 'DELETE'])
def handle_sections_by_id(sid):
    handler = Section_Controller()
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
    handler = Meeting_Controller()
    if request.method == 'GET':
        return handler.get_meetings()
    elif request.method == 'POST':
        return handler.post_meeting(request.json)
    else:
        return jsonify(f"Error: {request.method} Method Not Allowed"), 405

@app.route('/excel_db/meeting/<int:mid>', methods=['GET', 'PUT', 'DELETE'])
def handle_meetings_by_id(mid):
    handler = Meeting_Controller()
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
    handler = Room_Controller()
    if request.method == 'GET':
        return handler.get_rooms()
    elif request.method == 'POST':
        return handler.post_rooms(request.json)
    else:
        return jsonify(f"Error: {request.method} Method Not Allowed"), 405

@app.route('/excel_db/room/<int:rid>', methods=['GET', 'PUT', 'DELETE'])
def handle_rooms_by_id(rid):
    handler = Room_Controller()
    if request.method == 'GET':
        return handler.get_room_by_id(rid)
    elif request.method == 'PUT':
        return handler.put_room_by_id(rid, request.json)
    elif request.method == 'DELETE':
        return handler.delete_room_by_id(rid)
    else:
        return jsonify(f"Error: {request.method} Method Not Allowed"), 405

""" LOCAL STATISTICS ROUTES """

@app.route('/excel_db/room/<string:building>/<string:statistic>', methods=['POST'])
def handle_room_statistics(building, statistic):
    handler = Statistics_Controller()
    if not request.is_json:
        return jsonify("The request does not contain JSON data"), 400
    
    if statistic == 'capacity':
        return handler.top_room_capacity_by_building(building)
    elif statistic == 'ratio':
        return handler.top_ratio_rooms(building)
    else:
        return jsonify(f"Statistic '{statistic}' not found for building '{building}'"), 404

@app.route('/excel_db/room/<int:rid>/classes', methods=['POST'])
def local_statistics_by_id(rid):
    handler = Statistics_Controller()
    if not request.is_json:
        return jsonify("The request does not contain JSON data"), 400

    try:
        return handler.top_classes_per_room(rid)
    except Exception as e:
        return jsonify(f"An error occurred while fetching statistics for room ID '{rid}': {str(e)}"), 500

@app.route('/excel_db/classes/<string:year>/<string:semester>', methods=['POST'])
def top_classes_per_semester_year(year, semester):
    handler = Statistics_Controller()
    if not request.is_json:
        return jsonify("The request does not contain JSON data"), 400

    try:
        return handler.top_classes_per_semester(year, semester)
    except Exception as e:
        return jsonify(f"An error occurred while fetching statistics for year '{year}' and semester '{semester}': {str(e)}"), 500

""" GLOBAL STATISTICS ROUTES """

@app.route('/excel_db/most/<string:statistic>', methods=['POST'])
def handle_global_statistics(statistic):
    handler = Statistics_Controller()
    if not request.is_json:
        return jsonify("The request does not contain JSON data"), 400

    if statistic == 'meeting':
        return handler.top_meeting()
    elif statistic == 'prerequisite':
        return handler.top_pre_requisite()
    else:
        return jsonify(f"Most '{statistic}' global statistic not found"), 404

@app.route('/excel_db/least/classes', methods=['POST'])
def least_global_statistics():
    handler = Statistics_Controller()
    if not request.is_json:
        return jsonify("The request does not contain JSON data"), 400

    try:
        return handler.top_least_classes()
    except Exception as e:
        return jsonify(f"An error occurred while fetching the least classes statistics: {str(e)}"), 500

@app.route('/excel_db/section/year', methods=['POST'])
def total_sections_per_year():
    handler = Statistics_Controller()
    if not request.is_json:
        return jsonify("The request does not contain JSON data"), 400

    try:
        return handler.total_sections()
    except Exception as e:
        return jsonify(f"An error occurred while fetching the total sections per year: {str(e)}"), 500

if __name__ == "__main__":
    app.run(debug=True)
