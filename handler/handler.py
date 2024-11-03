from sqlalchemy import result_tuple

from dao.dao import DAO
from flask import jsonify

class Handler:
    # Local Statistics ----------------------------------------------+
    def TopRoomCapacity(self):
        # TODO Top 3 rooms with the most capacity.
        # @Glorian
        return

    def TopSectionStudent(self):
        # TODO Top 3 sections with the most student-to-capacity ratio.
        # @Glorian
        return

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

    def topPreRequisite(self):
        # TODO Top 3 classes that appears the most as prerequisite to other classes.
        # @Anthony
        dao = DAO()
        result = []
        temp = dao.topPreRequisite()
        if temp:
            for tuple in temp:
                tempdict = {}
                tempdict['count'] = tuple[0]
                tempdict['requid'] = tuple[1]
                tempdict['cdesc'] = tuple[2]
                result.append(tempdict)
        else:
            return "Error not executed",404

        return jsonify(result)

    def topLeastClasses(self):
        # TODO Top 3 classes that were offered the least.
        # @Anthony
        dao = DAO()
        result = []
        temp = dao.topLeastClasses()
        if temp:
            for tuple in temp:
                tempdict = {}
                tempdict['cid'] = tuple[0]
                tempdict['count'] = tuple[1]
                tempdict['cdesc'] = tuple[2]
                result.append(tempdict)
        else:
            return "Error not executed",404

        return jsonify(result)

    def totalSections(self):
        # TODO Total number of sections per year.
        # @Anthony
        dao = DAO()
        result = []
        temp = dao.totalSections()
        if temp:
            for tuple in temp:
                tempdict = {}
                tempdict['year'] = tuple[0]
                tempdict['total_sections'] = tuple[1]
                result.append(tempdict)

        else:
            return "Error not executed",404

        return jsonify(result)