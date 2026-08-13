# -*- coding: utf-8 -*-
import json, os, base64, io, time, urllib.request
from PIL import Image, ImageDraw

os.makedirs("icons", exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0"}

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()

if not os.path.exists("amber.json"):
    open("amber.json", "wb").write(get("https://gi.yatta.moe/api/v2/kr/avatar"))
amber = json.load(open("amber.json", encoding="utf-8"))["data"]["items"]
byname = {v["name"]: v for v in amber.values()}
byname_n = {k.replace(" ", ""): v for k, v in byname.items()}
# id -> kr value ; and name -> id
name2id = {}
for cid, v in amber.items():
    name2id[v["name"]] = cid
name2id_n = {k.replace(" ", ""): i for k, i in name2id.items()}
# english names by id
if not os.path.exists("amber_en.json"):
    open("amber_en.json", "wb").write(get("https://gi.yatta.moe/api/v2/en/avatar"))
en_items = json.load(open("amber_en.json", encoding="utf-8"))["data"]["items"]
id2en = {cid: v.get("name", "") for cid, v in en_items.items()}

ours = json.load(open("data.json", encoding="utf-8"))

# 표에는 올라왔지만 ambr API에 아직 없는 미출시 캐릭터의 원소 (수동 보정).
# API에 추가되면 API 값이 우선하므로 이 항목은 그때 지우면 됨.
MANUAL_EL = {
    "알료샤": "Electric",
    "오데트": "Ice",
}


def el_from_name(n):
    if "불" in n: return "Fire"
    if "물" in n: return "Water"
    if "얼음" in n: return "Ice"
    if "번개" in n: return "Electric"
    if "바람" in n: return "Wind"
    if "바위" in n: return "Rock"
    if "풀" in n: return "Grass"
    return ""

def fetch_png(icon):
    path = os.path.join("icons", icon + ".png")
    if os.path.exists(path) and os.path.getsize(path) > 100:
        return open(path, "rb").read()
    url = "https://gi.yatta.moe/assets/UI/%s.png" % icon
    req = urllib.request.Request(url, headers=UA)
    data = urllib.request.urlopen(req, timeout=30).read()
    open(path, "wb").write(data)
    return data

def placeholder_webp(size=96, q=82):
    """API에 아직 없는 미출시 캐릭터용 중립 실루엣 (여행자 아이콘 오용 방지)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = size / 96.0
    d.ellipse([0, 0, size - 1, size - 1], fill=(150, 143, 128, 60))
    d.ellipse([34 * s, 22 * s, 62 * s, 50 * s], fill=(150, 143, 128, 165))
    d.ellipse([20 * s, 56 * s, 76 * s, 104 * s], fill=(150, 143, 128, 165))
    buf = io.BytesIO()
    im.save(buf, format="WEBP", quality=q, method=6)
    return buf.getvalue()


def to_webp(png_bytes, size=96, q=82):
    im = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
    im = im.resize((size, size), Image.LANCZOS)
    # flatten transparency onto nothing -> keep alpha via webp
    buf = io.BytesIO()
    im.save(buf, format="WEBP", quality=q, method=6)
    return buf.getvalue()

out = {}
fails = []
unknown = []
for i, c in enumerate(ours):
    name = c["name"]
    v = byname.get(name) or byname_n.get(name.replace(" ", ""))
    cid = name2id.get(name) or name2id_n.get(name.replace(" ", ""))
    en = id2en.get(cid, "") if cid else ""
    icon = None
    if v:
        icon = v["icon"]; el = v.get("element", "")
    elif "여행자" in name:
        # 원소별 여행자는 API에 개별 항목이 없음 — 여행자 아이콘 + 이름에서 원소 추론
        icon = "UI_AvatarIcon_PlayerGirl"; el = el_from_name(name); en = "Traveler"
    else:
        # 표에는 있으나 API에 아직 없는 미출시 캐릭터.
        # 여행자로 대체하면 잘못된 초상화 + 영문 검색 오염이 생기므로 플레이스홀더 사용.
        unknown.append(name); el = MANUAL_EL.get(name, ""); en = ""
    try:
        webp = to_webp(fetch_png(icon)) if icon else placeholder_webp()
        uri = "data:image/webp;base64," + base64.b64encode(webp).decode()
        out[name] = {"img": uri, "el": el, "en": en}
    except Exception as e:
        fails.append((name, icon, str(e)))
        out[name] = {"img": "", "el": el, "en": en}
    if i % 20 == 0:
        print("...", i, name.encode("ascii", "replace").decode())

json.dump(out, open("images.json", "w", encoding="utf-8"), ensure_ascii=False)
total = sum(len(v["img"]) for v in out.values())
print("done. entries:", len(out), "| with img:", sum(1 for v in out.values() if v["img"]))
print("with en:", sum(1 for v in out.values() if v.get("en")))
print("approx base64 chars total:", total, "(~%.1f MB)" % (total/1024/1024))
print("fails:", len(fails), fails[:5])
print("unknown (API 미등재 -> 플레이스홀더):", len(unknown),
      [n.encode("ascii", "replace").decode() for n in unknown])

# --- Paimon CI icon (official Genshin favicon) ---
paimon_sources = [
    "https://genshin.hoyoverse.com/favicon.ico",
    "https://act.hoyoverse.com/favicon.ico",
    "https://webstatic.hoyoverse.com/favicon.ico",
]
pu = ""
for u in paimon_sources:
    try:
        raw = get(u)
        im = Image.open(io.BytesIO(raw)).convert("RGBA")
        # pick largest frame if multi-size ico
        im = im.resize((64, 64), Image.LANCZOS)
        buf = io.BytesIO(); im.save(buf, format="WEBP", quality=90, method=6)
        pu = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
        print("paimon from", u, "bytes", len(raw))
        break
    except Exception as e:
        print("paimon fail", u, str(e)[:60])
json.dump({"uri": pu}, open("paimon.json", "w", encoding="utf-8"))
