from html.parser import HTMLParser
import re

DIV = "div"
A = "a"
SPAN = "span"

def is_dashboard_card(tag, attrs):
    return (tag == DIV and
            attrs.get("class") == "card dashboard-card" and 
            attrs.get("role") == "listitem" and 
            attrs.get("data-region") == "course-content" and 
            attrs.get("data-course-id") is not None)

def is_card_body(tag, attrs):
    return (tag == DIV and 
            attrs.get("class") == "card-body pr-1 course-info-container")

def is_muted_div(tag, attrs):
    return (tag == DIV and 
            attrs.get("class") == "text-muted muted d-flex mb-1 flex-wrap")

def is_short_name(tag, attrs):
    return (tag == DIV and len(attrs) == 0)

def is_href(tag, attrs):
    moodle = re.compile(r"https://moodle.epfl.ch/course/view.php\?id=\d+")
    return (tag == A and 
            attrs.get("class") == "aalink coursename mr-2" and
            moodle.match(attrs.get("href")) is not None)

def is_full_name(tag, attrs):
    return (tag == SPAN and attrs.get("class") == "multiline")

class MoodleCourseParser(HTMLParser):
    courses = {}
    current_course = []
    divs = 0

    dashboard_card = False
    card_body = False
    muted_div = False
    short_name = False
    href = False
    full_name = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs) # Convert list of tuples to dict.

        if is_dashboard_card(tag, attrs):
            self.dashboard_card = True
        elif self.dashboard_card and is_card_body(tag, attrs):
            self.card_body = True
        elif self.card_body and is_muted_div(tag, attrs):
            self.muted_div = True 
        elif self.muted_div and is_short_name(tag, attrs):
            self.short_name = True
        elif self.card_body and is_href(tag, attrs):
            self.current_course.append(attrs.get("href").strip())
            self.href = True
        elif self.href and is_full_name(tag, attrs):
            self.full_name = True

        if tag == DIV and self.dashboard_card:
            self.divs += 1

    def handle_data(self, data):
        if self.short_name:
            short = data.strip().replace("-", "")
            short = re.sub("\(.*\)", "", short)
            self.current_course.append(short)
            self.short_name = False
            self.muted_div = False
        elif self.full_name:
            self.current_course.append(data.strip())
            self.full_name = False
            self.href = False

    def handle_endtag(self, tag):
        if tag == DIV and self.dashboard_card:
            self.divs -= 1
            if self.divs == 0:
                self.dashboard_card = False
                self.card_body = False
                if len(self.current_course) == 3:
                    short, url, full = tuple(self.current_course)
                    self.courses[full] = short, url
                self.current_course = []

if __name__ == "__main__":
    parser = MoodleCourseParser()
    file_name = "Dashboard.html"
    with open(file_name, "r") as f:
        parser.feed(f.read())

    for key, value in parser.courses.items():
        print(f"{key:<30} : {value}")
