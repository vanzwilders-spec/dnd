#!/usr/bin/env python3
"""Build a themed HTML guide from a Markdown source.

Usage: build_html.py SOURCE.md OUT.html --kind player [--sidebar-title "A Player's" --sidebar-sub "Companion"]

Rules:
- "# Title" + italic line + blockquote at the top become the cover.
- Each "## Heading" becomes a card and a sidebar link.
- "### Session N: ..." becomes a color-coded session block.
- For --kind player, the section titled "Session Notes" is replaced by a
  browser-saved notes tool (the Markdown keeps a plain template for Scribe).
"""
import argparse
import html
import re

import markdown

CSS = """
:root{--bg-main:#0d0a08;--bg-sidebar:#1a1208;--bg-card:#2a1f15;--text-primary:#e8d5a8;--text-secondary:#b8a080;
--text-dim:#8a7560;--gold:#8b6914;--gold-light:#d4a017;--gold-bright:#f0c040;--blood:#6b0000;--blood-light:#8b1a1a;}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg-main);color:var(--text-primary);font-family:'Crimson Text',Georgia,serif;font-size:18px;line-height:1.7}
h1,h2,h3,.cinzel{font-family:'Cinzel',Georgia,serif;font-weight:600}
::-webkit-scrollbar{width:8px}::-webkit-scrollbar-track{background:var(--bg-main)}::-webkit-scrollbar-thumb{background:var(--gold);border-radius:4px}
.sidebar{position:fixed;left:0;top:0;bottom:0;width:280px;background:var(--bg-sidebar);border-right:1px solid rgba(139,105,20,.3);z-index:40;display:flex;flex-direction:column;overflow-y:auto}
.side-head{padding:1.75rem 1.5rem 1rem;border-bottom:1px solid rgba(139,105,20,.2)}
.side-eyebrow{font-family:'Cinzel',serif;font-size:.7rem;text-transform:uppercase;letter-spacing:.2em;color:var(--gold)}
.side-title{font-family:'Cinzel',serif;font-size:1rem;color:var(--gold-light);letter-spacing:.05em;margin-top:2px}
.side-sub{font-size:.8rem;color:var(--text-dim);margin-top:.5rem;font-style:italic}
nav{padding:1rem 0;flex:1}
.nav-link{display:block;padding:.7rem 1.25rem;color:var(--text-secondary);text-decoration:none;font-size:15px;border-left:2px solid transparent;transition:all .2s}
.nav-link:hover{color:var(--gold-light);background:rgba(139,105,20,.08)}
.nav-link.active{color:var(--gold-light);border-left-color:var(--gold-light);background:rgba(139,105,20,.12)}
.main{margin-left:280px;min-height:100vh}
.wrap{max-width:900px;margin:0 auto;padding:2.5rem 2rem 4rem}
.hero{text-align:center;padding:3rem 1rem 2rem}
.hero h1{font-size:2.2rem;line-height:1.3;letter-spacing:.1em;color:var(--gold-bright);margin:.25rem 0 .75rem;text-shadow:0 0 30px rgba(212,160,23,.25)}
.hero .sub{color:var(--text-secondary);font-style:italic}
.hero blockquote{margin:1.5rem auto 0;max-width:36rem;border:0;background:none;color:var(--gold-light);font-style:italic;font-size:1.25rem;padding:0}
.section-card{background:var(--bg-card);border:1px solid rgba(139,105,20,.2);border-radius:8px;padding:2rem;margin-bottom:1.5rem;scroll-margin-top:1rem}
.section-card h2{color:var(--gold-light);margin-top:0;font-size:1.6rem;letter-spacing:.06em;border-bottom:1px solid rgba(139,105,20,.25);padding-bottom:.6rem}
.section-card h3{color:var(--gold-bright);font-size:1.1rem;letter-spacing:.05em;margin:1.6rem 0 .5rem}
.section-card p,.section-card li{color:var(--text-primary)}
.section-card strong{color:var(--gold-bright)}
.section-card em{color:var(--text-secondary)}
blockquote{border-left:3px solid var(--gold-light);background:rgba(139,105,20,.1);margin:1.5rem 0;padding:1rem 1.5rem;border-radius:0 6px 6px 0}
blockquote p{margin:.3rem 0}
.divider{text-align:center;color:var(--gold);font-size:1.2rem;padding:.5rem 0 1.25rem;opacity:.6;letter-spacing:.5em}
table{width:100%;border-collapse:collapse;margin:1rem 0;font-size:.95rem}
th,td{border:1px solid rgba(139,105,20,.25);padding:.5rem .7rem;text-align:left;vertical-align:top}
th{background:rgba(139,105,20,.15);color:var(--gold-light);font-family:'Cinzel',serif;font-size:.8rem;letter-spacing:.06em}
tr:nth-child(even) td{background:rgba(0,0,0,.12)}
.table-scroll{overflow-x:auto}
.session-preview{border-radius:8px;padding:1.5rem 1.75rem;background:rgba(0,0,0,.18);margin:1.25rem 0;position:relative;overflow:hidden}
.session-preview::before{content:'';position:absolute;top:0;left:0;right:0;height:3px}
.session-preview h3{margin-top:.25rem}
.s1{border:1px solid rgba(122,94,160,.35)}.s1::before{background:linear-gradient(90deg,#7a5ea0,#8b6914)}
.s2{border:1px solid rgba(196,146,42,.35)}.s2::before{background:linear-gradient(90deg,#c4922a,#d4a017)}
.s3{border:1px solid rgba(106,138,154,.35)}.s3::before{background:linear-gradient(90deg,#4a6a7a,#6a8a9a)}
.s4{border:1px solid rgba(139,26,26,.4)}.s4::before{background:linear-gradient(90deg,#6b0000,#8b1a1a)}
hr{border:0;border-top:1px solid rgba(139,105,20,.2);margin:1.5rem 0}
.footer{text-align:center;color:var(--text-dim);font-style:italic;padding:2rem 0}
.mobile-header{display:none}
/* notes tool */
.notes-tabs{display:flex;gap:.5rem;flex-wrap:wrap;margin:1rem 0}
.notes-tab{background:transparent;color:var(--text-secondary);border:1px solid rgba(139,105,20,.35);border-radius:4px;padding:.4rem .9rem;font-family:'Cinzel',serif;font-size:.75rem;letter-spacing:.08em;cursor:pointer}
.notes-tab.active{background:rgba(139,105,20,.25);color:var(--gold-bright);border-color:var(--gold-light)}
.notes-pane{display:none}.notes-pane.active{display:block}
.notes-pane label{display:block;font-family:'Cinzel',serif;font-size:.7rem;text-transform:uppercase;letter-spacing:.15em;color:var(--gold);margin:1rem 0 .3rem}
.notes-pane textarea{width:100%;min-height:110px;background:rgba(0,0,0,.25);color:var(--text-primary);border:1px solid rgba(139,105,20,.3);border-radius:6px;padding:.7rem;font-family:'Crimson Text',serif;font-size:16px;resize:vertical}
.notes-pane textarea:focus{outline:none;border-color:var(--gold-light)}
.btn{background:var(--gold);color:#fff;border:0;border-radius:4px;padding:.5rem 1.1rem;font-family:'Cinzel',serif;font-size:.75rem;letter-spacing:.1em;cursor:pointer}
.btn:hover{background:var(--gold-light);color:#1a1208}
.notes-status{color:var(--text-dim);font-size:.85rem;margin-left:.75rem;font-style:italic}
@media(max-width:900px){
 .sidebar{transform:translateX(-100%);transition:transform .25s}.sidebar.open{transform:none}
 .main{margin-left:0}.mobile-header{display:flex;align-items:center;position:sticky;top:0;z-index:30;background:var(--bg-sidebar);border-bottom:1px solid rgba(139,105,20,.3);padding:.6rem 1rem}
 .mobile-header button{background:none;border:0;color:var(--gold-light);font-size:1.5rem;cursor:pointer;margin-right:.75rem}
 .mobile-header span{font-family:'Cinzel',serif;font-size:.8rem;letter-spacing:.1em;color:var(--gold-light)}
 .wrap{padding:1.5rem 1rem 3rem}.hero h1{font-size:1.8rem}.section-card{padding:1.25rem}
}
"""

NOTES_HTML = """
<p>Track what you discover. In this campaign, details matter. Notes save in this browser as you type.</p>
<div class="notes-tabs" id="notes-tabs"></div>
<div id="notes-panes"></div>
<p><button class="btn" id="notes-export" type="button">Export all notes (.md)</button><span class="notes-status" id="notes-status"></span></p>
<script>
(function(){
  var SESSIONS=[["1","The Inheritance"],["2","Harvest of the Hollow"],["3","No Signal"],["4","The Grand Theater"]];
  var FIELDS=["General notes","NPCs met","Mysteries and open questions","Things that felt important"];
  var KEY="reveler-notes-v1", data={}, status=document.getElementById("notes-status");
  try{data=JSON.parse(localStorage.getItem(KEY)||"{}");}catch(e){data={};}
  function save(){try{localStorage.setItem(KEY,JSON.stringify(data));status.textContent="Saved";}catch(e){status.textContent="Could not save in this browser. Use Export.";}}
  var tabs=document.getElementById("notes-tabs"), panes=document.getElementById("notes-panes"), timer=null;
  SESSIONS.forEach(function(s,i){
    var b=document.createElement("button");b.type="button";b.className="notes-tab"+(i===0?" active":"");b.textContent="Session "+s[0];tabs.appendChild(b);
    var p=document.createElement("div");p.className="notes-pane"+(i===0?" active":"");
    var h=document.createElement("h3");h.textContent=s[1];p.appendChild(h);
    FIELDS.forEach(function(f,j){
      var id="s"+s[0]+"f"+j,l=document.createElement("label");l.textContent=f;l.htmlFor=id;
      var t=document.createElement("textarea");t.id=id;t.value=data[id]||"";
      t.addEventListener("input",function(){data[id]=t.value;status.textContent="Saving...";clearTimeout(timer);timer=setTimeout(save,400);});
      p.appendChild(l);p.appendChild(t);
    });
    panes.appendChild(p);
    b.addEventListener("click",function(){
      Array.prototype.forEach.call(tabs.children,function(x){x.classList.remove("active");});
      Array.prototype.forEach.call(panes.children,function(x){x.classList.remove("active");});
      b.classList.add("active");p.classList.add("active");
    });
  });
  document.getElementById("notes-export").addEventListener("click",function(){
    var out="# The Reveler's Stage: My Notes\\n\\n";
    SESSIONS.forEach(function(s){
      out+="## Session "+s[0]+": "+s[1]+"\\n\\n";
      FIELDS.forEach(function(f,j){out+="### "+f+"\\n\\n"+(data["s"+s[0]+"f"+j]||"")+"\\n\\n";});
    });
    var a=document.createElement("a");a.href=URL.createObjectURL(new Blob([out],{type:"text/markdown"}));
    a.download="Revelers_Stage_My_Notes.md";document.body.appendChild(a);a.click();document.body.removeChild(a);
  });
})();
</script>
"""

NAV_JS = """
<script>
(function(){
  var links=document.querySelectorAll('.nav-link'), side=document.getElementById('sidebar');
  var map={};links.forEach(function(l){map[l.getAttribute('href').slice(1)]=l;});
  var cards=Array.prototype.slice.call(document.querySelectorAll('.section-card'));
  function setActive(){
    var cur=cards[0], line=window.innerHeight*0.3;
    cards.forEach(function(c){if(c.getBoundingClientRect().top<=line)cur=c;});
    links.forEach(function(l){l.classList.remove('active');});
    if(cur&&map[cur.id])map[cur.id].classList.add('active');
  }
  window.addEventListener('scroll',setActive,{passive:true});setActive();
  var btn=document.getElementById('menu-btn');
  if(btn)btn.addEventListener('click',function(){side.classList.toggle('open');});
  links.forEach(function(l){l.addEventListener('click',function(){side.classList.remove('open');});});
})();
</script>
"""


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def md_to_html(text):
    out = markdown.markdown(text, extensions=["tables", "sane_lists"])
    # drop table headers that are entirely empty
    out = re.sub(r"<thead>\s*<tr>(?:\s*<th>\s*</th>)+\s*</tr>\s*</thead>", "", out)
    out = out.replace("<table>", '<div class="table-scroll"><table>').replace("</table>", "</table></div>")
    # wrap Session blocks (h3 "Session N")
    parts = re.split(r"(?=<h3>)", out)
    wrapped = []
    for part in parts:
        m = re.match(r"<h3>Session (\d)", part)
        if m:
            wrapped.append(f'<div class="session-preview s{m.group(1)}">{part}</div>')
        else:
            wrapped.append(part)
    return "".join(wrapped)


def build(src, dst, kind, side_eyebrow, side_title, side_sub, doc_title):
    raw = open(src, encoding="utf-8").read()
    head, *sections = re.split(r"\n## ", raw)

    # cover
    cover_lines = [l for l in head.splitlines() if l.strip()]
    title = cover_lines[0].lstrip("# ").strip()
    subtitle, tagline = "", ""
    for l in cover_lines[1:]:
        if l.startswith(">"):
            tagline = l.lstrip("> ").strip()
        elif l.startswith("*") and not subtitle:
            subtitle = l.strip("*").strip()

    cards, nav = [], []
    footer = ""
    for sec in sections:
        name, _, body = sec.partition("\n")
        name = name.strip()
        body = body.rstrip()
        # strip trailing hr
        body = re.sub(r"\n---\s*$", "", body).rstrip()
        # pull the closing italic line into the footer
        m = re.search(r"\n\*([^*\n]+)\*\s*$", body)
        if m and "·" in m.group(1):
            footer = m.group(1)
            body = body[: m.start()].rstrip()
        sid = slug(name)
        nav.append((sid, name))
        if kind == "player" and name == "Session Notes":
            inner = NOTES_HTML
        else:
            inner = md_to_html(body)
        cards.append(f'<section class="section-card" id="{sid}"><h2>{html.escape(name)}</h2>{inner}</section>')

    nav_html = "".join(f'<a class="nav-link" href="#{i}">{html.escape(n)}</a>' for i, n in nav)
    cards_html = '\n<div class="divider">&#9901; &#9901; &#9901;</div>\n'.join(cards)

    page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(doc_title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Crimson+Text:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body>
<div class="mobile-header"><button id="menu-btn" type="button" aria-label="Menu">&#9776;</button><span>THE REVELER'S STAGE</span></div>
<aside class="sidebar" id="sidebar">
 <div class="side-head"><div class="side-eyebrow">{html.escape(side_eyebrow)}</div><div class="side-title">{html.escape(side_title)}</div><div class="side-sub">{html.escape(side_sub)}</div></div>
 <nav>{nav_html}</nav>
</aside>
<div class="main"><div class="wrap">
 <header class="hero"><h1>{html.escape(title)}</h1><div class="sub">{html.escape(subtitle)}</div><blockquote>{html.escape(tagline)}</blockquote></header>
 {cards_html}
 <div class="footer">{html.escape(footer)}</div>
</div></div>
{NAV_JS}
</body></html>"""
    open(dst, "w", encoding="utf-8").write(page)
    print(f"wrote {dst}: {len(sections)} sections, {len(page)} bytes")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--kind", default="player", choices=["player", "dm"])
    ap.add_argument("--eyebrow", default="A Player's")
    ap.add_argument("--side-title", default="Companion")
    ap.add_argument("--side-sub", default="D&D 5e Campaign Guide")
    ap.add_argument("--doc-title", default="The Reveler's Stage - Player Guide")
    a = ap.parse_args()
    build(a.src, a.dst, a.kind, a.eyebrow, a.side_title, a.side_sub, a.doc_title)
