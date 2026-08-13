# -*- coding: utf-8 -*-
import json, os, base64, io, urllib.request, difflib
from PIL import Image

UA = {"User-Agent": "Mozilla/5.0"}
def get(url): return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()

os.makedirs("wicons", exist_ok=True)
if not os.path.exists("amber_weapon.json"):
    open("amber_weapon.json", "wb").write(get("https://gi.yatta.moe/api/v2/kr/weapon"))
witems = json.load(open("amber_weapon.json", encoding="utf-8"))["data"]["items"]
byname = {v["name"]: v for v in witems.values()}
byname_n = {k.replace(" ", ""): v for k, v in byname.items()}

def base_name(n):
    i = len(n)
    p = n.find("("); s = n.find("*")
    if p >= 0: i = min(i, p)
    if s >= 0: i = min(i, s)
    return n[:i].strip() or n

data = json.load(open("data.json", encoding="utf-8"))
bases = []
seen = set()
for c in data:
    for w in c.get("weapons", []):
        b = base_name(w["name"])
        if b not in seen:
            seen.add(b); bases.append(b)

def fetch_png(icon):
    path = os.path.join("wicons", icon + ".png")
    if os.path.exists(path) and os.path.getsize(path) > 100:
        return open(path, "rb").read()
    d = get("https://gi.yatta.moe/assets/UI/%s.png" % icon)
    open(path, "wb").write(d); return d

def to_webp(png, size=96, q=84):
    im = Image.open(io.BytesIO(png)).convert("RGBA").resize((size, size), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, format="WEBP", quality=q, method=6)
    return buf.getvalue()

def lookup(b):
    v = byname.get(b) or byname_n.get(b.replace(" ", ""))
    if v:
        return v, None
    # 원본 표의 오탈자 대응: 공백 무시 후 유사도 폴백
    cand = difflib.get_close_matches(b.replace(" ", ""), list(byname_n), n=1, cutoff=0.8)
    if cand:
        return byname_n[cand[0]], cand[0]
    return None, None

out = {}
miss = []
fuzzy = []
for b in bases:
    v, alias = lookup(b)
    if alias:
        fuzzy.append("%s -> %s" % (b, v["name"]))
    if not v:
        miss.append(b); out[b] = {"img": "", "rank": 0}; continue
    try:
        png = fetch_png(v["icon"])
        uri = "data:image/webp;base64," + base64.b64encode(to_webp(png)).decode()
        out[b] = {"img": uri, "rank": v.get("rank", 0)}
    except Exception as e:
        miss.append(b); out[b] = {"img": "", "rank": v.get("rank", 0)}

json.dump(out, open("weapons.json", "w", encoding="utf-8"), ensure_ascii=False)
total = sum(len(x["img"]) for x in out.values())
print("weapon bases:", len(bases), "| matched:", sum(1 for x in out.values() if x["img"]))
print("approx img total: %.2f MB" % (total/1024/1024))
open("wmiss.txt", "w", encoding="utf-8").write(
    "MISSING (%d):\n" % len(miss) + "\n".join(miss)
    + "\n\nFUZZY (%d):\n" % len(fuzzy) + "\n".join(fuzzy))
print("missing count:", len(miss), "| fuzzy-matched:", len(fuzzy))
