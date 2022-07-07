import sys
from codecs import open
import json
import re
from datetime import datetime


JSON_FILENAME = "win_by_team.json"


def ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def to_csv():
    with open(JSON_FILENAME, "r", encoding="utf8") as f:
        data = json.load(f)

    cards = [c for c in data["components"] if re.match(r"^Card \d\d", c["name"])]
    with open(ts() + ".csv", "w", encoding="utf-8") as f:
        for card in cards:
            glued = card["glued"]
            texts = [card["name"]] + [g["text"] for g in glued]

            s = ""
            for t in texts:
                if s:
                    s += ","
                s += f'"{t}"'
            f.writelines([s + "\n"])


def from_csv(csv_filename):
    with open(JSON_FILENAME, "r", encoding="utf8") as f:
        data = json.load(f)

    with open(csv_filename, "r", encoding="utf-8") as f:
        for line in f.readlines():
            values = line.rstrip().replace('"', '').split(",")
            card_name, texts = values[0], values[1:]
            card = [c for c in data["components"] if c["name"] == card_name][0]
            glued = card["glued"]
            for i, g in enumerate(glued):
                g["text"] = texts[i]

    with open(ts() + ".json", "w", encoding="utf-8") as f:
        json.dump(data, f,
                ensure_ascii=False,
                indent=2)


def main():
    if len(sys.argv) <= 1:
        cmd = 'to_csv'
    else:
        cmd = sys.argv[1]

    match cmd:
        case 'to_csv':
            to_csv()
        case 'from_csv':
            from_csv(sys.argv[2])


if __name__=='__main__':
    main()
