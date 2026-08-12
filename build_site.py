# -*- coding: utf-8 -*-
import json

data = json.load(open("data.json", encoding="utf-8"))
imgs = json.load(open("images.json", encoding="utf-8"))
weap = json.load(open("weapons.json", encoding="utf-8"))
paimon = json.load(open("paimon.json", encoding="utf-8")).get("uri", "")
for c in data:
    m = imgs.get(c["name"], {})
    c["img"] = m.get("img", "")
    c["el"] = m.get("el", "")
    c["en"] = m.get("en", "")

DATA_JSON = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
WIMG_JSON = json.dumps(weap, ensure_ascii=False, separators=(",", ":"))

HTML = r"""<title>원신 캐릭터 빌드 뷰어</title>
<link rel="icon" type="image/webp" href="__PAIMON__">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#14131a">
<style>
  :root {
    --bg:#f3efe4; --card:#fffdf7; --card2:#f7f2e6;
    --ink:#2b2620; --ink-soft:#6b6252; --ink-faint:#9a9080;
    --line:#e4dcc9; --line-soft:#efe9db;
    --gold:#b1852f; --gold-bright:#caa044; --a:#2f6fb0; --b:#c2712c;
    --shadow:0 1px 2px rgba(60,48,20,.05), 0 10px 30px -14px rgba(60,48,20,.22);
    --font:"Pretendard","Apple SD Gothic Neo","Malgun Gothic",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  }
  @media (prefers-color-scheme:dark){
    :root{
      --bg:#14131a; --card:#1e1d28; --card2:#25242f;
      --ink:#ece7db; --ink-soft:#b0a892; --ink-faint:#7d7666;
      --line:#33313f; --line-soft:#2a2934;
      --gold:#d7ac52; --gold-bright:#eac878; --a:#6fa9e6; --b:#e0975a;
      --shadow:0 1px 2px rgba(0,0,0,.3), 0 12px 34px -16px rgba(0,0,0,.65);
    }
  }
  :root[data-theme="light"]{
    --bg:#f3efe4; --card:#fffdf7; --card2:#f7f2e6; --ink:#2b2620; --ink-soft:#6b6252;
    --ink-faint:#9a9080; --line:#e4dcc9; --line-soft:#efe9db; --gold:#b1852f;
    --gold-bright:#caa044; --a:#2f6fb0; --b:#c2712c;
    --shadow:0 1px 2px rgba(60,48,20,.05), 0 10px 30px -14px rgba(60,48,20,.22);
  }
  :root[data-theme="dark"]{
    --bg:#14131a; --card:#1e1d28; --card2:#25242f; --ink:#ece7db; --ink-soft:#b0a892;
    --ink-faint:#7d7666; --line:#33313f; --line-soft:#2a2934; --gold:#d7ac52;
    --gold-bright:#eac878; --a:#6fa9e6; --b:#e0975a;
    --shadow:0 1px 2px rgba(0,0,0,.3), 0 12px 34px -16px rgba(0,0,0,.65);
  }
  *{box-sizing:border-box;}
  body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--font);line-height:1.55;-webkit-font-smoothing:antialiased;}

  .topbar{
    position:sticky; top:0; z-index:30;
    background:linear-gradient(100deg, color-mix(in srgb,var(--gold) 16%,var(--bg)), var(--bg) 70%);
    border-bottom:1px solid var(--line); padding:11px 16px;
    display:flex; align-items:center; gap:10px; flex-wrap:wrap;
  }
  .paimon{ width:30px; height:30px; border-radius:50%; flex:0 0 auto; box-shadow:0 0 0 2px color-mix(in srgb,var(--gold) 45%,transparent);}
  .brand{font-size:16.5px; font-weight:800; letter-spacing:-.01em; display:flex; align-items:center; gap:8px; flex-wrap:wrap;}
  .brand .mk{color:var(--gold);}
  .ver{font-size:12px; font-weight:700; color:var(--ink-faint); letter-spacing:0;
    background:var(--card); border:1px solid var(--line); padding:2px 9px; border-radius:999px;}
  .viewtoggle{ margin-left:auto; display:flex; gap:3px; background:var(--card); border:1px solid var(--line); border-radius:999px; padding:3px;}
  .vt{ font-family:inherit; cursor:pointer; border:0; background:none; border-radius:999px; padding:5px 11px; font-size:15px; line-height:1; color:var(--ink-faint);}
  .vt.active{ background:var(--gold); color:#fff;}
  .vt:focus-visible{ outline:2px solid var(--gold); outline-offset:1px;}

  /* ===== mobile-first layout ===== */
  .layout{ max-width:560px; margin:0 auto; padding:12px 14px 34px; }
  .backbtn{ display:inline-flex; align-items:center; gap:6px; font-family:inherit; cursor:pointer;
    font-size:13.5px; font-weight:800; color:var(--gold); background:var(--card); border:1px solid var(--line);
    border-radius:999px; padding:8px 15px; margin-bottom:14px; }
  .backbtn:hover{ border-color:var(--gold);}
  .backbtn:focus-visible{ outline:2px solid var(--gold); outline-offset:2px;}

  .modetabs{ display:flex; gap:6px; margin-bottom:10px; }
  .mtab{ flex:1; font-family:inherit; cursor:pointer; font-size:14px; font-weight:800; color:var(--ink-soft);
    background:var(--card); border:1px solid var(--line); border-radius:10px; padding:10px 10px; display:flex; align-items:center; justify-content:center; gap:6px;}
  .mtab.active{ color:#fff; background:var(--gold); border-color:var(--gold);}
  .mtab:focus-visible{ outline:2px solid var(--gold); outline-offset:1px;}
  .search-wrap{ position:relative; }
  #search{
    width:100%; font-family:inherit; font-size:15px; color:var(--ink);
    background:var(--card); border:1px solid var(--line); border-radius:10px;
    padding:11px 12px 11px 36px; outline:none;
  }
  #search:focus{ border-color:var(--gold); box-shadow:0 0 0 3px color-mix(in srgb,var(--gold) 22%,transparent);}
  .search-wrap::before{ content:"🔍"; position:absolute; left:12px; top:50%; transform:translateY(-50%); font-size:14px; opacity:.6;}
  .elfilter{ display:flex; flex-wrap:wrap; gap:6px; margin:10px 0 4px;}
  .elbtn{ font-family:inherit; cursor:pointer; font-size:12.5px; font-weight:700; color:var(--ink-soft);
    background:var(--card); border:1px solid var(--line); border-radius:999px; padding:5px 11px; display:inline-flex; align-items:center; gap:5px;}
  .elbtn .dot{ width:9px; height:9px; border-radius:50%;}
  .elbtn.active{ font-weight:800; color:var(--gold); border-color:var(--gold); background:color-mix(in srgb,var(--gold) 14%,transparent);}
  .elbtn:focus-visible{ outline:2px solid var(--gold); outline-offset:1px;}
  .count{ font-size:12px; color:var(--ink-faint); margin:7px 2px 6px;}
  .charlist{ list-style:none; margin:0; padding:4px; border:1px solid var(--line-soft); border-radius:12px; background:var(--card);}
  .charlist::-webkit-scrollbar{width:9px;}
  .charlist::-webkit-scrollbar-thumb{background:var(--line); border-radius:9px; border:2px solid var(--card);}
  .citem{ display:flex; align-items:center; gap:11px; width:100%; text-align:left;
    font-family:inherit; cursor:pointer; background:none; border:0; color:inherit;
    padding:9px 10px; border-radius:9px;}
  .citem:hover{ background:var(--card2);}
  .citem.active{ background:color-mix(in srgb,var(--gold) 18%,transparent); }
  .citem.active .cn{ color:var(--gold); }
  .citem:focus-visible{ outline:2px solid var(--gold); outline-offset:1px;}
  .avatar{ width:40px; height:40px; border-radius:50%; flex:0 0 auto; display:grid; place-items:center;
    font-size:16px; font-weight:800; color:#fff; object-fit:cover; border:2px solid transparent; background:var(--card2);}
  .wsq{ border-radius:10px; }
  .wpnav{ background:color-mix(in srgb,var(--gold) 20%,var(--card2)); color:var(--gold);}
  .cmeta{ min-width:0; }
  .cn{ font-size:15px; font-weight:700; letter-spacing:-.01em; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}
  .ct{ font-size:11.5px; color:var(--ink-faint); white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}

  /* detail (hidden on mobile until a pick) */
  .detail{ min-width:0; display:none; }
  body.show-detail .picker{ display:none; }
  body.show-detail .detail{ display:block; }
  .empty{ color:var(--ink-faint); text-align:center; padding:70px 20px; font-size:15px;}
  .dhead{ display:flex; align-items:center; gap:14px; margin-bottom:4px; flex-wrap:wrap;}
  .dhead .avatar{ width:60px; height:60px; font-size:24px; border-width:3px;}
  .dname{ font-size:23px; font-weight:800; letter-spacing:-.02em;}
  .den{ font-size:12.5px; font-weight:700; color:var(--ink-faint); margin-top:1px;}
  .chips{ display:flex; gap:6px; flex-wrap:wrap; margin-top:6px; align-items:center;}
  .chip{ font-size:11.5px; font-weight:700; padding:3px 9px; border-radius:999px;
    background:color-mix(in srgb,var(--gold) 15%,transparent); color:var(--gold);}
  .elchip{ font-size:11.5px; font-weight:800; padding:3px 10px; border-radius:999px; color:#fff; display:inline-flex; align-items:center; gap:5px;}
  .facts{ display:flex; gap:8px; flex-wrap:wrap; margin:14px 0 4px;}
  .fact{ background:var(--card); border:1px solid var(--line-soft); border-radius:10px; padding:8px 12px; box-shadow:var(--shadow);}
  .fact .k{ font-size:10.5px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:var(--ink-faint);}
  .fact .v{ font-size:15px; font-weight:800; margin-top:2px;}

  .sec{ margin-top:18px; }
  .sec > h3{ font-size:12px; font-weight:800; letter-spacing:.08em; text-transform:uppercase;
    color:var(--gold); margin:0 0 9px; display:flex; align-items:center; gap:8px;}
  .sec > h3::after{ content:""; flex:1; height:1px; background:var(--line);}
  .card{ background:var(--card); border:1px solid var(--line-soft); border-radius:12px; padding:13px 15px; box-shadow:var(--shadow);}
  .lines > div{ padding:5px 0; font-size:14px;}
  .lines > div + div{ border-top:1px dashed var(--line);}
  .ab{ font-weight:800; }
  .ab.A{ color:var(--a);} .ab.B{ color:var(--b);}

  .stat3{ display:grid; grid-template-columns:1fr; gap:10px;}
  .statc{ background:var(--card); border:1px solid var(--line-soft); border-radius:12px; padding:11px 13px; box-shadow:var(--shadow);}
  .statc .k{ font-size:11px; font-weight:800; color:var(--ink-faint); margin-bottom:5px; display:flex; align-items:center; gap:5px;}
  .statc .val{ font-size:13.5px; font-weight:600; line-height:1.5;}
  .statc .val .row + .row{ margin-top:3px; padding-top:3px; border-top:1px dashed var(--line);}

  .wpn{ background:var(--card); border:1px solid var(--line-soft); border-radius:12px; padding:12px 14px; box-shadow:var(--shadow);}
  .wpn + .wpn{ margin-top:9px;}
  .wpn .wn{ font-size:14.5px; font-weight:800; color:var(--gold); margin-bottom:7px; display:flex; align-items:center; gap:8px;}
  .wicon{ width:26px; height:26px; border-radius:6px; object-fit:cover; background:var(--card2); flex:0 0 auto;}
  .opt{ display:flex; flex-wrap:wrap; gap:6px 8px; align-items:center; font-size:13px; padding:5px 0;}
  .opt + .opt{ border-top:1px dashed var(--line);}
  .ocrit{ font-weight:800; font-variant-numeric:tabular-nums; background:color-mix(in srgb,var(--gold) 16%,transparent);
    color:var(--gold); padding:2px 8px; border-radius:6px;}
  .oeff{ color:var(--ink-soft);}
  .oer{ color:var(--ink-faint); font-size:12px;}
  .oer b{ color:var(--ink-soft); font-weight:700;}

  .users{ display:grid; grid-template-columns:1fr; gap:9px;}
  .usercard{ display:flex; align-items:flex-start; gap:10px; text-align:left; width:100%;
    font-family:inherit; cursor:pointer; color:inherit;
    background:var(--card); border:1px solid var(--line-soft); border-radius:12px; padding:10px 12px; box-shadow:var(--shadow);}
  .usercard:hover{ border-color:var(--gold);}
  .usercard:focus-visible{ outline:2px solid var(--gold); outline-offset:1px;}
  .usercard .avatar{ width:40px; height:40px;}
  .un{ font-size:14px; font-weight:800; }
  .usub{ font-size:11px; color:var(--ink-faint); margin:1px 0 5px;}
  .uopt{ font-size:12px; color:var(--ink-soft); padding:2px 0;}
  .uopt .ocrit{ font-size:11.5px; padding:1px 6px; }

  /* ===== desktop layout (toggled by JS: body.d) ===== */
  body.d .layout{ max-width:1120px; padding:16px 18px 40px; display:grid; grid-template-columns:300px 1fr; gap:20px; align-items:start; }
  body.d .picker{ position:sticky; top:60px; }
  body.d .picker, body.d .detail{ display:block !important; }
  body.d .charlist{ max-height:calc(100vh - 230px); overflow-y:auto; }
  body.d .backbtn{ display:none; }
  body.d .stat3{ grid-template-columns:repeat(3,1fr); }
  body.d .users{ grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); }
  body.d .dname{ font-size:26px; }
  body.d .dhead .avatar{ width:66px; height:66px; font-size:26px; }
  html{ scroll-behavior:smooth;}
  @media (prefers-reduced-motion:reduce){ html{scroll-behavior:auto;} }
</style>

<div class="topbar">
  <img class="paimon" src="__PAIMON__" alt="Paimon">
  <div class="brand"><span class="mk">원신</span> 캐릭터 빌드 뷰어 <span class="ver">ver 6.7</span></div>
  <div class="viewtoggle" id="viewtoggle">
    <button type="button" class="vt" data-view="mobile" title="모바일 보기" aria-label="모바일 보기">📱</button>
    <button type="button" class="vt" data-view="web" title="웹 보기" aria-label="웹 보기">💻</button>
  </div>
</div>

<div class="layout">
  <aside class="picker">
    <div class="modetabs">
      <button type="button" class="mtab active" data-mode="char">🧝 캐릭터</button>
      <button type="button" class="mtab" data-mode="weapon">⚔️ 무기</button>
    </div>
    <div class="search-wrap"><input id="search" type="text" placeholder="검색 (이름:마비카, ㅁㅂㅋ, akqlzk 등)" autocomplete="off"></div>
    <div class="elfilter" id="elfilter"></div>
    <div class="count" id="count"></div>
    <ul class="charlist" id="charlist"></ul>
  </aside>
  <main class="detail" id="detail">
    <div class="empty">캐릭터를 선택하세요 👈</div>
  </main>
</div>

<script>
const DATA = __DATA__;
const WIMG = __WIMG__;
const RANK = {5:"#e0a63f", 4:"#a97fd0", 3:"#5f8fb0"};

const EL = {
  Fire:{c:"#e0663f",k:"불"}, Water:{c:"#3f9fe0",k:"물"}, Ice:{c:"#4fb6cf",k:"얼음"},
  Electric:{c:"#b06fd8",k:"번개"}, Wind:{c:"#3fb499",k:"바람"}, Rock:{c:"#d1a23f",k:"바위"}, Grass:{c:"#79b23f",k:"풀"}
};
const PAL = ["#c2712c","#2f8f6f","#3f6fb0","#9a5bb8","#c04b6a","#b1852f","#4a8fb0","#7a6bd0"];
const CHO = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ","ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"];
function cho(s){ let r=""; for(const ch of s){ const x=ch.charCodeAt(0);
  r += (x>=0xAC00&&x<=0xD7A3) ? CHO[Math.floor((x-0xAC00)/588)] : ch; } return r; }
const CHO_E=["r","R","s","e","E","f","a","q","Q","t","T","d","w","W","c","z","x","v","g"];
const JUNG_E=["k","o","i","O","j","p","u","P","h","hk","ho","hl","y","n","nj","np","nl","b","m","ml","l"];
const JONG_E=["","r","R","rt","s","sw","sg","e","f","fr","fa","fq","ft","fx","fv","fg","a","q","qt","t","T","d","w","c","z","x","v","g"];
function engKeys(s){ let r=""; for(const ch of s){ const x=ch.charCodeAt(0);
  if(x>=0xAC00&&x<=0xD7A3){ const n=x-0xAC00;
    r += CHO_E[Math.floor(n/588)] + JUNG_E[Math.floor((n%588)/28)] + JONG_E[n%28]; }
  else r += ch; } return r.toLowerCase(); }
function hues(name){ let h=0; for(const c of name) h=(h*31+c.charCodeAt(0))>>>0; return PAL[h%PAL.length]; }
function initial(name){ return (name||"?").trim().charAt(0); }
function esc(s){ return (s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"); }
function fmt(s){
  return esc(s).replace(/\n/g,"<br>")
    .replace(/(^|<br>)\s*(A\))/g,'$1<span class="ab A">$2</span>')
    .replace(/(^|<br>)\s*(B\))/g,'$1<span class="ab B">$2</span>');
}
function ring(c){ return EL[c.el] ? EL[c.el].c : "var(--line)"; }
function avatarHTML(c, cls){
  const r = ring(c);
  if(c.img) return '<img class="avatar'+(cls?' '+cls:'')+'" style="border-color:'+r+'" src="'+c.img+'" alt="'+esc(c.name)+'" loading="lazy">';
  return '<span class="avatar'+(cls?' '+cls:'')+'" style="background:'+hues(c.name)+';border-color:'+r+'">'+esc(initial(c.name))+'</span>';
}
function weaponAvatar(w, big){
  const col = RANK[w.rank] || "var(--line)";
  const st = big ? 'width:60px;height:60px;border-color:'+col : 'border-color:'+col;
  if(w.img) return '<img class="avatar wsq" style="'+st+'" src="'+w.img+'" alt="" loading="lazy">';
  return '<span class="avatar wsq wpnav" style="'+st+(big?';font-size:26px':'')+'">⚔</span>';
}
DATA.forEach(c=>{ c._k = [c.name, cho(c.name), engKeys(c.name), (c.en||"").toLowerCase(), (c.tags||[]).join(" ")].join(" "); });

// weapon index (group by base name)
function baseName(n){ let i=n.length; const p=n.indexOf("("); const s=n.indexOf("*");
  if(p>=0)i=Math.min(i,p); if(s>=0)i=Math.min(i,s); return n.slice(0,i).trim()||n; }
const WMAP={};
DATA.forEach(c=>{ (c.weapons||[]).forEach(w=>{ const b=baseName(w.name); const m=WIMG[b]||{};
  if(!WMAP[b]) WMAP[b]={name:b, _k:(b+" "+cho(b)+" "+engKeys(b)), img:m.img||"", rank:m.rank||0, users:[]};
  WMAP[b].users.push({name:c.name, opts:w.opts, full:w.name}); }); });
const WEAPONS = Object.values(WMAP).sort((a,b)=> b.users.length-a.users.length || a.name.localeCompare(b.name,"ko"));

function optsHTML(opts, small){
  return opts.map(o=>{ let p=[];
    if(o.crit) p.push('<span class="ocrit">'+esc(o.crit)+'</span>');
    if(o.eff)  p.push('<span class="oeff">'+fmt(o.eff)+'</span>');
    if(o.er)   p.push('<span class="oer"><b>원충</b> '+fmt(o.er)+'</span>');
    return '<div class="'+(small?'uopt':'opt')+'">'+p.join(" ")+'</div>';
  }).join("");
}
function linesCard(arr){ if(!arr||!arr.length) return "";
  return '<div class="card lines">'+arr.map(x=>'<div>'+fmt(x)+'</div>').join("")+'</div>'; }
function statCard(k, icon, arr){
  const val = (arr&&arr.length) ? arr.map(x=>'<div class="row">'+fmt(x)+'</div>').join("") : '<div class="row" style="color:var(--ink-faint)">-</div>';
  return '<div class="statc"><div class="k">'+icon+' '+k+'</div><div class="val">'+val+'</div></div>';
}
function weaponCard(w){
  const m = WIMG[baseName(w.name)] || {};
  const ic = m.img ? '<img class="wicon" src="'+m.img+'" alt="" loading="lazy">' : '';
  return '<div class="wpn"><div class="wn">'+ic+esc(w.name)+'</div>'+optsHTML(w.opts)+'</div>';
}

function renderCharDetail(c){
  const chips = (c.tags||[]).map(t=>'<span class="chip">'+esc(t)+'</span>').join("");
  const elc = EL[c.el] ? '<span class="elchip" style="background:'+EL[c.el].c+'">'+EL[c.el].k+' 원소</span>' : '';
  const en = c.en ? '<div class="den">'+esc(c.en)+'</div>' : '';
  let h = '<div class="dhead">'+avatarHTML(c)+'<div><div class="dname">'+esc(c.name)+'</div>'+en
        + '<div class="chips">'+elc+chips+'</div></div></div>';
  h += '<div class="facts">';
  if(c.level)  h += '<div class="fact"><div class="k">권장 레벨/특성</div><div class="v">'+esc(c.level)+'</div></div>';
  if(c.talent) h += '<div class="fact"><div class="k">특성</div><div class="v">'+esc(c.talent)+'</div></div>';
  h += '</div>';
  if(c.roles&&c.roles.length) h += '<div class="sec"><h3>역할군</h3>'+linesCard(c.roles)+'</div>';
  if(c.arts&&c.arts.length)   h += '<div class="sec"><h3>성유물</h3>'+linesCard(c.arts)+'</div>';
  h += '<div class="sec"><h3>주 옵션</h3><div class="stat3">'
     + statCard("시계","⏳",c.sands) + statCard("성배","🍷",c.goblet) + statCard("왕관","👑",c.crown) + '</div></div>';
  if(c.substat&&c.substat.length) h += '<div class="sec"><h3>권장 부옵션</h3>'+linesCard(c.substat)+'</div>';
  if(c.weapons&&c.weapons.length) h += '<div class="sec"><h3>추천 무기 · 권장 스탯</h3>'+c.weapons.map(weaponCard).join("")+'</div>';
  if(c.remark&&c.remark.length)   h += '<div class="sec"><h3>비고</h3>'+linesCard(c.remark)+'</div>';
  showDetail(h);
}
function renderWeaponDetail(w){
  let users = w.users.map(u=>{
    const c = DATA.find(x=>x.name===u.name) || {name:u.name};
    const sub = u.full!==w.name ? '<div class="usub">'+esc(u.full)+'</div>' : '';
    const el = EL[c.el] ? '<span class="elchip" style="background:'+EL[c.el].c+';font-size:10px;padding:1px 7px">'+EL[c.el].k+'</span>' : '';
    return '<button class="usercard" data-name="'+esc(u.name)+'">'+avatarHTML(c)
      + '<div style="min-width:0"><div class="un">'+esc(u.name)+' '+el+'</div>'+sub+optsHTML(u.opts,true)+'</div></button>';
  }).join("");
  let h = '<div class="dhead">'+weaponAvatar(w,true)
    + '<div><div class="dname">'+esc(w.name)+'</div><div class="chips"><span class="chip">'+w.users.length+'명 사용</span></div></div></div>'
    + '<div class="sec"><h3>이 무기를 쓰는 캐릭터</h3><div class="users">'+users+'</div></div>';
  showDetail(h);
}
function showDetail(html){
  const d=document.getElementById("detail");
  d.innerHTML = '<button class="backbtn" type="button" data-back>← 목록으로</button>'+html;
  document.body.classList.add("show-detail");
  window.scrollTo(0,0);
}
function goBack(){ document.body.classList.remove("show-detail"); window.scrollTo(0,0); }

const listEl = document.getElementById("charlist");
const countEl = document.getElementById("count");
const elfEl = document.getElementById("elfilter");
const searchEl = document.getElementById("search");
let mode = "char";
let activeName = null, activeWeapon = null;
let elFilter = "";

const elsPresent = [];
DATA.forEach(c=>{ if(c.el && !elsPresent.includes(c.el)) elsPresent.push(c.el); });
const order = ["Fire","Water","Ice","Electric","Wind","Rock","Grass"];
elsPresent.sort((a,b)=>order.indexOf(a)-order.indexOf(b));
elfEl.innerHTML = '<button class="elbtn active" data-el="">전체</button>'
  + elsPresent.map(e=>'<button class="elbtn" data-el="'+e+'"><span class="dot" style="background:'+EL[e].c+'"></span>'+EL[e].k+'</button>').join("");
elfEl.addEventListener("click", e=>{
  const b=e.target.closest(".elbtn"); if(!b) return;
  elFilter=b.dataset.el;
  [...elfEl.children].forEach(x=>{ x.classList.remove("active"); x.style.color=""; x.style.borderColor=""; x.style.background=""; });
  b.classList.add("active");
  if(elFilter){ const col=EL[elFilter].c; b.style.color=col; b.style.borderColor=col; b.style.background="color-mix(in srgb,"+col+" 15%,transparent)"; }
  buildList();
});

function buildList(){
  const q = searchEl.value.trim().toLowerCase();
  if(mode==="char"){
    elfEl.style.display="flex";
    const items = DATA.filter(c=>{
      if(elFilter && c.el!==elFilter) return false;
      return !q || c._k.toLowerCase().includes(q);
    });
    countEl.textContent = items.length+" / "+DATA.length+" 캐릭터";
    listEl.innerHTML = items.map(c=>{
      const active = c.name===activeName ? " active":"";
      return '<li><button class="citem'+active+'" data-name="'+esc(c.name)+'">'+avatarHTML(c)
        + '<span class="cmeta"><span class="cn">'+esc(c.name)+'</span></span></button></li>';
    }).join("");
  } else {
    elfEl.style.display="none";
    const items = WEAPONS.filter(w=> !q || w._k.toLowerCase().includes(q));
    countEl.textContent = items.length+" / "+WEAPONS.length+" 무기";
    listEl.innerHTML = items.map(w=>{
      const active = w.name===activeWeapon ? " active":"";
      return '<li><button class="citem'+active+'" data-weapon="'+esc(w.name)+'">'
        + weaponAvatar(w,false)
        + '<span class="cmeta"><span class="cn">'+esc(w.name)+'</span>'
        + '<span class="ct">'+w.users.length+'명 사용</span></span></button></li>';
    }).join("");
  }
}

listEl.addEventListener("click", e=>{
  const btn = e.target.closest(".citem"); if(!btn) return;
  if(btn.dataset.name){ activeName=btn.dataset.name; const c=DATA.find(x=>x.name===activeName); if(c) renderCharDetail(c); }
  else if(btn.dataset.weapon){ activeWeapon=btn.dataset.weapon; const w=WEAPONS.find(x=>x.name===activeWeapon); if(w) renderWeaponDetail(w); }
  buildList();
});
document.getElementById("detail").addEventListener("click", e=>{
  if(e.target.closest("[data-back]")){ goBack(); return; }
  const u = e.target.closest(".usercard"); if(!u) return;
  switchMode("char"); activeName=u.dataset.name;
  const c=DATA.find(x=>x.name===activeName); if(c) renderCharDetail(c);
  buildList();
});
searchEl.addEventListener("input", buildList);

function switchMode(m){
  mode=m;
  [...document.querySelectorAll(".mtab")].forEach(t=>t.classList.toggle("active", t.dataset.mode===m));
  searchEl.value="";
  searchEl.placeholder = m==="char" ? "검색 (이름:마비카, ㅁㅂㅋ, akqlzk 등)" : "무기 검색 (이름, ㅁㅂㅋ, akqlzk 등)";
  buildList();
}
document.querySelectorAll(".mtab").forEach(t=> t.addEventListener("click", ()=> switchMode(t.dataset.mode)));

// ===== web / mobile view toggle =====
const mql = window.matchMedia("(min-width:821px)");
let viewPref = "auto";
try{ viewPref = localStorage.getItem("viewPref") || "auto"; }catch(e){}
function applyView(){
  const desktop = viewPref==="web" || (viewPref==="auto" && mql.matches);
  document.body.classList.toggle("d", desktop);
  document.querySelectorAll(".vt").forEach(b=>
    b.classList.toggle("active", b.dataset.view==="web" ? desktop : !desktop));
}
if(mql.addEventListener) mql.addEventListener("change", ()=>{ if(viewPref==="auto") applyView(); });
document.querySelectorAll(".vt").forEach(b=> b.addEventListener("click", ()=>{
  viewPref = b.dataset.view;
  try{ localStorage.setItem("viewPref", viewPref); }catch(e){}
  applyView();
}));
applyView();

buildList();
</script>
"""

out = HTML.replace("__DATA__", DATA_JSON).replace("__WIMG__", WIMG_JSON).replace("__PAIMON__", paimon)
open("genshin-build.html", "w", encoding="utf-8").write(out)
print("written genshin-build.html, bytes:", len(out.encode("utf-8")))
