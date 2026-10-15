#!/usr/bin/env python3
"""Build a themed HTML guide from a Markdown source.

Usage: build_html.py SOURCE.md OUT.html --kind player|dm|table [--sidebar-title "A Player's" --sidebar-sub "Companion"]

Rules:
- "# Title" + italic line + blockquote at the top become the cover.
- Each "## Heading" becomes a card and a sidebar link.
- "### Session N: ..." becomes a color-coded session block.
- --kind sets the dominant color and margin art: dm = blood red, player = cauldron
  green, table = witch purple. All share black, gold and fall accents.
- One illuminated (drop-cap) letter per document: on the opening prose paragraph
  if there is one, otherwise on the cover's intro line.
- For --kind player, the section titled "Session Notes" is replaced by a
  browser-saved notes tool (the Markdown keeps a plain template for Scribe).
"""
import argparse
import html
import re

import markdown

CSS = """
:root{--bg-main:#0c0a0b;--gold:#a8832f;--gold-light:#d9b25c;--gold-bright:#f0d48a;--pumpkin:#c8671e;
--text-primary:#e8dcc2;--text-secondary:#bfae8e;--text-dim:#8c7d68;--rule:rgba(168,131,47,.35)}
/* dominant color per document type; the other two hues stay on as accents */
body.kind-dm{--hue:#9e2424;--hue-light:#e0705f;--hue-deep:#3a0d0e;--bg-card:#1d1213;--bg-sidebar:#150c0d;--glow:rgba(158,36,36,.28)}
body.kind-player{--hue:#4f7d2c;--hue-light:#a8d05a;--hue-deep:#18270f;--bg-card:#151a11;--bg-sidebar:#0f140c;--glow:rgba(110,160,50,.22)}
body.kind-table{--hue:#6a3591;--hue-light:#bb97e2;--hue-deep:#28133b;--bg-card:#1a1322;--bg-sidebar:#130d1a;--glow:rgba(120,60,170,.28)}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;color:var(--text-primary);font-family:'EB Garamond',Georgia,serif;font-size:19px;line-height:1.7;
 background:radial-gradient(ellipse 90% 55% at 50% -12%,var(--glow),transparent 70%) fixed,radial-gradient(ellipse 60% 40% at 100% 110%,rgba(200,103,30,.10),transparent 70%) fixed,var(--bg-main)}
h1,h2,h3{font-weight:400}
::-webkit-scrollbar{width:8px}::-webkit-scrollbar-track{background:var(--bg-main)}::-webkit-scrollbar-thumb{background:var(--hue);border-radius:4px}
a{color:var(--hue-light)}
:focus-visible{outline:2px solid var(--gold-light);outline-offset:2px}
.sidebar{position:fixed;left:0;top:0;bottom:0;width:280px;background:var(--bg-sidebar);border-right:1px solid var(--rule);box-shadow:inset -4px 0 0 var(--bg-sidebar),inset -5px 0 0 var(--hue);z-index:40;display:flex;flex-direction:column;overflow-y:auto}
.side-head{padding:1.75rem 1.5rem 1.1rem;border-bottom:1px solid var(--rule)}
.side-eyebrow{font-family:'IM Fell English SC',Georgia,serif;font-size:.95rem;letter-spacing:.06em;color:var(--hue-light)}
.side-title{font-family:'UnifrakturMaguntia',serif;font-size:1.55rem;color:var(--gold-light);line-height:1.2;margin-top:2px}
.side-sub{font-size:.9rem;color:var(--text-dim);margin-top:.35rem;font-style:italic}
nav{padding:1rem 0;flex:1}
.nav-link{display:block;padding:.55rem 1.25rem;color:var(--text-secondary);text-decoration:none;font-family:'IM Fell English',Georgia,serif;font-size:16px;line-height:1.35;border-left:3px solid transparent}
.nav-link:hover{color:var(--gold-bright);background:rgba(168,131,47,.08)}
.nav-link.active{color:var(--gold-bright);border-left-color:var(--hue-light);background:linear-gradient(90deg,var(--hue-deep),transparent)}
.main{margin-left:280px;min-height:100vh}
.wrap{max-width:900px;margin:0 auto;padding:2.5rem 2rem 4rem}
/* cover */
.hero{text-align:center;padding:3rem 1rem 1.5rem}
.hero h1{font-family:'UnifrakturMaguntia',serif;font-size:2.7rem;line-height:1.2;color:var(--gold-bright);margin:.25rem 0 .5rem;text-shadow:0 0 28px var(--glow)}
.flourish{display:block;width:240px;max-width:70%;height:24px;margin:0 auto 1.5rem;color:var(--hue-light)}
.hero blockquote{margin:0 auto 1rem;max-width:36rem;border:0;background:none;color:var(--gold-light);font-family:'IM Fell English',Georgia,serif;font-style:italic;font-size:1.3rem;padding:0}
.lede{text-align:left;display:flow-root}
.hero .lede,.hero .intro{max-width:40rem;margin:0 auto;color:var(--text-secondary);font-size:1.05rem}
.hero p code{font-size:.85em}
/* the illuminated letter: once per document */
.lede::first-letter{float:left;font-family:'UnifrakturMaguntia',serif;font-style:normal;font-weight:400;font-size:4.1em;line-height:.82;color:var(--gold-bright);
 background:radial-gradient(circle at 30% 25%,var(--hue),var(--hue-deep) 75%);border:4px double var(--gold-light);padding:.16em .16em .1em;margin:.06em .16em 0 0;text-shadow:0 2px 0 rgba(0,0,0,.6)}
/* section cards: Victorian double rule, inner line in the document's color */
.section-card{position:relative;background:var(--bg-card);border:1px solid var(--rule);border-radius:3px;box-shadow:inset 0 0 0 5px var(--bg-card),inset 0 0 0 6px var(--hue),0 10px 30px rgba(0,0,0,.35);padding:2.25rem;margin-bottom:1rem;scroll-margin-top:1rem}
.section-card h2{font-family:'IM Fell English SC',Georgia,serif;color:var(--gold-light);margin-top:0;font-size:1.75rem;line-height:1.25;letter-spacing:.02em;border-bottom:1px solid var(--rule);padding-bottom:.55rem}
.section-card h2::before{content:'\\2767';color:var(--hue-light);margin-right:.45em;font-size:.85em}
.section-card h3{font-family:'IM Fell English',Georgia,serif;font-style:italic;color:var(--hue-light);font-size:1.3rem;margin:1.6rem 0 .4rem}
.section-card p,.section-card li{color:var(--text-primary)}
.section-card strong{color:var(--gold-bright);font-weight:600}
.section-card em{color:var(--text-secondary)}
code{font-family:inherit;color:var(--gold-light);background:rgba(168,131,47,.12);padding:0 .25em;border-radius:2px}
blockquote{border-left:3px solid var(--hue);background:linear-gradient(90deg,var(--hue-deep),rgba(0,0,0,.15));margin:1.25rem 0;padding:.9rem 1.4rem;border-radius:0 3px 3px 0}
blockquote p{margin:.3rem 0}
/* dividers: a vignette between rules */
.divider{display:flex;align-items:center;gap:1rem;color:var(--hue-light);padding:.5rem 0 1.5rem}
.divider::before,.divider::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,transparent,var(--gold) 50%,transparent)}
.divider svg{width:44px;height:44px;opacity:.85}
/* margin art, wide screens only */
.marg{display:none;position:absolute;top:1.75rem;width:96px;color:var(--hue-light);opacity:.5;pointer-events:none}
.marg svg{width:96px;height:96px}
.marg.l{left:-136px}.marg.r{right:-136px}
@media(min-width:1500px){.marg{display:block}}
table{width:100%;border-collapse:collapse;margin:1rem 0;font-size:.95rem}
th,td{border:1px solid var(--rule);padding:.5rem .7rem;text-align:left;vertical-align:top}
th{background:var(--hue-deep);color:var(--gold-light);font-family:'IM Fell English SC',Georgia,serif;font-weight:400;font-size:1rem}
tr:nth-child(even) td{background:rgba(0,0,0,.18)}
.table-scroll{overflow-x:auto}
/* session blocks keep the four-act colors: purple, pumpkin, brew green, blood */
.session-preview{border-radius:3px;padding:1.5rem 1.75rem;background:rgba(0,0,0,.22);margin:1.25rem 0;position:relative;overflow:hidden}
.session-preview::before{content:'';position:absolute;top:0;left:0;right:0;height:3px}
.session-preview h3{margin-top:.25rem;color:var(--gold-bright)}
.s1{border:1px solid rgba(122,62,170,.5)}.s1::before{background:linear-gradient(90deg,#5b2a7a,#a77ad0)}
.s2{border:1px solid rgba(200,103,30,.5)}.s2::before{background:linear-gradient(90deg,#8a3f0e,#e08a3a)}
.s3{border:1px solid rgba(95,143,58,.5)}.s3::before{background:linear-gradient(90deg,#2f5a1c,#93bf45)}
.s4{border:1px solid rgba(158,36,36,.55)}.s4::before{background:linear-gradient(90deg,#5a0d0d,#c8322a)}
hr{border:0;border-top:1px solid var(--rule);margin:1.5rem 0}
.footer{text-align:center;color:var(--text-dim);font-style:italic;padding:2rem 0}
.footer::before{content:'\\2766';display:block;color:var(--hue-light);font-style:normal;font-size:1.4rem;margin-bottom:.4rem}
.mobile-header{display:none}
/* notes tool */
.notes-tabs{display:flex;gap:.5rem;flex-wrap:wrap;margin:1rem 0}
.notes-tab{background:transparent;color:var(--text-secondary);border:1px solid var(--rule);border-radius:3px;padding:.35rem .9rem;font-family:'IM Fell English SC',Georgia,serif;font-size:1rem;cursor:pointer}
.notes-tab.active{background:var(--hue-deep);color:var(--gold-bright);border-color:var(--hue-light)}
.notes-pane{display:none}.notes-pane.active{display:block}
.notes-pane label{display:block;font-family:'IM Fell English SC',Georgia,serif;font-size:1rem;color:var(--hue-light);margin:1rem 0 .3rem}
.notes-pane textarea{width:100%;min-height:110px;background:rgba(0,0,0,.3);color:var(--text-primary);border:1px solid var(--rule);border-radius:3px;padding:.7rem;font-family:'EB Garamond',serif;font-size:17px;resize:vertical}
.notes-pane textarea:focus{outline:none;border-color:var(--hue-light)}
.btn{background:var(--hue);color:var(--text-primary);border:1px solid var(--gold);border-radius:3px;padding:.5rem 1.1rem;font-family:'IM Fell English SC',Georgia,serif;font-size:1rem;cursor:pointer}
.btn:hover{background:var(--hue-light);color:#120c0e}
.notes-status{color:var(--text-dim);font-size:.9rem;margin-left:.75rem;font-style:italic}
@media(max-width:900px){
 .sidebar{transform:translateX(-100%);transition:transform .25s}.sidebar.open{transform:none}
 .main{margin-left:0}.mobile-header{display:flex;align-items:center;position:sticky;top:0;z-index:30;background:var(--bg-sidebar);border-bottom:1px solid var(--hue);padding:.6rem 1rem}
 .mobile-header button{background:none;border:0;color:var(--gold-light);font-size:1.5rem;cursor:pointer;margin-right:.75rem}
 .mobile-header span{font-family:'UnifrakturMaguntia',serif;font-size:1.2rem;color:var(--gold-light)}
 .wrap{padding:1.5rem 1rem 3rem}.hero{padding:2rem .25rem 1rem}.hero h1{font-size:2rem}.section-card{padding:1.4rem 1.2rem}
 .section-card h2{font-size:1.45rem}.lede::first-letter{font-size:3.4em}
}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.sidebar{transition:none}}
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


SVG_OPEN = '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
ICONS = {
 # DM: the house's secrets
 "skull": '<path d="M32 9C20 9 13 17 13 27c0 6 2.5 10 6 12.5V47h26v-7.5c3.5-2.5 6-6.5 6-12.5C51 17 44 9 32 9z"/><circle cx="24.5" cy="28" r="4.5" fill="currentColor"/><circle cx="39.5" cy="28" r="4.5" fill="currentColor"/><path d="M32 34l-3 5h6z" fill="currentColor"/><path d="M25 47v-5M30 47v-5M34 47v-5M39 47v-5M16 55l32-0M20 51l-6 8M44 51l6 8"/>',
 "candle": '<path d="M32 22c-3.5-3-3.5-7.5 0-12.5 3.5 5 3.5 9.5 0 12.5z" fill="currentColor" fill-opacity=".35"/><path d="M32 22v4M27 52V26h10v26M27 30c0 4 2 5 2 8M37 28c0 3-1.5 4-1.5 6"/><path d="M18 56c0-3 6-4.5 14-4.5s14 1.5 14 4.5zM46 54c4 0 6-2 6-4"/>',
 "key": '<circle cx="19" cy="19" r="9"/><circle cx="19" cy="19" r="3.5"/><path d="M25.5 25.5L53 53M45 45l-5 5M49.5 49.5l-4 4M39 39l-3.5 3.5"/>',
 "dagger": '<path d="M54 10L32 36l-4-4z" fill="currentColor" fill-opacity=".2"/><path d="M54 10L32 36M54 10L28 32M24 28l12 12M30 34L18 46"/><circle cx="16" cy="48" r="3"/>',
 # Player: the witch's kitchen
 "cauldron": '<circle cx="26" cy="21" r="3"/><circle cx="35" cy="15" r="4"/><circle cx="30" cy="7" r="2"/><circle cx="42" cy="23" r="2"/><ellipse cx="32" cy="30" rx="19" ry="4"/><path d="M14 31c-1 12 6 19 18 19s19-7 18-19M20 47l-3 6M44 47l3 6M28 59c-2-3 0-5 2-7 0 3 2 3 2 7M34 59c-1-2 0-4 2-6 0 3 2 3 1 6"/>',
 "potion": '<path d="M27 6h10v5H27zM29 11v9c-9 3-15 10-15 19 0 10 8 17 18 17s18-7 18-17c0-9-6-16-15-19v-9"/><path d="M16 38c5 3 10-2 16 0s11 3 16 0"/><circle cx="27" cy="46" r="2"/><circle cx="36" cy="43" r="1.5"/><circle cx="33" cy="50" r="1"/>',
 "mushroom": '<path d="M10 32c0-12 10-20 22-20s22 8 22 20c-6 2-14 3-22 3s-16-1-22-3z"/><path d="M26 35c-1 7-2 13-3 19h18c-1-6-2-12-3-19M12 54h40"/><circle cx="22" cy="23" r="3"/><circle cx="35" cy="18" r="2.5"/><circle cx="43" cy="26" r="2.5"/>',
 "bat": '<path d="M32 26C30 26 29 27 29 28L27 24 28 30C22 24 13 24 6 29C10 30 12 33 12 36C15 34 18 34 20 37C22 34 25 34 27 36C28 39 30 41 32 42C34 41 36 39 37 36C39 34 42 34 44 37C46 34 49 34 52 36C52 33 54 30 58 29C51 24 42 24 36 30L37 24 35 28C35 27 34 26 32 26Z" fill="currentColor" fill-opacity=".25"/>',
 # Table: the stage and the seance
 "masks": '<path d="M10 14c8-3 16-3 22 0 0 14-4 24-11 24S10 28 10 14z"/><path d="M14 20q3-3 6 0M23 20q3-3 6 0M15 28q6 6 12 0"/><path d="M32 26c8-3 16-3 22 0 0 14-4 24-11 24S32 40 32 26z" fill="var(--bg-card)"/><path d="M36 33q3 3 6 0M45 33q3 3 6 0M37 44q6-6 12 0"/>',
 "crystal": '<circle cx="32" cy="27" r="16"/><path d="M24 19q4-5 10-5M21 42l-4 11h30l-4-11M13 55h38"/><path d="M36 28l1.5 3 3 .5-2.2 2 .6 3-2.9-1.5-2.9 1.5.6-3-2.2-2 3-.5z" fill="currentColor"/>',
 "moon": '<path d="M40 9a23 23 0 1 0 15 35A18 18 0 1 1 40 9z" fill="currentColor" fill-opacity=".15"/><path d="M14 12l1 3 3 1-3 1-1 3-1-3-3-1 3-1zM52 14l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8zM50 52l.6 1.6 1.6.6-1.6.6-.6 1.6-.6-1.6-1.6-.6 1.6-.6z" fill="currentColor"/>',
 "tarot": '<rect x="18" y="7" width="28" height="50" rx="2"/><rect x="21.5" y="10.5" width="21" height="43" rx="1"/><path d="M24 32q8-8 16 0q-8 8-16 0z"/><circle cx="32" cy="32" r="2.5" fill="currentColor"/><path d="M32 17v6M32 41v6M27 20l2 4M37 20l-2 4"/>',
}
ICON_SETS = {
 "dm": ["skull", "candle", "key", "dagger"],
 "player": ["cauldron", "potion", "bat", "mushroom"],
 "table": ["masks", "crystal", "tarot", "moon"],
}
FLOURISH = ('<svg class="flourish" viewBox="0 0 240 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true">'
            '<path d="M8 12h86M146 12h86M94 12c5-8 14-8 18 0-4 8-13 8-18 0zM146 12c-5-8-14-8-18 0 4 8 13 8 18 0z"/>'
            '<path d="M120 3l6 9-6 9-6-9z" fill="currentColor"/><circle cx="8" cy="12" r="2" fill="currentColor"/><circle cx="232" cy="12" r="2" fill="currentColor"/></svg>')


def icon(name):
    return SVG_OPEN + ICONS[name] + "</svg>"


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def md_to_html(text):
    out = markdown.markdown(text, extensions=["tables", "sane_lists", "attr_list"])
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

    # the illuminated letter goes on the document's opening prose paragraph if the
    # first section starts with one; otherwise on the cover's intro line
    lede_in_body = False
    if sections:
        first_body = sections[0].partition("\n")[2]
        blocks = [b.strip() for b in re.split(r"\n\s*\n", first_body) if b.strip()][:2]
        for i, b in enumerate(blocks):
            if len(b) >= 120 and "\n" not in b and not re.match(r"[-*|>#\d`]", b):
                name0 = sections[0].partition("\n")[0]
                rest = sections[0].partition("\n")[2].replace(b, b + "\n{: .lede}", 1)
                sections[0] = name0 + "\n" + rest
                lede_in_body = True
                break
            if not b.startswith("**"):
                break
    icon_set = ICON_SETS[kind]

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
        n = len(cards)
        side = "l" if n % 2 == 0 else "r"
        marg = f'<div class="marg {side}">{icon(icon_set[n % len(icon_set)])}</div>'
        cards.append(f'<section class="section-card" id="{sid}">{marg}<h2>{html.escape(name)}</h2>{inner}</section>')

    nav_html = "".join(f'<a class="nav-link" href="#{i}">{html.escape(n)}</a>' for i, n in nav)
    parts = [cards[0]] if cards else []
    for i, c in enumerate(cards[1:]):
        parts.append(f'\n<div class="divider">{icon(icon_set[(i + 1) % len(icon_set)])}</div>\n')
        parts.append(c)
    cards_html = "".join(parts)
    sub_html = markdown.markdown(subtitle).replace("<p>", "", 1).rsplit("</p>", 1)[0] if subtitle else ""
    lede_cls = "intro" if lede_in_body else "lede"
    quote_html = f"<blockquote>{html.escape(tagline)}</blockquote>" if tagline else ""

    page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(doc_title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;1,400&family=IM+Fell+English:ital@0;1&family=IM+Fell+English+SC&family=UnifrakturMaguntia&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body class="kind-{kind}">
<div class="mobile-header"><button id="menu-btn" type="button" aria-label="Menu">&#9776;</button><span>The Reveler's Stage</span></div>
<aside class="sidebar" id="sidebar">
 <div class="side-head"><div class="side-eyebrow">{html.escape(side_eyebrow)}</div><div class="side-title">{html.escape(side_title)}</div><div class="side-sub">{html.escape(side_sub)}</div></div>
 <nav>{nav_html}</nav>
</aside>
<div class="main"><div class="wrap">
 <header class="hero"><h1>{html.escape(title)}</h1>{FLOURISH}{quote_html}<p class="{lede_cls}">{sub_html}</p></header>
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
    ap.add_argument("--kind", default="player", choices=["player", "dm", "table"])
    ap.add_argument("--eyebrow", default="A Player's")
    ap.add_argument("--side-title", default="Companion")
    ap.add_argument("--side-sub", default="D&D 5e Campaign Guide")
    ap.add_argument("--doc-title", default="The Reveler's Stage - Player Guide")
    a = ap.parse_args()
    build(a.src, a.dst, a.kind, a.eyebrow, a.side_title, a.side_sub, a.doc_title)
