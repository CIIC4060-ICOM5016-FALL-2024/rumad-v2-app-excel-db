from section_dao import SectionDAO
from meeting_dao import MeetingDAO

sDAO = SectionDAO()
mDAO = MeetingDAO()

sections = sDAO.get_all_sections()
section10 = sDAO.get_section_by_sid(100)

meetings = mDAO.get_all_meetings()
meeting11 = mDAO.get_meeting_by_mid(11)

print(section10)
print(sections)
print(meetings)
print(meeting11)