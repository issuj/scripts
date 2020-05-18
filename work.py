#!/bin/env/python

"""
Keeping track of working hours

Sample input:

** 2019 hours=33:45 days=4.5 start=0:00

16.9. 9:00-12:00, 12:30-17:30
17.9. 9:15-12:00, 12:45-17:15
18.9. 9:15-11:30, 12:30-18:00
19.9. 9:30-11:30, 12:00-17:30
20.9. 8:45-11:45, 12:45-17:15
23.9. 11:10-11:35, 12:25-19:15
24.9. 8:30-12:10, 13:30-18:00
25.9. 8:30-11:45, 12:30-17:30
26.9. 10:15-12:00, 12:45-18:00
27.9. 9:15-12:00, 13:15-16:55
30.9. 10:15-12:35, 13:35-17:40


Output for that same sample:

16.9. 9:00-12:00, 12:30-17:30 (8:00) +1:15
17.9. 9:15-12:00, 12:45-17:15 (7:15) +1:45
18.9. 9:15-11:30, 12:30-18:00 (7:45) +2:45
19.9. 9:30-11:30, 12:00-17:30 (7:30) +3:30
20.9. 8:45-11:45, 12:45-17:15 (7:30) +4:15
Week 38/2019: 38:00 / 33:45
23.9. 11:10-11:35, 12:25-19:15 (7:15) +4:45
24.9. 8:30-12:10, 13:30-18:00 (8:10) +6:10
25.9. 8:30-11:45, 12:30-17:30 (8:15) +7:40
26.9. 10:15-12:00, 12:45-18:00 (7:00) +7:55
27.9. 9:15-12:00, 13:15-16:55 (6:25) +7:35
Week 39/2019: 37:05 / 33:45
30.9. 10:15-12:35, 13:35-17:40 (6:25) +7:15


Other stuff:
23.12. -  (dash: working day where I didn't work, comes off of my +-)
24.12. *  (star: public holiday)
"""


import sys
import re
from datetime import datetime
from datetime import timedelta

def fmtDelta(x, pref=""):
    zero = timedelta()
    if x < zero:
        return "-" + fmtDelta(-x, "")
    seconds = x.total_seconds()
    hours = seconds//3600
    minutes = (seconds//60)%60
    return pref + "{}:{:02d}".format(round(hours), round(minutes))

def weekRange(x):
    y, wd = x.year, x.weekday()
    start, end = x.date() - timedelta(days=wd), x.date() + timedelta(days=7-wd)
    yearstart = datetime(year=y, month=1, day=1).date()
    yearend = datetime(year=y+1, month=1, day=1).date()
    if start < yearstart:
        start = yearstart
    if end > yearend:
        end = yearend
    return datetime.combine(start, datetime.min.time()), datetime.combine(end, datetime.min.time())

def workWeekRatio(weekstart, weekend):
    n = 0
    day = timedelta(days=1)
    now = weekstart
    while now < weekend and n < 5:
        if now.weekday() in (0, 1, 2, 3, 4):
            n += 1
        now = now + day
    return n/5

year = datetime.now().year
week = weekRange(datetime.now())
weekTotal = timedelta()
total = timedelta()
expectWeek = timedelta(hours=37, minutes=30)
daysPerWeek = 5
daysSeen = 0
weekFactor = workWeekRatio(*week)
expectDay = expectWeek / daysPerWeek

for l in sys.stdin.readlines():
    l = l.strip()
    matchdef = re.match('\*\* (\d{4}) hours=(\d+:\d{2}) days=(\d+(.\d+)?) start=(-?\d+:\d{2})', l)
    match = re.match('(\d+\.\d+\.)\s+((\d+:\d+-\d+:\d+[\s,]*)+)', l)
    matchZero = re.match('(\d+\.\d+\.)\s+(-)', l)
    matchHoliday = re.match('(\d+\.\d+\.)\s+(\*)', l)
    if matchdef:
        year = int(matchdef.group(1))
        week = weekRange(datetime(year=year, month=1, day=1))
        weekFactor = workWeekRatio(*week)
        weekTotal = timedelta()
        total = timedelta(hours=int(matchdef.group(5).split(':')[0]), minutes=int(matchdef.group(5).split(':')[1]))
        expectWeek = timedelta(hours=int(matchdef.group(2).split(':')[0]), minutes=int(matchdef.group(2).split(':')[1]))
        daysPerWeek = float(matchdef.group(3))
        expectDay = expectWeek / daysPerWeek
        daysSeen = 0
    if not (match or matchZero or matchHoliday):
        continue

    day = (match or matchZero or matchHoliday).group(1)
    today = datetime.strptime("{}{}".format(day, year), '%d.%m.%Y')
    if not week[0] <= today < week[1]:
        if daysSeen:
            total += weekTotal - expectWeek * weekFactor
            print("Week {}/{}: {} / {}".format(*(week[0].isocalendar()[1::-1]), fmtDelta(weekTotal), fmtDelta(expectWeek*weekFactor)))
        weekTotal = timedelta()
        week = weekRange(today)
        weekFactor = workWeekRatio(*week)
        daysSeen = 0
    daysSeen += 1
    if match:
        timerangesStr = re.findall('\d+:\d+-\d+:\d+', l)
        fmt = '%H:%M'
        parse = lambda tstr: datetime.strptime(tstr, fmt)
        timeranges = [tuple(t.split("-")) for t in timerangesStr]
        timeranges = [parse(t[1]) - parse(t[0]) for t in timeranges]
        dayTotal = sum(timeranges, timedelta())
        weekTotal += dayTotal
        projection = weekTotal - min(daysSeen/(weekFactor*5), 1) * expectWeek * weekFactor
        print("{} {} ({}) {}".format(day, match.group(2).strip(), fmtDelta(dayTotal), fmtDelta(total + projection, '+')))
    elif matchZero:
        projection = weekTotal - weekFactor * expectWeek/(5/weekFactor)
        projection = weekTotal - min(daysSeen/(weekFactor*5), 1) * expectWeek * weekFactor
        print("{} {} ({}) {}".format(day, matchZero.group(2).strip(), fmtDelta(timedelta()), fmtDelta(total + projection, '+')))
    elif matchHoliday:
        weekTotal += expectWeek / 5
        projection = weekTotal - min(daysSeen/(5*weekFactor), 1) * expectWeek * weekFactor
        print("{} {} ({}) {}".format(day, matchHoliday.group(2).strip(), fmtDelta(expectWeek / 5), fmtDelta(total + projection, '+')))

