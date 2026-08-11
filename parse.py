# -*- coding: utf-8 -*-
import csv, json, re

rows = []
with open("sheet.csv", encoding="utf-8") as f:
    for r in csv.reader(f):
        # pad to 24 cols
        r = (r + [""]*24)[:24]
        rows.append([c.strip() for c in r])

def is_level(s):
    return bool(re.match(r"^\d+\s*렙\s*/", s))

# find character block start rows: name(col1) non-empty AND level(col2) matches
starts = []
for i, r in enumerate(rows):
    if r[1] and is_level(r[2]):
        starts.append(i)

chars = []
for idx, s in enumerate(starts):
    end = starts[idx+1] if idx+1 < len(starts) else len(rows)
    block = rows[s:end]

    name_cell = block[0][1]
    parts = [p.strip() for p in name_cell.split("\n") if p.strip()]
    name = " ".join(p for p in parts if not p.startswith("#"))
    tags = [p for p in parts if p.startswith("#")]

    def collect(col):
        seen, out = set(), []
        for r in block:
            v = r[col].strip()
            if v and v not in seen:
                seen.add(v); out.append(v)
        return out

    level = block[0][2]
    talent = block[0][3]
    roles = collect(6)
    arts = collect(7)
    sands = collect(11)
    goblet = collect(12)
    crown = collect(13)
    substat = collect(14)
    remark = collect(21)
    img = ""
    for r in block:
        if r[22].strip():
            img = r[22].strip(); break

    # weapons
    weapons = []
    cur = None
    for r in block:
        w = r[17].strip()
        crit, eff, er = r[18].strip(), r[19].strip(), r[20].strip()
        if w:
            cur = {"name": w, "opts": []}
            weapons.append(cur)
            if crit or eff or er:
                cur["opts"].append({"crit": crit, "eff": eff, "er": er})
        elif cur and (crit or eff or er):
            cur["opts"].append({"crit": crit, "eff": eff, "er": er})

    chars.append({
        "name": name, "tags": tags, "level": level, "talent": talent,
        "roles": roles, "arts": arts,
        "sands": sands, "goblet": goblet, "crown": crown, "substat": substat,
        "weapons": weapons, "remark": remark, "img": img,
    })

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(chars, f, ensure_ascii=False, indent=1)

print("characters:", len(chars))
print("names:", ", ".join(c["name"] for c in chars))
print("\n=== sample: 마비카 ===")
print(json.dumps(chars[0], ensure_ascii=False, indent=1))
print("\n=== sample: a A/B char (리니) ===")
for c in chars:
    if c["name"] == "리니":
        print(json.dumps(c, ensure_ascii=False, indent=1))
