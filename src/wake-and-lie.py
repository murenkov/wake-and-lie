import sys
import re, datetime
from bs4 import BeautifulSoup as BSoup
from pprint import pprint


def get_bodies(messages: list) -> list:
    bodies = []
    for message in messages:
        body = message.find(attrs={"class": "body"})
        if body:
            bodies.append(body)
    return bodies


def convert_timestamp(timestamp: list) -> str:
    return "{}-{}-{}T{}".format(timestamp[2], timestamp[1], timestamp[0], timestamp[3])


if __name__ == "__main__":
    MESSAGE_TIMESTAMP = re.compile("(\d\d)\.(\d\d)\.(\d{4}) ((\d\d:\d\d):\d\d)")
    TIMESTAMP = re.compile(
        "((\d{4})-(\d\d)-(\d\d))T((\d\d):(\d\d))([+|-](\d\d):(\d\d))"
    )
    WAKING_UP_TIME = re.compile("(Встал) (\d?\d:\d\d)", re.M)
    LYING_DOWN_TIME = re.compile("(Л[ё|е]г) (\d?\d:\d\d)", re.M)
    PARSER = "html5lib"

    input_file_name = sys.argv[1]
    table = set([])
    with open(input_file_name, "r") as doc:
        messages = BSoup(doc.read(), PARSER).find_all(
            name="div", attrs={"class": "default"}
        )

        for body in get_bodies(messages):
            timestamp = body.find(attrs={"class": "date"})
            if not timestamp:
                continue
            timestamp = convert_timestamp(
                MESSAGE_TIMESTAMP.match(timestamp.get("title")).groups()
            )

            text = body.find(attrs={"class": "text"})
            if not text:
                continue
            text = text.text.strip()

            ivent = [WAKING_UP_TIME.search(text), LYING_DOWN_TIME.search(text)]
            if ivent[0]:
                ivent.append(timestamp)
            if ivent[1]:
                ivent.append(timestamp)
            for iv in ivent[:]:
                if not iv:
                    ivent.remove(iv)

            if len(ivent) == 2:
                table.add(tuple([ivent[1], ivent[0].string]))
            if len(ivent) == 4:
                table.add((ivent[2], ivent[0].string))
                table.add((ivent[3], ivent[1].string))
    for stamp, ivent in sorted(table, key=(lambda item: item[0])):
        print(f"('{stamp}', '{ivent}')")
