from dao.dao import DAO
from flask import jsonify


class Handler:
    # Local Statistics ----------------------------------------------+
    def TopRoomCapacity(self):
        # TODO Top 3 rooms with the most capacity.
        # @Glorian
        result = []
        dao = DAO()
        temp = dao.TopRoomCapacity()
        if temp:
            for tuple in temp:
            
        return jsonify(result)

    def TopSectionStudent(self):
        # TODO Top 3 sections with the most student-to-capacity ratio.
        # @Glorian
        result = []
        dao = DAO()
        temp = dao.TopSectionStudent()
        if temp:
            for tuple in temp:
                temp_dict = {}
                temp_dict['rid'] = tuple[0]
                temp_dict['building'] = tuple [1]
                temp_dict['room_number'] = tuple[2]
                temp_dict['capacity'] = tuple [3]
                result.append(temp_dict)
        else:
            return "Error not executed", 404
        return jsonify(result)

    def TopClassesSemester(self):
        # TODO Top 3 most taught classes per semester.
        # @Alanis
        return

    def TopClassesRoom(self):
        # TODO Top 3 classes that were taught the most per room.
        # @Alanis
        return

    # Global Statistics ---------------------------------------------+
    def TopMeetingsSemester(self):
        # TODO Top 5 meetings with the most sections.
        # @Alanis
        return

    def TopPreRequisite(self):
        # TODO Top 3 classes that appears the most as prerequisite to other classes.
        # @Anthony
        return

    def TopLeastClasses(self):
        # TODO Top 3 classes that were offered the least.
        # @Anthony
        return

    def TotalSections(self):
        # TODO Total number of sections per year.
        # @Anthony
        return
