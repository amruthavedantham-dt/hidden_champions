import json, sys, html, re

CSS = """  :root{
    --field:#163a2b; --field-deep:#0f2c20; --leaf:#2f6b41; --sprout:#7fae6a;
    --paper:#f6f2e9; --grain:#e4ddcb; --soil:#8a5a2b; --ink:#20221c;
    --ink-soft:#54564b; --cream:#f3eedf;
  }
  *{box-sizing:border-box;}
  body{margin:0; background:#ece6d7; color:var(--ink); font-family:"Newsreader",Georgia,serif; font-size:18px; line-height:1.6; padding:32px 16px;}
  .paper{max-width:680px; margin:0 auto; background:var(--paper); border:1px solid var(--grain); box-shadow:0 24px 60px -32px rgba(15,44,32,.45);}
  .masthead{background:var(--field); color:var(--cream); padding:40px 40px 44px; position:relative; overflow:hidden;}
  .masthead::after{content:""; position:absolute; left:0;right:0;bottom:0; height:4px; background:linear-gradient(90deg,var(--sprout),var(--leaf) 60%,transparent);}
  .series{font-family:"Spline Sans Mono",monospace; font-size:12px; letter-spacing:.22em; text-transform:uppercase; color:var(--sprout); margin:0 0 22px;}
  .series span{color:rgba(243,238,223,.55);}
  .headline{font-family:"Fraunces",serif; font-weight:600; font-size:clamp(29px,5.6vw,42px); line-height:1.09; letter-spacing:-.01em; margin:0; text-wrap:balance;}
  .subhead{font-size:17px; line-height:1.5; color:rgba(243,238,223,.82); margin:18px 0 0; max-width:50ch;}
  .snapshot{display:grid; grid-template-columns:repeat(3,1fr); border-bottom:1px solid var(--grain);}
  .snap{padding:15px 22px; border-right:1px solid var(--grain); border-bottom:1px solid var(--grain);}
  .snap:nth-child(3n){border-right:none;} .snap:nth-last-child(-n+3){border-bottom:none;}
  .snap-label{font-family:"Spline Sans Mono",monospace; font-size:10px; letter-spacing:.16em; text-transform:uppercase; color:var(--ink-soft); margin:0 0 4px;}
  .snap-value{font-family:"Fraunces",serif; font-weight:500; font-size:15.5px; line-height:1.2; margin:0;}
  .body{padding:34px 40px 8px;}
  .part{margin:0 0 34px;}
  .pnum{font-family:"Spline Sans Mono",monospace; font-size:10.5px; letter-spacing:.18em; text-transform:uppercase; color:var(--ink-soft);}
  .eyebrow{font-family:"Fraunces",serif; font-weight:600; font-size:21px; color:var(--field); margin:3px 0 14px;}
  .insights{list-style:none; margin:0; padding:0;}
  .insight{padding:11px 0; border-bottom:1px dotted var(--grain);}
  .insight:last-child{border-bottom:none;}
  .insight .point{font-family:"Fraunces",serif; font-weight:500; font-size:18px; line-height:1.3; margin:0;}
  .insight .point b{font-weight:600; color:var(--field);}
  .insight .ev{font-size:13.5px; line-height:1.45; color:var(--ink-soft); margin:5px 0 0;}
  .fig{font-family:"Spline Sans Mono",monospace; font-size:12px; color:var(--soil); font-weight:600;}
  .reflect{font-family:"Fraunces",serif; font-style:italic; font-weight:500; font-size:17px; line-height:1.4; color:var(--field); margin:14px 0 0; padding-top:13px; border-top:1px solid var(--grain);}
  .src{font-family:"Spline Sans Mono",monospace; font-size:10px; color:var(--ink-soft); margin:12px 0 0; line-height:1.5;}

  .opp{background:#efe9da; border:1px solid var(--grain); border-left:3px solid var(--leaf); padding:15px 17px; margin:0 0 12px;}
  .opp .tag{font-family:"Spline Sans Mono",monospace; font-size:10px; letter-spacing:.08em; text-transform:uppercase; color:var(--leaf); margin:0 0 6px;}
  .opp h4{font-family:"Fraunces",serif; font-weight:600; font-size:17px; margin:0 0 5px;}
  .opp p{font-size:14.5px; line-height:1.5; margin:0; color:var(--ink-soft);}
  .opp p b{color:var(--ink);}
  .opp .glaser{font-family:"Fraunces",serif; font-style:italic; font-weight:500; font-size:15.5px; line-height:1.4; color:var(--leaf); margin:8px 0 0;}
  .opp .oppsrc{font-family:"Spline Sans Mono",monospace; font-size:9.5px; color:var(--ink-soft); margin:9px 0 0; letter-spacing:.02em; line-height:1.4;}
  .lede{font-size:16px; color:var(--ink-soft); margin:0 0 14px;}
  .prose{font-size:17px; line-height:1.62; margin:0 0 14px;}
  .prose:last-child{margin-bottom:0;}
  .prose b{font-weight:600; color:var(--field);}

  .reveal-btn{font-family:"Spline Sans Mono",monospace; font-size:12px; letter-spacing:.06em; text-transform:uppercase; color:var(--field); background:transparent; border:1px solid var(--leaf); border-radius:3px; padding:12px 18px; cursor:pointer; width:100%; text-align:left; display:flex; justify-content:space-between; align-items:center; transition:.15s;}
  .reveal-btn:hover{background:rgba(47,107,65,.07);}
  .reveal-btn .chev{transition:transform .2s;}
  .reveal-btn[aria-expanded="true"] .chev{transform:rotate(90deg);}
  .hidden-part{display:none; padding-top:18px;}
  .hidden-part.open{display:block;}
  .guesslabel{font-family:"Spline Sans Mono",monospace; font-size:11px; color:var(--soil); background:rgba(138,90,43,.08); border:1px solid rgba(138,90,43,.25); border-radius:3px; padding:8px 12px; margin:0 0 14px; line-height:1.45;}
  .hvt,.wf{border:1px solid var(--grain); border-radius:3px; padding:14px 16px; margin:0 0 10px;}
  .hvt .tag{font-family:"Spline Sans Mono",monospace; font-size:10px; letter-spacing:.08em; text-transform:uppercase; color:var(--soil); margin:0 0 5px;}
  .hvt h5,.wf h5{font-family:"Fraunces",serif; font-weight:600; font-size:16px; margin:0 0 6px;}
  .hvt p{font-size:14px; line-height:1.5; margin:0; color:var(--ink-soft);}
  .hintro{font-size:15px; color:var(--ink-soft); margin:0 0 14px;}
  .hrow{display:grid; grid-template-columns:60px 1fr; gap:14px; padding:14px 0; border-bottom:1px solid var(--grain);}
  .hrow:last-of-type{border-bottom:none;}
  .hlabel{font-family:"Fraunces",serif; font-weight:900; font-size:22px; color:var(--soil); line-height:1;}
  .hlabel span{display:block; font-family:"Spline Sans Mono",monospace; font-size:9px; letter-spacing:.06em; text-transform:uppercase; color:var(--ink-soft); font-weight:600; margin-top:5px;}
  .hopp{font-size:14px; line-height:1.5; margin:7px 0 0; color:var(--leaf);}
  .hopp .k{font-family:"Spline Sans Mono",monospace; font-size:9px; letter-spacing:.06em; text-transform:uppercase; color:var(--soil); margin-right:7px;}
  .genericflag{font-family:"Spline Sans Mono",monospace; font-size:9px; letter-spacing:.06em; text-transform:uppercase; color:var(--soil); background:rgba(138,90,43,.08); border:1px solid rgba(138,90,43,.2); border-radius:2px; padding:2px 6px; margin-left:6px;}
  .hsrc{font-family:"Spline Sans Mono",monospace; font-size:9.5px; color:var(--ink-soft); margin:12px 0 0; line-height:1.5;}
  .steps{font-size:14.5px; line-height:1.7; margin:0;}
  .steps b{color:var(--field); font-weight:600;}

  .takeaway{background:var(--field-deep); color:var(--cream); padding:32px 40px 30px;}
  .takeaway p{font-family:"Fraunces",serif; font-weight:500; font-size:clamp(19px,3.2vw,23px); line-height:1.34; margin:0 0 18px; text-wrap:balance;}
  .takeaway p .hi{color:var(--sprout);}
  .takeaway .cta{font-family:"Spline Sans Mono",monospace; font-size:12.5px; letter-spacing:.06em; text-transform:uppercase; color:var(--field-deep); background:var(--sprout); border:none; border-radius:3px; padding:13px 20px; cursor:pointer; font-weight:600;}
  .takeaway .cta-note{font-size:13px; color:rgba(243,238,223,.6); margin:12px 0 0;}
  .colophon{padding:18px 40px 24px; background:var(--field-deep); color:rgba(243,238,223,.5); font-family:"Spline Sans Mono",monospace; font-size:10.5px; letter-spacing:.04em; border-top:1px solid rgba(243,238,223,.12); line-height:1.6;}
  .colophon b{color:rgba(243,238,223,.8); font-weight:600;}
  @media (max-width:560px){
    body{padding:16px 0;} .paper{border:none;}
    .masthead{padding:30px 22px 34px;} .body{padding:26px 22px 4px;}
    .takeaway,.colophon{padding-left:22px;padding-right:22px;}
    .snapshot{grid-template-columns:1fr 1fr;}
    .snap:nth-child(3n){border-right:1px solid var(--grain);} .snap:nth-child(2n){border-right:none;}
  }
"""

def md_bold(s):
    if s is None: return ""
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return s

def render(j):
    m = j["meta"]
    mh = j["masthead"]
    title = f'Hidden Champions — {j["p1_engine"]["eyebrow"] if False else m["profileId"].replace("-", " ").title()}'
    snap_html = "".join(
        f'<div class="snap"><p class="snap-label">{html.escape(s["label"])}</p><p class="snap-value">{md_bold(s["value"])}</p></div>'
        for s in j["snapshot"]
    )
    p1_html = "".join(f'<p class="prose">{md_bold(b["text"])}</p>' for b in j["p1_engine"]["blocks"])
    ins_html = ""
    for ins in j["p2_market"]["insights"]:
        ev = f'<p class="ev">{md_bold(ins.get("evidence",""))}</p>' if ins.get("evidence") else ""
        ins_html += f'<li class="insight"><p class="point">{md_bold(ins["point"])}</p>{ev}</li>'
    opp_html = ""
    for o in j["p3_opportunities"]["items"]:
        opp_html += (f'<div class="opp"><p class="tag">{html.escape(o["lever"].title())}</p>'
                     f'<h4>{html.escape(o["title"])}</h4><p>{md_bold(o["body"])}</p>'
                     f'<p class="oppsrc">{html.escape(o.get("source",""))}</p></div>')
    exp_html = ""
    for e in j["p4_experiments"]["items"]:
        exp_html += (f'<div class="hvt"><p class="tag">{html.escape(e["lever"].title())}</p>'
                     f'<h5>{html.escape(e["title"])}</h5><p>{md_bold(e["body"])}</p></div>')
    hrows = ""
    for h in j["p5_workflows"]["horizontals"]:
        steps = " → ".join(html.escape(s) for s in h["steps"])
        spotted = h.get("spotted")
        hopp = ""
        if spotted:
            hopp = f'<p class="hopp"><span class="k">Spotted at &quot;{html.escape(h.get("spottedAt") or "")}&quot;</span> {md_bold(spotted["text"].split("→")[-1].strip() if "→" in spotted.get("text","") else spotted.get("text",""))}</p>'
        genflag = '<span class="genericflag">generic scaffold</span>' if h.get("flags",{}).get("generic") else ""
        hrows += (f'<div class="hrow"><div class="hlabel">{h["hId"]}<span>{html.escape(h["hName"])}</span></div>'
                  f'<div><p class="steps">{steps}{genflag}</p>{hopp}</div></div>')

    takeaway = md_bold(j["takeaway"]["text"])
    colophon_text = html.escape(j["colophon"]["text"])
    subhead = md_bold(mh["subhead"]["text"])
    headline = md_bold(mh["headline"]["text"])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,900&family=Newsreader:opsz,wght@6..72,400;6..72,500&family=Spline+Sans+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
{CSS}
</style>
</head>
<body>
<article class="paper">

  <header class="masthead">
    <p class="series">Hidden Champions of India <span>/ a DeepThought series</span></p>
    <h1 class="headline">{headline}</h1>
    <p class="subhead">{subhead}</p>
  </header>

  <section class="snapshot" aria-label="Snapshot">
    {snap_html}
  </section>

  <div class="body">

    <section class="part">
      <p class="pnum">Part 1</p>
      <h2 class="eyebrow">{html.escape(j["p1_engine"]["eyebrow"])}</h2>
      {p1_html}
    </section>

    <section class="part">
      <p class="pnum">Part 2</p>
      <h2 class="eyebrow">{html.escape(j["p2_market"]["eyebrow"])}</h2>
      <ul class="insights">
        {ins_html}
      </ul>
      <p class="reflect">{md_bold(j["p2_market"]["reflect"]["text"])}</p>
      <p class="src">{html.escape(j["p2_market"].get("sourceNote",""))}</p>
    </section>

    <section class="part">
      <p class="pnum">Part 3</p>
      <h2 class="eyebrow">{html.escape(j["p3_opportunities"]["eyebrow"])}</h2>
      <p class="lede">{html.escape(j["p3_opportunities"].get("lede",""))}</p>
      {opp_html}
    </section>

    <section class="part">
      <button class="reveal-btn" aria-expanded="false" onclick="toggle('p4',this)"><span>Part 4 · {html.escape(j["p4_experiments"]["eyebrow"])}</span><span class="chev">▸</span></button>
      <div class="hidden-part" id="p4">
        <p class="guesslabel">{html.escape(j["p4_experiments"]["guesslabel"]["text"])}</p>
        {exp_html}
      </div>
    </section>

    <section class="part">
      <button class="reveal-btn" aria-expanded="false" onclick="toggle('p5',this)"><span>Part 5 · {html.escape(j["p5_workflows"]["eyebrow"])}</span><span class="chev">▸</span></button>
      <div class="hidden-part" id="p5">
        <p class="hintro">{html.escape(j["p5_workflows"]["intro"]["text"])}</p>
        {hrows}
        <p class="hsrc">{html.escape(j["p5_workflows"].get("sourceNote",""))}</p>
      </div>
    </section>

  </div>

  <footer class="takeaway">
    <p>{takeaway}</p>
    <button class="cta" onclick="document.getElementById('p4').classList.add('open');document.querySelector('[onclick*=p4]').setAttribute('aria-expanded','true');document.getElementById('p4').scrollIntoView({{behavior:'smooth'}});">{html.escape(j["cta"]["label"])}</button>
    <p class="cta-note">{html.escape(j["cta"]["note"])}</p>
  </footer>

  <div class="colophon">
    <b>Hidden Champions of India</b> — a DeepThought series on how India's quiet world-beaters create wealth.<br>
    {colophon_text}
  </div>

</article>
<script>
  function toggle(id, btn){{
    var el = document.getElementById(id);
    var open = el.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  }}
</script>
</body>
</html>
"""

if __name__ == "__main__":
    src = sys.argv[1]
    dst = sys.argv[2]
    with open(src, encoding="utf-8") as f:
        j = json.load(f)
    out = render(j)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(out)
    print("wrote", dst)
