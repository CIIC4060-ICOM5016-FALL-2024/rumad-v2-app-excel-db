from dao.dao import DAO

class Handler:
    def __init__(self):
        self.dao = DAO()

    # Local Statistics ----------------------------------------------+
    def TopRoomCapacity(self):
        # TODO Top 3 rooms with the most capacity.
        # @Glorian
        return

    def TopSectionStudent(self):
        # TODO Top 3 sections with the most student-to-capacity ratio.
        # @Glorian
        return

    def topClassesSemester(self):
        # Top 3 most taught classes per semester
        # @Alanis
        return self.dao.topClassesSemester()

    def topClassesRoom(self):
        # Top 3 classes that were taught the most per room.
        # @Alanis
        return self.dao.topClassesRoom()

    # Global Statistics ---------------------------------------------+
    def topMeetingsSemester(self):
        # Top 5 meetings with the most sections.
        # @Alanis
        return self.dao.topMeetingsSemester()

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