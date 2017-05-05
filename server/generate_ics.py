import pytz
from icalendar import Calendar, Event
from datetime import datetime


# .ics files should follow
# https://tools.ietf.org/html/rfc2445?cm_mc_uid=02098050116114871518159&cm_mc_sid_50200000=1493972416
def generate_ics(student_id, student_name, student_classes):
    # Create calender object
    cal = Calendar()
    cal.add('prodid', '-//Admirable//EveryClass 1.0//EN')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('X-WR-CALNAME', student_name + '的课表')
    cal.add('X-WR-TIMEZONE', 'Asia/Shanghai')
    # Create events
    for time in range(1, 7):
        for day in range(1, 8):
            if (day, time) in student_classes:
                for every_class in student_classes[(day, time)]:
                    cal.add_component(
                        __add_event(every_class['name'], every_class['location'], every_class['teacher'], student_id))
    # Write file
    import os
    with open(os.path.dirname(__file__) + '/ics/%s.ics' % student_id, 'w') as f:
        f.write(cal.to_ical().decode(encoding='utf-8'))


def __add_event(name, location, teacher, student_id):
    event = Event()
    event.add('transp', 'opaque')
    summary = name
    if location != 'None':
        summary = name + '@' + location
    description = ''
    if teacher != 'None':
        description = '教师：' + teacher + '\n'
    description += '由 EveryClass (http://every.admirable.one) 导入'
    event.add('summary', summary)
    event.add('location', location)
    event.add('description', description)
    event.add('dtstart', datetime(2016, 3, 14, 8, 0, 0, tzinfo=pytz.timezone("Asia/Shanghai")))
    event.add('dtend', datetime(2016, 3, 14, 8, 0, 0, tzinfo=pytz.timezone("Asia/Shanghai")))
    event['uid'] = 'ec-CSU' + student_id + '@admirable.one'
    event.add('rrule', {'freq': 'weekly', 'interval': '2',
                        'until': datetime(2016, 3, 14, 8, 0, 0, tzinfo=pytz.timezone("Asia/Shanghai")), 'byday': 'MO',
                        'wkst': 'SU'})
    return event
