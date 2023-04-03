from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple

from epfl_moodle_parser import MoodleCourseParser

DEFAULT_APPS = [
    {
        "name": "VS Code",
        "cmd": "code",
        "args": [
            "$b/$c/"
        ],
        "quick": True 
    }
]

DEFAULT_STRUCTURE = [
    {
        "name": "Books",
        "path": "$b/$c/Books/",
        "quick": True,
    },
    {
        "name": "Labs",
        "path": "$b/$c/Labs/",
        "quick": True
    },
    {
        "name": "Notes",
        "path": "$b/$c/Notes/main.tex",
        "template": "empty.tex",
        "quick": True
    },
    {
        "name": "Serie",
        "path": "$b/$c/Serie/Week$W/",
        "quick": True
    },
    {
        "name": "Cours",
        "path": "$b/$c/Cours/Week$W/lecture_$W.md",
        "template": "empty.md",
        "quick": True
    }
]


Event = Tuple[str, str, datetime, datetime, str]
"""Tuple containing the name, location, start, end and category of an event."""

def extract_events(lines: List[str]) -> List[Event]:
    """Extracts the events from the ics file represented as a list of lines.

    Args:
        lines (List[str]): Lines of an ics file.

    Returns:
        List[Event]: The extracted events.
    """    
    
    events = []

    reading = False
    for line in lines:
        line = line.strip()

        if reading:
            if line.startswith("SUMMARY:"):
                name = line[8:]
            elif line.startswith("LOCATION:"):
                location = line[9:]
            elif line.startswith("DTSTART;TZID=Europe/Berlin:"):
                start = datetime.strptime(line[27:], "%Y%m%dT%H%M%S")
            elif line.startswith("DURATION:PT"):
                duration = timedelta(minutes=int(line[11:-1]))
            elif line == "CATEGORIES:Horaires enseignés FBM":
                pass
            elif line == "CATEGORIES:":
                pass
            elif line.startswith("CATEGORIES:"):
                category = line[11:]

        if line == "BEGIN:VEVENT":
            reading = True
            name = "Unknown"
            location = "Unknown"
            start = datetime(1900, 1, 1)
            duration = timedelta()
            category = "Unknown"

        elif line == "END:VEVENT":
            reading = False
            events.append((name, location, start, start+duration, category))

    return events

def events_to_config(events: List[Event]) -> Dict:
    """Converts the events to a config file.

    Args:
        events (List[Event]): The events to convert.

    Returns:
        Dict: The config file.
    """    

    course_names = set(map(lambda event: event[0], events))

    to_weekly_event = lambda event: (
        format(event[2], "%a"), 
        format(event[2], "%H:%M"), 
        format(event[3], "%H:%M"),
        event[4],
        event[1]
    )
    
    courses = []
    for course_name in course_names:
        course_events = list(filter(lambda event: event[0] == course_name, events))
        weekly_events = set(map(to_weekly_event, course_events))

        course = {
            "fullName": course_name,
            "shortName": "",
            "urls": [],
            "apps": DEFAULT_APPS,
            "structure": DEFAULT_STRUCTURE,
            "events": [],
        }

        for weekly_event in weekly_events:
            course["events"].append({
                "day": weekly_event[0],
                "start": weekly_event[1],
                "end": weekly_event[2],
                "type": weekly_event[3],
                "location": weekly_event[4],
                "autoOpen": []
            })

        courses.append(course)

    courses = sorted(courses, key=lambda course: course["fullName"])

    dates = set(map(lambda event: event[2].date(), events))
    weeks = sorted(set(map(lambda date: date.isocalendar()[0:2], dates)))
    week_to_num = {f"{week[0]}-{week[1]:02}": i+1 for i, week in enumerate(weeks)}

    return {
        "name": "",
        "basePath": "",
        "weekToNum": week_to_num,
        "courses": courses,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Converts an ics file to a config file."
    )

    parser.add_argument(
        "calendar", 
        default="horaire.ics",
        help="Path to the ics file.", 
        type=str,
    )

    parser.add_argument(
        "moodle",
        default="Dashboard.html",
        help="Path to the moodle dashboard html website.",
        type=str
    )

    parser.add_argument(
        "output", 
        default="config.json", 
        help="Location to save the config file.",
        type=str
    )

    args = parser.parse_args()

    lines = []
    with open(args.calendar) as file:
        lines = file.readlines()

    events = extract_events(lines)
    config = events_to_config(events)

    page = ""
    with open(args.moodle) as file:
        page = file.read()
    
    parser = MoodleCourseParser()
    parser.feed(page)

    for course in config["courses"]:
        if course["fullName"] in parser.courses:
            short, url = parser.courses[course["fullName"]]
            course["shortName"] = short
            course["urls"].append({
                "name": "Moodle",
                "url": url,
                "quick": True
            })

    with open(args.output, "w") as outfile:
        json.dump(config, outfile, indent=4, ensure_ascii=False)
