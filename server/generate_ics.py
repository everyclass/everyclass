import pytz
from icalendar import Calendar, Event
from datetime import datetime
from ec_server import get_classes_for_student


def generate_ics(student_id):
    classes = get_classes_for_student(student_id)
    if not classes:
        return 'Student not exists or have no classes.'
    else:
        student_id, student_name, student_classes = classes
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
                for every_class in student_classes[(day, time)]:
                    # todo 写函数判断当前周是否在上课范围内
                    cal.add_component(__add_event(every_class['name'], every_class['location'], every_class['teacher']))
        # Write file and return
        with open('example.ics', 'wb') as f:
            f.write(cal.to_ical())
        return cal.to_ical()


def __add_event(name, location, teacher):
    event = Event()
    event.add('transp', 'opaque')
    event.add('summary', name)
    event.add('location', location)
    event.add('description', teacher + '，XXXXXXXX\n由 EveryClass (http://every.admirable.one) 导入')
    event.add('dtstart', datetime(2016, 3, 14, 8, 0, 0, tzinfo=pytz.timezone("Asia/Shanghai")))
    event.add('dtend', datetime(2016, 3, 14, 8, 0, 0, tzinfo=pytz.timezone("Asia/Shanghai")))
    event.add('dtstamp', datetime(2016, 3, 14, 8, 0, 0, tzinfo=pytz.timezone("Asia/Shanghai")))
    event['uid'] = 'ec-3901160407CSU@admirable.one'
    event.add('rrule', {'freq': 'weekly', 'interval': '2',
                        'until': datetime(2016, 3, 14, 8, 0, 0, tzinfo=pytz.timezone("Asia/Shanghai")), 'byday': 'MO',
                        'wkst': 'SU'})
    return event
