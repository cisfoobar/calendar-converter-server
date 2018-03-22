from bs4 import BeautifulSoup as soup
from dateutil.parser import parse
import re
raw_dates = """<table cellpadding="0" cellspacing="0" class="timetable screen"><tbody><tr class="heading"><td class="label" colspan="7"><h2>Semester 2 - 2017/2018</h2></td></tr><tr class="heading"><td class="label"><br></td><td><strong>Period 1</strong><br>07:55-09:15<br></td><td><strong>Period 2</strong><br>09:20-10:35<br></td><td><strong>Period 3</strong><br>10:40-11:05<br></td><td><strong>Period 4</strong><br>11:05-11:30<br></td><td><strong>Period 5</strong><br>11:35-12:50<br></td><td><strong>Period 6</strong><br>13:45-15:00<br></td></tr><tr><td class="label">Day A1</td><td class="slot lesson left"><p>08 dDes 21 1718<br>Sanaz Momeni<br>513</p></td><td class="slot lesson "><p>08 Math 7 1718<br>Francis Murphy<br>524</p></td><td class="slot lesson "><p><br><br></p></td><td class="slot lesson "><p>08Y1<br>Greg Silver<br>512</p></td><td class="slot lesson "><p>08 PE 1 1718<br>Jamie Hooper<br>001</p></td><td class="slot lesson "><p>08 Sci 7 1718<br>Deborah Smith<br>505</p></td></tr><tr><td class="label">Day B1</td><td class="slot lesson left"><p>08 InSo 7 1718<br>Adam Cruickshank et al<br>524</p></td><td class="slot lesson "><p>08 Music 23 1718<br>Sam Lau<br>411</p></td><td class="slot lesson "><p><br><br></p></td><td class="slot lesson "><p>08 Com Time 9 1718<br><br>TBC</p></td><td class="slot lesson "><p>08 Eng 7 1718<br>Nuala O'Connell et al<br>524</p></td><td class="slot lesson "><p>08 Chin 1 1 1718<br>Debbie Chan<br>422</p></td></tr><tr><td class="label">Day A2</td><td class="slot lesson left"><p>08 Sci 7 1718<br>Deborah Smith<br>505</p></td><td class="slot lesson "><p>08 dDes 21 1718<br>Sanaz Momeni<br>513</p></td><td class="slot lesson "><p><br><br></p></td><td class="slot lesson "><p>08Y1<br>Greg Silver<br>512</p></td><td class="slot lesson "><p>08 Math 7 1718<br>Francis Murphy<br>524</p></td><td class="slot lesson "><p>08 PE 1 1718<br>Jamie Hooper<br>001</p></td></tr><tr><td class="label">Day B2</td><td class="slot lesson left"><p>08 Chin 1 1 1718<br>Debbie Chan<br>422</p></td><td class="slot lesson "><p>08 InSo 7 1718<br>Adam Cruickshank et al<br>524</p></td><td class="slot lesson "><p><br><br></p></td><td class="slot lesson "><p>08Y1<br>Greg Silver<br>512</p></td><td class="slot lesson "><p>08 Music 23 1718<br>Sam Lau<br>411</p></td><td class="slot lesson "><p>08 Eng 7 1718<br>Nuala O'Connell et al<br>524</p></td></tr><tr><td class="label">Day A3</td><td class="slot lesson left"><p>08 Eng X 1 1718<br>Bradford Masoni<br>226</p></td><td class="slot lesson "><p>08 Sci 7 1718<br>Deborah Smith<br>505</p></td><td class="slot lesson "><p><br><br></p></td><td class="slot lesson "><p>08 Com Time 9 1718<br><br>TBC</p></td><td class="slot lesson "><p>08 dDes 21 1718<br>Sanaz Momeni<br>513</p></td><td class="slot lesson "><p>08 Math 7 1718<br>Francis Murphy<br>524</p></td></tr><tr><td class="cycle label">Day B3</td><td class="slot today cycle lesson left"><p>08 Eng 7 1718<br>Nuala O'Connell et al<br>524</p></td><td class="slot today cycle lesson "><p>08 Chin 1 1 1718<br>Debbie Chan<br>422</p></td><td class="slot today cycle lesson "><p><br><br></p></td><td class="slot today cycle lesson "><p>08Y1<br>Greg Silver<br>512</p></td><td class="slot today cycle lesson "><p>08 InSo 7 1718<br>Adam Cruickshank et al<br>524</p></td><td class="slot today cycle lesson "><p>08 Music 23 1718<br>Sam Lau<br>411</p></td></tr><tr><td class="label">Day A4</td><td class="slot lesson left"><p>08 Math 7 1718<br>Francis Murphy<br>524</p></td><td class="slot lesson "><p>08 PE 1 1718<br>Jamie Hooper<br>001</p></td><td class="slot lesson "><p><br><br></p></td><td class="slot lesson "><p>08Y1<br>Greg Silver<br>512</p></td><td class="slot lesson "><p>08 Sci 7 1718<br>Deborah Smith<br>505</p></td><td class="slot lesson "><p>08 dDes 21 1718<br>Sanaz Momeni<br>513</p></td></tr><tr><td class="label">Day B4</td><td class="slot lesson left"><p>08 Music 23 1718<br>Sam Lau<br>411</p></td><td class="slot lesson "><p>08 Eng 7 1718<br>Nuala O'Connell et al<br>524</p></td><td class="slot lesson "><p><br><br></p></td><td class="slot lesson "><p>08 Com Time 9 1718<br><br>TBC</p></td><td class="slot lesson "><p>08 Chin 1 1 1718<br>Debbie Chan<br>422</p></td><td class="slot lesson "><p>08 InSo 7 1718<br>Adam Cruickshank et al<br>524</p></td></tr><tr><td class="label">Day A5</td><td class="slot lesson left"><p>08 dDes 21 1718<br>Sanaz Momeni<br>513</p></td><td class="slot lesson "><p>08 Math 7 1718<br>Francis Murphy<br>524</p></td><td class="slot lesson "><p><br><br></p></td><td class="slot lesson "><p>08Y1<br>Greg Silver<br>512</p></td><td class="slot lesson "><p>08 PE 1 1718<br>Jamie Hooper<br>001</p></td><td class="slot lesson "><p>08 Sci 7 1718<br>Deborah Smith<br>505</p></td></tr><tr><td class="label">Day B5</td><td class="slot lesson left"><p>08 InSo 7 1718<br>Adam Cruickshank et al<br>524</p></td><td class="slot lesson "><p>08 Music 23 1718<br>Sam Lau<br>411</p></td><td class="slot lesson "><p><br><br></p></td><td class="slot lesson "><p>08Y1<br>Greg Silver<br>512</p></td><td class="slot lesson "><p>08 Eng 7 1718<br>Nuala O'Connell et al<br>524</p></td><td class="slot lesson "><p>08 Chin 1 1 1718<br>Debbie Chan<br>422</p></td></tr><tr><td class="label">Day A6</td><td class="slot lesson left"><p>08 Chin X 31 1718<br>Debbie Chan<br>512</p></td><td class="slot lesson "><p>08 Sci 7 1718<br>Deborah Smith<br>505</p></td><td class="slot lesson "><p><br><br></p></td><td class="slot lesson "><p>08 Com Time 9 1718<br><br>TBC</p></td><td class="slot lesson "><p>08 dDes 21 1718<br>Sanaz Momeni<br>513</p></td><td class="slot lesson "><p>08 Math 7 1718<br>Francis Murphy<br>524</p></td></tr><tr><td class="cycle label">Day B6</td><td class="slot cycle lesson left"><p>08 Eng 7 1718<br>Nuala O'Connell et al<br>524</p></td><td class="slot cycle lesson "><p>08 Chin 1 1 1718<br>Debbie Chan<br>422</p></td><td class="slot cycle lesson "><p><br><br></p></td><td class="slot cycle lesson "><p>08Y1<br>Greg Silver<br>512</p></td><td class="slot cycle lesson "><p>08 InSo 7 1718<br>Adam Cruickshank et al<br>524</p></td><td class="slot cycle lesson "><p>08 Music 23 1718<br>Sam Lau<br>411</p></td></tr><tr><td colspan="10" style="height:50%;">&nbsp;</td></tr><tr><td class="label" style="padding-top:0;">Day A1</td><td colspan="9" style="text-align:left;"><span>Wed 9 Aug&nbsp;&nbsp;&nbsp;</span><span>Wed 6 Sep&nbsp;&nbsp;&nbsp;</span><span>Fri 22 Sep&nbsp;&nbsp;&nbsp;</span><span>Fri 13 Oct&nbsp;&nbsp;&nbsp;</span><span>Thu 16 Nov&nbsp;&nbsp;&nbsp;</span><span>Tue 5 Dec&nbsp;&nbsp;&nbsp;</span><span>Mon 8 Jan&nbsp;&nbsp;&nbsp;</span><span>Wed 24 Jan&nbsp;&nbsp;&nbsp;</span><span>Fri 9 Feb&nbsp;&nbsp;&nbsp;</span><span>Wed 14 Mar&nbsp;&nbsp;&nbsp;</span><span>Mon 9 Apr&nbsp;&nbsp;&nbsp;</span><span>Wed 25 Apr&nbsp;&nbsp;&nbsp;</span><span>Wed 30 May&nbsp;&nbsp;&nbsp;</span><span>Fri 15 Jun&nbsp;&nbsp;&nbsp;</span></td></tr><tr><td class="label" style="padding-top:0;">Day B1</td><td colspan="9" style="text-align:left;"><span>Tue 22 Aug&nbsp;&nbsp;&nbsp;</span><span>Thu 7 Sep&nbsp;&nbsp;&nbsp;</span><span>Mon 25 Sep&nbsp;&nbsp;&nbsp;</span><span>Mon 30 Oct&nbsp;&nbsp;&nbsp;</span><span>Fri 17 Nov&nbsp;&nbsp;&nbsp;</span><span>Wed 6 Dec&nbsp;&nbsp;&nbsp;</span><span>Tue 9 Jan&nbsp;&nbsp;&nbsp;</span><span>Thu 25 Jan&nbsp;&nbsp;&nbsp;</span><span>Mon 12 Feb&nbsp;&nbsp;&nbsp;</span><span>Thu 15 Mar&nbsp;&nbsp;&nbsp;</span><span>Tue 10 Apr&nbsp;&nbsp;&nbsp;</span><span>Thu 26 Apr&nbsp;&nbsp;&nbsp;</span><span>Thu 31 May&nbsp;&nbsp;&nbsp;</span></td></tr><tr><td class="label" style="padding-top:0;">Day A2</td><td colspan="9" style="text-align:left;"><span>Wed 23 Aug&nbsp;&nbsp;&nbsp;</span><span>Fri 8 Sep&nbsp;&nbsp;&nbsp;</span><span>Tue 31 Oct&nbsp;&nbsp;&nbsp;</span><span>Mon 20 Nov&nbsp;&nbsp;&nbsp;</span><span>Thu 7 Dec&nbsp;&nbsp;&nbsp;</span><span>Wed 10 Jan&nbsp;&nbsp;&nbsp;</span><span>Fri 26 Jan&nbsp;&nbsp;&nbsp;</span><span>Tue 13 Feb&nbsp;&nbsp;&nbsp;</span><span>Fri 16 Mar&nbsp;&nbsp;&nbsp;</span><span>Wed 11 Apr&nbsp;&nbsp;&nbsp;</span><span>Fri 27 Apr&nbsp;&nbsp;&nbsp;</span><span>Fri 1 Jun&nbsp;&nbsp;&nbsp;</span></td></tr><tr><td class="label" style="padding-top:0;">Day B2</td><td colspan="9" style="text-align:left;"><span>Thu 24 Aug&nbsp;&nbsp;&nbsp;</span><span>Mon 11 Sep&nbsp;&nbsp;&nbsp;</span><span>Wed 27 Sep&nbsp;&nbsp;&nbsp;</span><span>Wed 1 Nov&nbsp;&nbsp;&nbsp;</span><span>Fri 8 Dec&nbsp;&nbsp;&nbsp;</span><span>Thu 11 Jan&nbsp;&nbsp;&nbsp;</span><span>Mon 29 Jan&nbsp;&nbsp;&nbsp;</span><span>Mon 19 Mar&nbsp;&nbsp;&nbsp;</span><span>Thu 12 Apr&nbsp;&nbsp;&nbsp;</span><span>Mon 30 Apr&nbsp;&nbsp;&nbsp;</span><span>Mon 4 Jun&nbsp;&nbsp;&nbsp;</span></td></tr><tr><td class="label" style="padding-top:0;">Day A3</td><td colspan="9" style="text-align:left;"><span>Fri 25 Aug&nbsp;&nbsp;&nbsp;</span><span>Thu 28 Sep&nbsp;&nbsp;&nbsp;</span><span>Fri 29 Sep&nbsp;&nbsp;&nbsp;</span><span>Thu 2 Nov&nbsp;&nbsp;&nbsp;</span><span>Wed 22 Nov&nbsp;&nbsp;&nbsp;</span><span>Mon 11 Dec&nbsp;&nbsp;&nbsp;</span><span>Fri 12 Jan&nbsp;&nbsp;&nbsp;</span><span>Wed 28 Feb&nbsp;&nbsp;&nbsp;</span><span>Wed 2 May&nbsp;&nbsp;&nbsp;</span><span>Tue 5 Jun&nbsp;&nbsp;&nbsp;</span></td></tr><tr><td class="label" style="padding-top:0;">Day B3</td><td colspan="9" style="text-align:left;"><span>Mon 28 Aug&nbsp;&nbsp;&nbsp;</span><span>Wed 13 Sep&nbsp;&nbsp;&nbsp;</span><span>Fri 3 Nov&nbsp;&nbsp;&nbsp;</span><span>Thu 23 Nov&nbsp;&nbsp;&nbsp;</span><span>Mon 15 Jan&nbsp;&nbsp;&nbsp;</span><span>Wed 31 Jan&nbsp;&nbsp;&nbsp;</span><span>Thu 1 Mar&nbsp;&nbsp;&nbsp;</span><span>Wed 21 Mar&nbsp;&nbsp;&nbsp;</span><span>Mon 16 Apr&nbsp;&nbsp;&nbsp;</span><span>Thu 3 May&nbsp;&nbsp;&nbsp;</span><span>Wed 6 Jun&nbsp;&nbsp;&nbsp;</span></td></tr><tr><td class="label" style="padding-top:0;">Day A4</td><td colspan="9" style="text-align:left;"><span>Tue 29 Aug&nbsp;&nbsp;&nbsp;</span><span>Thu 14 Sep&nbsp;&nbsp;&nbsp;</span><span>Wed 4 Oct&nbsp;&nbsp;&nbsp;</span><span>Mon 6 Nov&nbsp;&nbsp;&nbsp;</span><span>Fri 24 Nov&nbsp;&nbsp;&nbsp;</span><span>Wed 13 Dec&nbsp;&nbsp;&nbsp;</span><span>Tue 16 Jan&nbsp;&nbsp;&nbsp;</span><span>Thu 1 Feb&nbsp;&nbsp;&nbsp;</span><span>Fri 2 Mar&nbsp;&nbsp;&nbsp;</span><span>Thu 22 Mar&nbsp;&nbsp;&nbsp;</span><span>Fri 4 May&nbsp;&nbsp;&nbsp;</span><span>Thu 7 Jun&nbsp;&nbsp;&nbsp;</span></td></tr><tr><td class="label" style="padding-top:0;">Day B4</td><td colspan="9" style="text-align:left;"><span>Wed 30 Aug&nbsp;&nbsp;&nbsp;</span><span>Fri 15 Sep&nbsp;&nbsp;&nbsp;</span><span>Fri 6 Oct&nbsp;&nbsp;&nbsp;</span><span>Mon 27 Nov&nbsp;&nbsp;&nbsp;</span><span>Thu 14 Dec&nbsp;&nbsp;&nbsp;</span><span>Wed 17 Jan&nbsp;&nbsp;&nbsp;</span><span>Fri 2 Feb&nbsp;&nbsp;&nbsp;</span><span>Mon 5 Mar&nbsp;&nbsp;&nbsp;</span><span>Fri 23 Mar&nbsp;&nbsp;&nbsp;</span><span>Wed 18 Apr&nbsp;&nbsp;&nbsp;</span><span>Mon 21 May&nbsp;&nbsp;&nbsp;</span><span>Fri 8 Jun&nbsp;&nbsp;&nbsp;</span></td></tr><tr><td class="label" style="padding-top:0;">Day A5</td><td colspan="9" style="text-align:left;"><span>Thu 31 Aug&nbsp;&nbsp;&nbsp;</span><span>Mon 18 Sep&nbsp;&nbsp;&nbsp;</span><span>Mon 9 Oct&nbsp;&nbsp;&nbsp;</span><span>Wed 8 Nov&nbsp;&nbsp;&nbsp;</span><span>Tue 28 Nov&nbsp;&nbsp;&nbsp;</span><span>Fri 15 Dec&nbsp;&nbsp;&nbsp;</span><span>Thu 18 Jan&nbsp;&nbsp;&nbsp;</span><span>Mon 5 Feb&nbsp;&nbsp;&nbsp;</span><span>Tue 6 Mar&nbsp;&nbsp;&nbsp;</span><span>Mon 26 Mar&nbsp;&nbsp;&nbsp;</span><span>Thu 19 Apr&nbsp;&nbsp;&nbsp;</span><span>Wed 23 May&nbsp;&nbsp;&nbsp;</span><span>Mon 11 Jun&nbsp;&nbsp;&nbsp;</span></td></tr><tr><td class="label" style="padding-top:0;">Day B5</td><td colspan="9" style="text-align:left;"><span>Fri 1 Sep&nbsp;&nbsp;&nbsp;</span><span>Mon 13 Nov&nbsp;&nbsp;&nbsp;</span><span>Wed 29 Nov&nbsp;&nbsp;&nbsp;</span><span>Wed 3 Jan&nbsp;&nbsp;&nbsp;</span><span>Fri 19 Jan&nbsp;&nbsp;&nbsp;</span><span>Tue 6 Feb&nbsp;&nbsp;&nbsp;</span><span>Wed 7 Mar&nbsp;&nbsp;&nbsp;</span><span>Tue 27 Mar&nbsp;&nbsp;&nbsp;</span><span>Fri 20 Apr&nbsp;&nbsp;&nbsp;</span><span>Thu 24 May&nbsp;&nbsp;&nbsp;</span></td></tr><tr><td class="label" style="padding-top:0;">Day A6</td><td colspan="9" style="text-align:left;"><span>Mon 4 Sep&nbsp;&nbsp;&nbsp;</span><span>Wed 20 Sep&nbsp;&nbsp;&nbsp;</span><span>Wed 11 Oct&nbsp;&nbsp;&nbsp;</span><span>Thu 30 Nov&nbsp;&nbsp;&nbsp;</span><span>Thu 4 Jan&nbsp;&nbsp;&nbsp;</span><span>Mon 22 Jan&nbsp;&nbsp;&nbsp;</span><span>Wed 7 Feb&nbsp;&nbsp;&nbsp;</span><span>Thu 8 Mar&nbsp;&nbsp;&nbsp;</span><span>Wed 28 Mar&nbsp;&nbsp;&nbsp;</span><span>Mon 23 Apr&nbsp;&nbsp;&nbsp;</span><span>Mon 28 May&nbsp;&nbsp;&nbsp;</span><span>Wed 13 Jun&nbsp;&nbsp;&nbsp;</span></td></tr><tr><td class="label" style="padding-top:0;">Day B6</td><td colspan="9" style="text-align:left;"><span>Thu 21 Sep&nbsp;&nbsp;&nbsp;</span><span>Thu 12 Oct&nbsp;&nbsp;&nbsp;</span><span>Wed 15 Nov&nbsp;&nbsp;&nbsp;</span><span>Mon 4 Dec&nbsp;&nbsp;&nbsp;</span><span>Fri 5 Jan&nbsp;&nbsp;&nbsp;</span><span>Thu 8 Feb&nbsp;&nbsp;&nbsp;</span><span>Thu 29 Mar&nbsp;&nbsp;&nbsp;</span><span>Tue 29 May&nbsp;&nbsp;&nbsp;</span><span>Thu 14 Jun&nbsp;&nbsp;&nbsp;</span></td></tr></tbody></table>"""
parsed_contents = soup(raw_dates, "html.parser")

def parse_date(date):
    output = parse(date)
    # print (date)
    return "{0}/{1}/{2}".format(date.day(), date.month(), date.year())

# Order = A1, A2, A3, A4, A5, A6, B1, B2, B3, B4, B5, B6

def repl(sub):
    return {
        'Eng':'English',
        'Chin':'Chinese',
        'Math':'Mathematics',
        'Sci':'Science',
        'InSo':'Individual and Society',
        'Fren':'French',
        'Span':'Spanish',
        'dDes':'Digital Design',
        'pDes':'Product Design',
        'Eng X':'English X',
        'Chin X':'Chinese X',
        'VisA':'Visual Art'
    }.get(sub, sub)

def selecting_date(line):
    pattern = r'(Day [AB][123456])'
    return (re.findall(pattern, line))

def starting_time(n):
    if n == 1: return '07:55 AM'
    elif n == 2: return '09:20 AM'
    elif n == 5: return '11:35 AM'
    else: return '13:45 PM'

def ending_time(n):
    if n == 1: return '09:15 AM'
    elif n == 2: return '10:35 AM'
    elif n == 5: return '12:50 PM'
    else: return '15:00 PM'

with open('desired_output.csv', 'w') as fout:
    fout.write('Subject, Start Date, All Day Event, Start Time, End Time, Location\n')
    date_rows = parsed_contents.select("tbody tr")[14:]

    date_rows = map(lambda row: list(map(lambda x: x.string.strip(), row.select("td span"))), date_rows)
    output = {}
    for num, dates in enumerate(date_rows):
        for date in dates:
            # date = parse_date(date)
            output[date] = "{0}{1}".format("A" if num % 2 == 1 else "B", ((num - 1) // 2) + 1)

    date_slot = ["A1", "A2", "A3", "A4", "A5", "A6", "B1", "B2", "B3", "B4", "B5", "B6"]

    months = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()
    # Format: Subject, Start Date, All Day Event

    dates = [[], [], [], [], [], [], [], [], [], [], [], []]

    for t in output:
        array = t.split()
        month = months.index(array[2]) + 1
        date_string = '%s/%s/%s' % (array[1], months.index(array[2]) + 1, [2017, 2018][month <= 7])
        fout.write('%s, %s, %s,,,\n' % (output[t], date_string, True))
        dates[date_slot.index(output[t])].append(str(date_string))

    array = ["A1", "A2", "A3", "A4", "A5", "A6", "B1", "B2", "B3", "B4", "B5", "B6"]

    date_rows = parsed_contents.select("tbody tr")[2:14:]
    for t in (date_rows):
        original = t.select('td')
        del original[3]
        class_order = selecting_date(str(original[0]))[0]
        del original[0]
        for index in range(len(original)):
            u = original[index]
            classes = str(u.select('p')[0])[3:-4:].split('<br/>')
            number = array.index(class_order.split()[1])
            if len(dates) > number:
                date = dates[number]
                for u in date:
                    # Subject, Start Date, All Day Event, Start Time, End Time
                    if 'Com Time' in classes[0]:
                        fout.write('Com Time, %s, False, 11:05 AM, 11:30 AM,\n' % (u))
                    elif len(classes[0]) == 4:
                        fout.write('Advisory, %s, False, 11:05 AM, 11:30 AM,\n' % (u))
                    else:
                        current_class = classes[0].split()[1] if classes[0].split()[2] != 'X' else classes[0].split()[1] + ' ' + classes[0].split()[2]
                        current_class = repl(current_class)
                        period = index + 1
                        fout.write('%s, %s, False, %s, %s, %s\n' % (current_class, u, starting_time(period), ending_time(period), classes[2] if current_class != 'PE' else ''))
