from codecs import open
import json

with open("win_by_team.json", "r", encoding="utf8") as f:
    data = json.load(f)

cards = [c for c in data["components"] if "glued" in c]
for card in cards:
    glued = card["glued"]
    texts = [card["name"]] + [g["text"] for g in glued]

    s = ""
    for t in texts:
        if s:
            s += ","
        s += f'"{t}"'
    print(s)

