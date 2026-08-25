#!/usr/bin/env python3
"""Builds the four session decks as self-contained HTML. Run: python3 build.py"""
import html as H, os

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0d1117;--fg:#e6edf3;--dim:#8b949e;--acc:#f0b429;--good:#3fb950;--bad:#f85149;--line:#30363d;--card:#161b22}
html,body{height:100%}
body{background:var(--bg);color:var(--fg);font:400 16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,sans-serif;overflow:hidden}
.deck{height:100vh;display:flex;align-items:center;justify-content:center;padding:4vh 5vw}
.s{display:none;width:100%;max-width:1100px;animation:in .25s ease}
.s.on{display:block}
@keyframes in{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
h1{font-size:clamp(38px,6.5vw,84px);line-height:1.05;letter-spacing:-.03em;font-weight:800}
h2{font-size:clamp(28px,4.2vw,56px);line-height:1.1;letter-spacing:-.02em;font-weight:750;margin-bottom:.6em}
p,li{font-size:clamp(18px,2.1vw,30px);line-height:1.45}
ul{list-style:none}
li{margin:.5em 0;padding-left:1.4em;position:relative}
li:before{content:"";position:absolute;left:0;top:.62em;width:.5em;height:.5em;background:var(--acc);border-radius:50%}
.badge{display:inline-block;font-size:clamp(11px,1.2vw,15px);font-weight:800;letter-spacing:.16em;
  padding:.45em 1em;border-radius:99px;margin-bottom:1.1em;text-transform:uppercase}
.b-watch{background:#7c3aed;color:#fff}.b-look{background:#0969da;color:#fff}
.b-board{background:var(--acc);color:#0d1117}.b-ask{background:#db6d28;color:#fff}
.b-drill{background:var(--good);color:#0d1117}.b-slide{background:var(--line);color:var(--dim)}
.punch{font-size:clamp(30px,5vw,68px);line-height:1.15;font-weight:800;letter-spacing:-.02em}
.punch em{color:var(--acc);font-style:normal}
table{width:100%;border-collapse:collapse;margin:.5em 0;font-size:clamp(15px,1.9vw,26px)}
th,td{padding:.5em .7em;text-align:left;border-bottom:1px solid var(--line)}
th{color:var(--dim);font-size:.82em;text-transform:uppercase;letter-spacing:.08em;font-weight:700}
td.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
tr.tot td{border-top:2px solid var(--fg);border-bottom:none;font-weight:800;font-size:1.12em;padding-top:.5em}
.neg{color:var(--bad)}.pos{color:var(--good)}.acc{color:var(--acc)}.dim{color:var(--dim)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:2.2em}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:1.1em 1.3em}
.card h3{font-size:clamp(17px,2vw,27px);margin-bottom:.4em}
a{color:var(--acc)}
.res{font-size:clamp(15px,1.7vw,22px);background:var(--card);border:1px solid var(--line);
  border-left:4px solid var(--acc);border-radius:8px;padding:.8em 1em;margin-top:1em;word-break:break-all}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
.bar{background:var(--card);border-radius:6px;height:clamp(30px,4.5vw,58px);position:relative;display:flex;align-items:center;
  padding:0 .8em;font-weight:800;font-size:clamp(15px,2vw,28px);color:#0d1117}
#hud{position:fixed;bottom:14px;right:20px;color:var(--dim);font-size:13px;font-variant-numeric:tabular-nums;z-index:9}
#ttl{position:fixed;bottom:14px;left:20px;color:var(--dim);font-size:13px;z-index:9}
#notes{position:fixed;left:0;right:0;bottom:0;max-height:42vh;overflow:auto;background:#161b22;
  border-top:2px solid var(--acc);padding:1.1em 1.6em 2.4em;display:none;z-index:8;font-size:17px;line-height:1.55}
#notes.on{display:block}
#notes b{color:var(--acc);display:block;margin-bottom:.35em;font-size:12px;letter-spacing:.14em;text-transform:uppercase}
@media print{body{overflow:visible;background:#fff;color:#000}.deck{display:block;height:auto;padding:0}
  .s{display:block!important;page-break-after:always;padding:6vh 5vw;min-height:96vh}#hud,#ttl,#notes{display:none}}
"""

JS = """
const S=[...document.querySelectorAll('.s')];let i=0;
const N=document.getElementById('notes'),NB=document.getElementById('nb'),HUD=document.getElementById('hud');
function go(n){i=Math.max(0,Math.min(S.length-1,n));S.forEach((s,k)=>s.classList.toggle('on',k===i));
 HUD.textContent=(i+1)+' / '+S.length;NB.innerHTML=S[i].dataset.notes||'<i class=dim>no notes</i>';
 location.hash=i+1;}
addEventListener('keydown',e=>{
 if(['ArrowRight','ArrowDown',' ','PageDown'].includes(e.key)){e.preventDefault();go(i+1)}
 else if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();go(i-1)}
 else if(e.key==='Home')go(0); else if(e.key==='End')go(S.length-1);
 else if(e.key.toLowerCase()==='s'||e.key.toLowerCase()==='n')N.classList.toggle('on');});
addEventListener('click',e=>{if(e.target.tagName!=='A')go(i+1)});
go(parseInt(location.hash.slice(1)||'1')-1);
"""

def badge(k):
    m={'watch':'▶ watch together','look':'◉ open it live','board':'✎ whiteboard',
       'ask':'? ask the room','drill':'▲ they do it','slide':''}
    return f'<span class="badge b-{k}">{m[k]}</span>' if m.get(k) else ''

def build(fn, title, subtitle, slides):
    out=[]
    for s in slides:
        k=s.get('k','slide')
        notes=H.escape(s.get('n','')).replace('\n','<br>')
        body=badge(k)+s['h']
        out.append(f'<section class="s" data-notes="{notes}">{body}</section>')
    doc=f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{H.escape(title)}</title>
<style>{CSS}</style></head><body>
<div class="deck">{''.join(out)}</div>
<div id="ttl">{H.escape(subtitle)} &nbsp;·&nbsp; <span class="dim">S = notes &nbsp; ← → = move</span></div>
<div id="hud"></div><div id="notes"><b>say</b><div id="nb"></div></div>
<script>{JS}</script></body></html>"""
    open(fn,'w').write(doc)
    print(f'  {fn}  ({len(slides)} slides)')

# ─────────────────────────── ILLUSTRATIONS ───────────────────────────
A,G,R,D,L,C,W = '#f0b429','#3fb950','#f85149','#8b949e','#30363d','#161b22','#e6edf3'
def _s(vb,body,h='auto'):
    return f'<svg viewBox="{vb}" style="width:100%;height:{h};display:block;margin:.6em 0" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Inter,sans-serif">{body}</svg>'

def svg_layers():
    """Price built up in layers: each layer adds a slice."""
    segs=[("Factory",0,30,A),("Brand",30,60,"#c98a1f"),("Distributor",60,75,"#8f6416"),("Retail shop",75,100,"#5c4110")]
    b=''
    for name,a,z,col in segs:
        x,w=a*8,(z-a)*8
        b+=f'<rect x="{x}" y="40" width="{w}" height="70" fill="{col}" stroke="#0d1117" stroke-width="2"/>'
        b+=f'<text x="{x+w/2}" y="82" fill="#0d1117" font-size="17" font-weight="800" text-anchor="middle">+${z-a}</text>'
        b+=f'<text x="{x+w/2}" y="132" fill="{D}" font-size="15" text-anchor="middle">{name}</text>'
    b+=f'<text x="0" y="26" fill="{D}" font-size="15">$0</text>'
    b+=f'<text x="800" y="26" fill="{W}" font-size="22" font-weight="800" text-anchor="end">$100 to you</text>'
    b+=f'<line x1="240" y1="34" x2="240" y2="116" stroke="{W}" stroke-width="2" stroke-dasharray="5 4"/>'
    b+=f'<text x="248" y="26" fill="{A}" font-size="15" font-weight="700">cost to make</text>'
    return _s("0 0 800 145",b)

def svg_eaten():
    """The $60 bar, and the costs that exceed it."""
    P=11.5
    b=f'<text x="0" y="20" fill="{D}" font-size="15">WHAT SHE PAYS</text>'
    b+=f'<rect x="0" y="30" width="{60*P}" height="44" rx="4" fill="{C}" stroke="{G}" stroke-width="2"/>'
    b+=f'<text x="{30*P}" y="59" fill="{G}" font-size="21" font-weight="800" text-anchor="middle">$60.00</text>'
    b+=f'<text x="0" y="110" fill="{D}" font-size="15">WHAT IT COSTS HER SHOP</text>'
    costs=[("discount",9,"#8f6416"),("the shirt",30,"#5a5f66"),("ship",6,"#484d54"),("fee",1.78,"#3a3f45"),("ads",15,R)]
    x=0
    for n,v,col in costs:
        w=v*P
        b+=f'<rect x="{x}" y="120" width="{w}" height="44" rx="4" fill="{col}" stroke="#0d1117" stroke-width="2"/>'
        if v>4: b+=f'<text x="{x+w/2}" y="148" fill="#0d1117" font-size="15" font-weight="800" text-anchor="middle">{n}</text>'
        x+=w
    b+=f'<line x1="{60*P}" y1="24" x2="{60*P}" y2="176" stroke="{W}" stroke-width="2" stroke-dasharray="5 4"/>'
    b+=f'<rect x="{60*P}" y="120" width="{x-60*P}" height="44" rx="4" fill="none" stroke="{R}" stroke-width="3"/>'
    b+=f'<text x="{x+10}" y="150" fill="{R}" font-size="21" font-weight="800">−$1.78</text>'
    return _s("0 0 800 182",b)

def svg_two_orders(l1,v1,l2,v2,neg1=True):
    z=280
    w1=abs(v1)/22*440; w2=abs(v2)/22*440
    b=f'<line x1="{z}" y1="10" x2="{z}" y2="150" stroke="{L}" stroke-width="2"/>'
    b+=f'<text x="{z-w1-12}" y="45" fill="{D}" font-size="15" text-anchor="end">ORDER 1</text>' if neg1 else ''
    if neg1:
        b+=f'<rect x="{z-w1}" y="24" width="{w1}" height="46" rx="4" fill="{R}"/>'
        b+=f'<text x="{z-w1/2}" y="54" fill="#0d1117" font-size="19" font-weight="800" text-anchor="middle">{l1}</text>'
    else:
        b+=f'<rect x="{z}" y="24" width="{w1}" height="46" rx="4" fill="{A}"/>'
        b+=f'<text x="{z+w1/2}" y="54" fill="#0d1117" font-size="19" font-weight="800" text-anchor="middle">{l1}</text>'
        b+=f'<text x="{z-12}" y="54" fill="{D}" font-size="15" text-anchor="end">ORDER 1</text>'
    b+=f'<rect x="{z}" y="88" width="{w2}" height="46" rx="4" fill="{G}"/>'
    b+=f'<text x="{z+w2/2}" y="118" fill="#0d1117" font-size="19" font-weight="800" text-anchor="middle">{l2}</text>'
    b+=f'<text x="{z-12}" y="118" fill="{D}" font-size="15" text-anchor="end">ORDER 2</text>'
    return _s("0 0 800 155",b)

def svg_dtc():
    b=''
    for i,(t,on) in enumerate([("factory",1),("brand",1),("distributor",0),("shop",0),("you",1)]):
        x=i*160
        col=A if on else C; tc="#0d1117" if on else D
        b+=f'<rect x="{x}" y="30" width="132" height="56" rx="8" fill="{col}" stroke="{L if not on else col}" stroke-width="2"/>'
        b+=f'<text x="{x+66}" y="64" fill="{tc}" font-size="17" font-weight="700" text-anchor="middle">{t}</text>'
        if not on:
            b+=f'<line x1="{x+14}" y1="80" x2="{x+118}" y2="36" stroke="{R}" stroke-width="4"/>'
        if i<4: b+=f'<text x="{x+142}" y="64" fill="{D}" font-size="20" text-anchor="middle">→</text>'
    b+=f'<path d="M330 108 L330 128 L560 128" stroke="{R}" stroke-width="3" fill="none"/>'
    b+=f'<text x="345" y="152" fill="{R}" font-size="18" font-weight="800">you buy an ad instead — every single customer</text>'
    return _s("0 0 800 165",b)

def svg_funnel():
    stops=[("1 ad",100),("2 land",78),("3 popup",70),("4 product",52),("5 offer",44),("6 cart",34),("7 leave",20),("8 checkout",15),("9 paid",11)]
    b=''; x=0
    for i,(t,pct) in enumerate(stops):
        w=84; h=pct*1.5
        y=120-h/2
        col=A if i in(0,8) else (R if i==6 else "#2f4f6f")
        b+=f'<rect x="{x}" y="{y}" width="{w-10}" height="{h}" rx="4" fill="{col}" opacity="{0.55+i*0.05}"/>'
        b+=f'<text x="{x+37}" y="212" fill="{D}" font-size="13" text-anchor="middle">{t}</text>'
        x+=w
    b+=f'<text x="0" y="20" fill="{A}" font-size="16" font-weight="700">everyone who saw the ad</text>'
    b+=f'<text x="756" y="20" fill="{G}" font-size="16" font-weight="700" text-anchor="end">paid</text>'
    b+=f'<text x="530" y="238" fill="{R}" font-size="15" font-weight="700" text-anchor="middle">~70% of carts end here</text>'
    return _s("0 0 800 248",b)

def svg_shop_online():
    b=f'<rect x="0" y="0" width="380" height="200" rx="12" fill="{C}" stroke="{L}" stroke-width="2"/>'
    b+=f'<text x="24" y="36" fill="{D}" font-size="17" font-weight="700">A SHOP</text>'
    b+=f'<circle cx="90" cy="105" r="24" fill="none" stroke="{D}" stroke-width="3" stroke-dasharray="6 5"/>'
    b+=f'<path d="M130 105 L250 105" stroke="{D}" stroke-width="3" stroke-dasharray="8 6"/><path d="M240 96 l12 9 -12 9" fill="none" stroke="{D}" stroke-width="3"/>'
    b+=f'<text x="268" y="100" fill="{R}" font-size="20" font-weight="800">gone</text>'
    b+=f'<text x="268" y="124" fill="{D}" font-size="14">no name. no record.</text>'
    b+=f'<rect x="420" y="0" width="380" height="200" rx="12" fill="{C}" stroke="{A}" stroke-width="2"/>'
    b+=f'<text x="444" y="36" fill="{A}" font-size="17" font-weight="700">ONLINE</text>'
    b+=f'<circle cx="510" cy="105" r="24" fill="none" stroke="{W}" stroke-width="3"/>'
    b+=f'<path d="M550 105 L668 105" stroke="{W}" stroke-width="3"/><path d="M658 96 l12 9 -12 9" fill="none" stroke="{W}" stroke-width="3"/>'
    b+=f'<text x="686" y="100" fill="{D}" font-size="18">left</text>'
    b+=f'<rect x="486" y="146" width="150" height="34" rx="17" fill="{A}"/>'
    b+=f'<text x="561" y="169" fill="#0d1117" font-size="15" font-weight="800" text-anchor="middle">@ on a list</text>'
    return _s("0 0 800 205",b)

def svg_timeline():
    pts=[(0,"order","",A),(1,"ships","",D),(2,"arrives","",D),(3,"how to use it","wk 1",D),
         (5,"review","wk 2",D),(9,"running low?","wk 6",A),(12,"REORDERS","wk 8",G)]
    b=f'<line x1="30" y1="80" x2="770" y2="80" stroke="{L}" stroke-width="3"/>'
    for t,lab,sub,col in pts:
        x=30+t*61.6
        big = col in (A,G)
        b+=f'<circle cx="{x}" cy="80" r="{11 if big else 7}" fill="{col}"/>'
        b+=f'<text x="{x}" y="{52 if big else 58}" fill="{col}" font-size="{16 if big else 13}" font-weight="{800 if big else 500}" text-anchor="middle">{lab}</text>'
        if sub: b+=f'<text x="{x}" y="108" fill="{D}" font-size="13" text-anchor="middle">{sub}</text>'
    b+=f'<rect x="520" y="24" width="250" height="76" rx="8" fill="none" stroke="{A}" stroke-width="2" stroke-dasharray="6 5"/>'
    b+=f'<text x="645" y="134" fill="{A}" font-size="15" font-weight="700" text-anchor="middle">worth more than the ad</text>'
    return _s("0 0 800 145",b)

def svg_dots():
    b=f'<text x="0" y="20" fill="{D}" font-size="15">SHOP A — 100 customers, 100% loyal</text>'
    for i in range(100):
        b+=f'<rect x="{(i%20)*9}" y="{34+(i//20)*9}" width="6" height="6" fill="{A}"/>'
    b+=f'<text x="0" y="106" fill="{R}" font-size="18" font-weight="800">≈100 extra orders — still dead</text>'
    b+=f'<text x="330" y="20" fill="{D}" font-size="15">SHOP B — 20,000 customers, 5% loyal</text>'
    for i in range(1000):
        col = A if i%20==0 else "#252b33"
        b+=f'<rect x="{330+(i%50)*9}" y="{34+(i//50)*3.4}" width="6" height="2.4" fill="{col}"/>'
    b+=f'<text x="330" y="106" fill="{G}" font-size="18" font-weight="800">≈3,000–4,000 extra orders — real money</text>'
    return _s("0 0 800 118",b)

def svg_grow_vs_keep():
    b=f'<circle cx="180" cy="105" r="62" fill="none" stroke="{W}" stroke-width="3"/>'
    b+=f'<text x="180" y="112" fill="{W}" font-size="16" font-weight="700" text-anchor="middle">the base</text>'
    for a in (-40,0,40):
        import math
        r=math.radians(a); x1,y1=180+130*math.cos(r),105+130*math.sin(r); x2,y2=180+72*math.cos(r),105+72*math.sin(r)
        b+=f'<path d="M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}" stroke="{G}" stroke-width="3"/>'
        b+=f'<path d="M{x2+13:.0f} {y2-8:.0f} L{x2:.0f} {y2:.0f} L{x2+13:.0f} {y2+8:.0f}" fill="none" stroke="{G}" stroke-width="3"/>'
    b+=f'<text x="180" y="205" fill="{G}" font-size="19" font-weight="800" text-anchor="middle">REFERRAL grows it</text>'
    b+=f'<circle cx="600" cy="105" r="62" fill="none" stroke="{W}" stroke-width="3"/>'
    b+=f'<text x="600" y="112" fill="{W}" font-size="16" font-weight="700" text-anchor="middle">the base</text>'
    b+=f'<path d="M600 40 A62 62 0 1 1 538 105" fill="none" stroke="{A}" stroke-width="4"/>'
    b+=f'<path d="M528 92 L538 105 L551 98" fill="none" stroke="{A}" stroke-width="4"/>'
    b+=f'<path d="M672 105 L740 105" stroke="{A}" stroke-width="3"/><path d="M730 96 l12 9 -12 9" fill="none" stroke="{A}" stroke-width="3"/>'
    b+=f'<text x="600" y="205" fill="{A}" font-size="19" font-weight="800" text-anchor="middle">LOYALTY monetises it</text>'
    return _s("0 0 800 218",b)

def svg_once_again():
    b=f'<text x="0" y="20" fill="{D}" font-size="15">BOUGHT ONCE — mattress, cookware, luggage</text>'
    b+=f'<line x1="10" y1="52" x2="780" y2="52" stroke="{L}" stroke-width="2"/>'
    b+=f'<circle cx="30" cy="52" r="12" fill="{A}"/><text x="56" y="58" fill="{D}" font-size="14">then nothing for years</text>'
    b+=f'<text x="0" y="106" fill="{D}" font-size="15">BOUGHT AGAIN — soap, shampoo, razors, skincare</text>'
    b+=f'<line x1="10" y1="138" x2="780" y2="138" stroke="{L}" stroke-width="2"/>'
    for i in range(7):
        x=30+i*118
        b+=f'<circle cx="{x}" cy="138" r="{12 if i==0 else 10}" fill="{A if i==0 else G}"/>'
    b+=f'<text x="640" y="168" fill="{G}" font-size="15" font-weight="700" text-anchor="middle">this is where we live</text>'
    return _s("0 0 800 178",b)

def svg_ceiling():
    b=''
    for i,(lab,val,w,col) in enumerate([("1 order",13.22,150,D),("3 orders",57,470,A)]):
        y=30+i*80
        b+=f'<rect x="150" y="{y}" width="{w}" height="48" rx="4" fill="{col}" opacity=".85"/>'
        b+=f'<text x="140" y="{y+31}" fill="{D}" font-size="16" text-anchor="end">{lab}</text>'
        b+=f'<text x="{160+w}" y="{y+31}" fill="{col}" font-size="20" font-weight="800">${val}</text>'
    b+=f'<text x="150" y="196" fill="{W}" font-size="17" font-weight="700">how long she stays = what you may pay to get her</text>'
    return _s("0 0 800 208",b)

def svg_confession():
    rows=[("Klaviyo","cannot reach my visitors"),("Rebuy","my orders are too thin"),
          ("Recharge","customers buy once"),("Gorgias","drowning in where-is-my-order"),
          ("Loyalty app","have a base, nothing brings them back")]
    b=''
    for i,(app,fear) in enumerate(rows):
        y=i*44
        b+=f'<rect x="0" y="{y}" width="200" height="34" rx="6" fill="{C}" stroke="{A}" stroke-width="2"/>'
        b+=f'<text x="100" y="{y+23}" fill="{A}" font-size="16" font-weight="700" text-anchor="middle">{app}</text>'
        b+=f'<path d="M212 {y+17} L258 {y+17}" stroke="{D}" stroke-width="2"/><path d="M250 {y+11} l9 6 -9 6" fill="none" stroke="{D}" stroke-width="2"/>'
        b+=f'<text x="272" y="{y+23}" fill="{W}" font-size="17">&#8220;{fear}&#8221;</text>'
    b+=f'<text x="0" y="{len(rows)*44+26}" fill="{D}" font-size="15">what they bought &#8594; what they were afraid of</text>'
    return _s(f"0 0 800 {len(rows)*44+38}",b)

def svg_points_credit():
    b=f'<rect x="0" y="0" width="380" height="196" rx="12" fill="{C}" stroke="{A}" stroke-width="2"/>'
    b+=f'<text x="24" y="38" fill="{A}" font-size="20" font-weight="800">POINTS</text>'
    b+=f'<text x="24" y="66" fill="{W}" font-size="16">the brand&#8217;s currency</text>'
    for i,t in enumerate(["abstract — needs explaining","feels like belonging, progress","you name it, you theme it","some never redeemed"]):
        b+=f'<text x="24" y="{98+i*24}" fill="{D}" font-size="14">&#183; {t}</text>'
    b+=f'<rect x="420" y="0" width="380" height="196" rx="12" fill="{C}" stroke="{G}" stroke-width="2"/>'
    b+=f'<text x="444" y="38" fill="{G}" font-size="20" font-weight="800">STORE CREDIT</text>'
    b+=f'<text x="444" y="66" fill="{W}" font-size="16">money with your logo on it</text>'
    for i,t in enumerate(["understood instantly","feels like a transaction","looks like money, not like you","spent fast — you hold their cash"]):
        b+=f'<text x="444" y="{98+i*24}" fill="{D}" font-size="14">&#183; {t}</text>'
    return _s("0 0 800 205",b)

def svg_boxes():
    bx=[("GET PEOPLE IN","ads, email, they remember you"),("ON THE SITE","home, product, cart, popup"),
        ("PAY","checkout, discount, shipping"),("AFTER THE ORDER","email, where is my order, refund"),
        ("COME BACK","refill, drop, membership"),("MONEY","order 1 cost them. order 2 is the win")]
    b=''
    for i,(t,sub) in enumerate(bx):
        x=(i%3)*270; y=(i//3)*104
        hot = t in ("COME BACK","MONEY")
        b+=f'<rect x="{x}" y="{y}" width="250" height="86" rx="10" fill="{C}" stroke="{A if hot else L}" stroke-width="2"/>'
        b+=f'<text x="{x+18}" y="{y+34}" fill="{A if hot else W}" font-size="16" font-weight="800">{t}</text>'
        b+=f'<text x="{x+18}" y="{y+60}" fill="{D}" font-size="13">{sub}</text>'
    return _s("0 0 800 200",b)

def svg_stage():
    rows=[("no real base yet","expand the base &#8212; REFERRAL",G),
          ("base, but they buy once","a reason to return &#8212; POINTS",A),
          ("base, discounting everyone","stop the blanket discount &#8212; TIERS",A)]
    b=''
    for i,(l,r,col) in enumerate(rows):
        y=i*62
        b+=f'<rect x="0" y="{y}" width="330" height="48" rx="8" fill="{C}" stroke="{L}" stroke-width="2"/>'
        b+=f'<text x="18" y="{y+30}" fill="{W}" font-size="16">{l}</text>'
        b+=f'<path d="M344 {y+24} L392 {y+24}" stroke="{col}" stroke-width="3"/><path d="M383 {y+17} l10 7 -10 7" fill="none" stroke="{col}" stroke-width="3"/>'
        b+=f'<text x="406" y="{y+30}" fill="{col}" font-size="17" font-weight="700">{r}</text>'
    return _s("0 0 800 190",b)

# ═══════════════ SESSION 1 — THE BASICS: how a shop makes money ═══════════════
S1=[
{'h':'<h1>How a shop<br>makes money</h1><p class="dim" style="margin-top:1em">Session 1 · the basics · no website, no app, no Joy</p>'
 ,'n':'Goal: you understand a shop as a business, not as a website. Everything else this month sits on top of tonight.'},

{'k':'ask','h':'<h2>You can buy this shirt for <span class="acc">$30</span>.</h2><p class="punch">What do you sell it for?</p>'
 ,'n':'Shout it out. Write every answer up, judge none. Someone will say sixty.'},

{'h':'<h2>Same shirt. Three prices.</h2><div class="two">'
 '<div class="card"><h3 class="dim">Retail shop</h3><p class="punch">$100</p></div>'
 '<div class="card"><h3 class="dim">Outlet, next season</h3><p class="punch">$60</p></div></div>'
 '<p style="margin-top:1.2em">Why? It is not brand. It is not quality.</p>'
 ,'n':'Let them guess. They will say brand and quality. Both mostly wrong. It is distribution.'},

{'h':'<h2>Price is layers</h2>'+svg_layers()+
 '<p style="margin-top:.4em">Every layer is somebody who <b class="acc">has to eat</b>.</p>'
 ,'n':'Price is not the cost of the thing. The shop is not greedy — the shop has rent, staff and a shelf. Point at the gap between thirty and a hundred: none of that is shirt.'},

{'h':'<p class="punch">The further a product travels from the factory, the <em>more mouths</em> it has to feed.</p>'
 '<p class="punch" style="margin-top:1em">A discount does not eat the profit. It eats <em>the layer that was paying for everything else.</em></p>'
 ,'n':'Remember the second one. Every time a merchant flinches at a discount, this is why.'},

{'h':'<h2>So DTC deletes the layers</h2>'+svg_dtc()
 ,'n':'Sell straight to the person, keep the layers. That is why DTC can charge less and keep more. But nothing is free — they deleted the shop and bought an ad instead, and unlike a shop you pay the ad again for every single customer.'},

{'k':'watch','h':'<h2>The clearest example ever filmed</h2><p><b>Dollar Shave Club</b>, March 2012. 90 seconds.</p>'
 '<ul><li>Shot in one day for <b class="acc">$4,500</b></li>'
 '<li><b class="acc">12,000 orders</b> in 48 hours — the servers fell over</li>'
 '<li>~25M views · sold to Unilever for <b class="acc">~$1B</b></li></ul>'
 '<div class="res">youtube.com/watch?v=RBHMf7BNd8o</div>'
 ,'n':'Watch it, then ask: what did they actually delete? The supermarket shelf. And what replaced it — subscription replaced remembering to buy, referral replaced the shelf. Their innovation was the price structure, not the razor.'},

{'k':'board','h':'<h2>Back to your shirt</h2><p class="punch">$30 → you said <em>$60</em>.</p>'
 '<p style="margin-top:1em">Let us find out what actually stays in your pocket.</p>'
 ,'n':'Whiteboard from here. Build it live, one line at a time. Do NOT show them the finished picture.'},

{'h':'<h2>Order one</h2>'+svg_eaten()+
 '<p style="margin-top:.4em">The costs run <b class="neg">past the end</b> of what she paid.</p>'
 ,'n':'You sold a shirt and you are down one dollar seventy-eight. The bar literally overflows — that is the point.'},

{'h':'<h2>And nothing else is paid yet</h2>'
 '<p class="mono dim" style="font-size:clamp(16px,2.2vw,30px)">Shopify plan · apps · salary · rent · tax</p>'
 '<p class="punch" style="margin-top:1em">The honest number is closer to <em class="neg">−$8</em>.</p>'
 ,'n':'The app stack alone is around ten percent of revenue at this size. Stop here. Let it sit.'},

{'k':'ask','h':'<p class="punch">So why would anybody <em>run this business?</em></p>'
 ,'n':'Say nothing. Wait. Let them answer. Somebody will get close.'},

{'h':'<h2>Because of this one</h2>'+svg_two_orders('−$2',2,'+$22',22)+
 '<p class="punch" style="margin-top:.6em">The business is not the shirt.<br>It is the <em>second shirt.</em></p>'
 ,'n':'Same shirt, same price. Twenty-two dollars instead of minus two. The only difference is nobody had to pay to find her. Write this down — everything for the next four weeks comes back to it.'},

{'h':'<h2>So how much are you <em class="acc">allowed</em> to spend?</h2>'+svg_ceiling()
 ,'n':'Same product, same ad, same market — the brand that gets a second order can outspend the brand that does not. That is why retention is not a nice-to-have. It is how you afford to compete at all.'},

{'h':'<h2>Not every product is the same business</h2>'+svg_once_again()
 ,'n':'One question — bought once or bought again — predicts most of what a merchant does, including whether they need us at all. Hold onto this. Session four is built on it.'},

{'h':'<h2>And every shop is these six boxes</h2>'+svg_boxes()+
 '<p style="margin-top:.4em">Every merchant message you will ever read is about <b class="acc">one box</b>.</p>'
 ,'n':'This is your map for next week. We live in COME BACK. But you cannot help someone in COME BACK if you do not know the other five exist.'},

{'h':'<h2>Your two fears, as arithmetic</h2>'
 '<div class="card" style="margin-bottom:1em"><h3>1 · I keep buying new people who vanish</h3>'
 '<p class="dim">only ever booking the first table</p></div>'
 '<div class="card"><h3>2 · I keep discounting people who would have paid anyway</h3>'
 '<p class="dim">the $9, handed to someone already buying</p></div>'
 ,'n':'These are not feelings. They are the two tables you just built. When a merchant sounds scared, it is one of these two.'},

{'k':'drill','h':'<h2>Now you</h2>'
 '<ul><li>Pairs. A real brand. Teardown sheet <b>§0–1</b></li><li>50 minutes, then every pair reports</li></ul>'
 '<p class="punch" style="margin-top:1em">At that margin, <em>how many orders</em> before they are ahead?</p>'
 ,'n':'Homework: sections 0-1 on two more brands. Classify each bought-once or bought-again. And: what does one order cost YOUR store?'},
]

# ═══════════════ SESSION 2 — BREAK DOWN A BRAND ═══════════════
S2=[
{'h':'<h1>Break down<br>a brand</h1><p class="dim" style="margin-top:1em">Session 2 · the method · phones out</p>'
 ,'n':'Goal: you can open any brand you have never seen and say what it is doing, and where it is losing people.'},

{'h':'<h2>One sheet. Any brand. No login.</h2>'
 '<p class="punch"><em>Outside-in:</em> if you cannot see it on the public site, it is not on the sheet.</p>'
 '<p style="margin-top:1.2em">No ad account. No merchant interview. No Joy admin.</p>'
 '<p class="dim" style="margin-top:.6em">First time ~45 min. By next month, 15.</p>'
 ,'n':'This is the skill the whole course is built to give you. Everything else is context for this.'},

{'h':'<h2>Why you can do this at all</h2>'+svg_shop_online()
 ,'n':'This is the difference between a shop and a website, and nearly every app in ecom exists because of it.'},

{'h':'<p class="punch">In a shop, someone who leaves is <em>gone.</em></p>'
 '<p class="punch" style="margin-top:.8em">Online, someone who leaves is <em>a list.</em></p>'
 ,'n':'That is why the popup exists, why retargeting exists, why abandoned cart email is the most profitable email in ecom. And it is why loyalty works at all — loyalty is identity applied over time.'},

{'h':'<h2>The path you are looking for</h2>'+svg_funnel()
 ,'n':'Nine stops from stranger to paid. Your job walking a brand is to find where people fall out. Not to fix it — to find it.'},

{'k':'look','h':'<h2>Start at the ad</h2>'
 '<p>Find a live ad for tonight\'s brand. Then click through.</p>'
 '<div class="res">facebook.com/ads/library</div>'
 '<p class="punch" style="margin-top:1em">Does the page <em>repeat the promise</em> the ad just made?</p>'
 ,'n':'An ad is an argument aimed at one person: name her problem, prove it, make it urgent. The most common way to waste thirty dollars is the ad promising one thing and the page saying another.'},

{'k':'look','h':'<h2>The popup</h2><p class="punch">"10% off your first order"</p>'
 '<p style="margin-top:1em">What is actually being bought here?</p>'
 '<p style="margin-top:.6em">Not the sale. <b class="acc">The email.</b></p>'
 '<p class="dim" style="margin-top:1em">And the 10% is real. Some who take it would have paid full price — fear #2, in the first thirty seconds.</p>'
 ,'n':'Trigger it live on the projector so they watch it fire. Then point out: without this, recovery later is impossible.'},

{'h':'<h2>The product page answers three questions</h2>'
 '<p class="punch">Will this work for me?<br>Can I trust you?<br>What if I hate it?</p>'
 '<p style="margin-top:1.2em">Reviews answer all three, cheaper than any copy.</p>'
 ,'n':'A hidden returns policy kills the sale. A stranger will not risk forty-two dollars on a shop that will not say what happens if it fails.'},

{'h':'<h2>Subscribe or bundle — not the same thing</h2><table>'
 '<tr><th></th><th>Buys the owner</th><th>Costs</th></tr>'
 '<tr><td><b>Subscription</b></td><td class="acc"><b>LTV</b> — next order agreed</td><td>15% margin, forever</td></tr>'
 '<tr><td><b>Bundle</b></td><td class="acc"><b>AOV</b> — fatter order today</td><td>less per unit, more cash now</td></tr></table>'
 ,'n':'Different problems. A shop with a repeat problem needs the first. A shop with thin orders needs the second. Do not let anyone say them in the same breath.'},

{'k':'look','h':'<h2>The cart, and the strongest lever in ecom</h2>'
 '<p class="punch">"You are <em>$12 away</em> from free shipping."</p>'
 '<p style="margin-top:1.2em">She would rather add $12 of product than pay $7 of shipping for nothing.</p>'
 ,'n':'Add to cart live so they watch the bar move. Free shipping thresholds move AOV more than almost anything else.'},

{'h':'<h2>Checkout — where intent goes to die</h2>'
 '<ul><li><b class="acc">Extra costs are the #1 abandon reason — 39%</b></li>'
 '<li>The discount code box is a <b>leak</b></li>'
 '<li>Express wallets: five fields → one thumbprint</li>'
 '<li>Guest checkout — do not force an account on a stranger</li></ul>'
 '<p class="dim" style="margin-top:1em">~70% of carts are abandoned. That is normal, not failure.</p>'
 '<div class="res">baymard.com/lists/cart-abandonment-rate</div>'
 ,'n':'A seven dollar fee on a forty-two dollar order reads as a seventeen percent price rise. It is the surprise, not the price.'},

{'h':'<h2>Every leak has a name</h2><table>'
 '<tr><th>The number</th><th>Where</th><th>Low means</th></tr>'
 '<tr><td>Site speed</td><td class="dim">landing</td><td>she left before it loaded</td></tr>'
 '<tr><td>Email capture</td><td class="dim">popup</td><td>you do not know who is visiting</td></tr>'
 '<tr><td><b>Add-to-cart rate</b></td><td class="dim">product</td><td>the page did not convince her</td></tr>'
 '<tr><td><b>AOV</b></td><td class="dim">cart</td><td>orders are too thin</td></tr>'
 '<tr><td><b>Checkout rate</b></td><td class="dim">checkout</td><td>shipping shock, friction</td></tr></table>'
 ,'n':'These numbers are not abstract. Each one is a place on the path you just walked.'},

{'h':'<p class="punch">"Conversion is down" is <em>not a problem.</em></p>'
 '<p style="margin-top:1em">It is a symptom of a leak at one specific place.</p>'
 '<p class="punch" style="margin-top:1.2em">An AM finds the place.<br><span class="dim">CS forwards the sentence.</span></p>'
 ,'n':'That sentence is the difference between the two jobs. That is all it is.'},

{'k':'look','h':'<h2>Now read what they installed</h2>'
 '<p class="mono dim">right-click → View Page Source → Ctrl-F</p>'
 '<div class="res mono">klaviyo · attentive · recharge · appstle · skio · smile<br>'
 'yotpo · loyaltylion · rivo · growave · okendo · judge.me<br>gorgias · rebuy · subscribe</div>'
 '<p style="margin-top:1em">Then the footer · <span class="mono">/account</span> · <span class="mono acc">/pages/rewards</span></p>'
 ,'n':'Do it live. It is genuinely fun to watch. Sixty seconds and you know more than a discovery call would tell you.'},

{'h':'<h2>The stack is a confession</h2>'+svg_confession()
 ,'n':'Nobody installs a bundle app for fun. They installed it at 11pm after looking at a number that scared them. The stack tells you what the owner is afraid of before they say a word.'},

{'k':'drill','h':'<h2>Now you — the whole sheet</h2>'
 '<ul><li>Pairs, <b>phones out</b>, a real brand, real money in the cart</li>'
 '<li>Walk it as a customer. Fill <b>§0–6</b></li>'
 '<li>Every stop: what you saw · what they wanted · <b>what would make you quit</b></li></ul>'
 '<p class="punch" style="margin-top:1em">The main door, the place you would quit, and <em>what this owner is paying to fix.</em></p>'
 ,'n':'Homework: a full teardown on two more brands. Walk your own store and mark where you would quit. Three tickets from your queue — which part of the path is each really about?'},
]

# ═══════════════ SESSION 3 — RETENTION & LOYALTY, DEEP ═══════════════
S3=[
{'h':'<h1>Why people<br>come back</h1><p class="dim" style="margin-top:1em">Session 3 · retention and loyalty · our actual subject</p>'
 ,'n':'Goal: you understand why a person buys a second time, and what actually makes them. This is the session about our own product area.'},

{'h':'<h2 class="dim">Last week ended the moment she paid.</h2>'
 '<p class="punch">Every business thinks that is the finish line.</p>'
 '<p class="punch" style="margin-top:.6em">It is <em>the start.</em></p>'
 ,'n':'Everything from here is where the money actually is.'},

{'h':'<h2>The wait</h2>'
 '<p class="mono dim" style="font-size:clamp(16px,2.4vw,32px)">paid —————— ? —————— arrived</p>'
 '<p style="margin-top:1.2em">Nothing happens here. That is the problem.</p>'
 '<p style="margin-top:.8em">This gap is where every <b class="acc">"where is my order"</b> ticket is born.</p>'
 ,'n':'Usually the biggest ticket category in ecom. You live in it already. A late parcel someone warned you about is fine. A late parcel nobody mentioned is a refund and a one-star review.'},

{'h':'<h2>The eight weeks after she pays</h2>'+svg_timeline()
 ,'n':'The review comes when she has USED it, not when it arrived. A review on day one is a review of the packaging. And week six is the one that pays — you arrive before she runs out and before she thinks about alternatives.'},

{'h':'<p class="punch">That one email is worth more than <em>the whole ad</em> that found her.</p>'
 '<p style="margin-top:1.4em">It costs almost nothing. It goes to somebody who already likes them.</p>'
 ,'n':'Say it twice. One automated email beats thirty dollars of advertising.'},

{'h':'<h2>And she is everywhere now</h2>'
 '<p class="mono" style="font-size:clamp(15px,2vw,28px)">saw the ad → got the email → watched a creator → <b class="acc">bought on Amazon</b></p>'
 '<p class="punch" style="margin-top:1.4em">Four arrows. <em>One sale.</em> Who gets the credit?</p>'
 ,'n':'Retargeting is far cheaper than the first ad, because they are no longer paying to find a stranger — they are paying to remind a customer. And this is why attribution is a swamp. You do not have to solve it. Just stop being surprised when a merchant says the numbers do not match.'},

{'k':'ask','h':'<p class="punch">Why would a human buy <em>this</em> twice?</p>'
 ,'n':'Ask it about tonight\'s two brands. Let the room struggle on the weak one. Do not rescue them.'},

{'h':'<h2>Sometimes there is no reason</h2>'+svg_once_again()+
 '<p style="margin-top:.4em">A mattress. A set of pans. That is not a failure of the shop —<br>it is a <b class="acc">fact about the product</b>, and it decides everything they need.</p>'
 ,'n':'This is the uncomfortable one. If the honest answer is no reason, a points program will not create one. Hold that thought for next week.'},

{'h':'<h2>Lumi, all the way through</h2>'+svg_two_orders('+$2.13',2.13,'+$17.28',17.28,neg1=False)+
 '<p class="dim" style="margin-top:.4em">Mai spent $61.20 the first time and $42 the second.</p>'
 ,'n':'The first order paid for the ad and almost nothing else. The second one, with no ad attached, is worth eight of it. Same shop, same product, same customer.'},

{'h':'<h2>Order 1 — where it all went</h2><table>'
 '<tr><td>Ad to reach Mai</td><td class="n neg">−$30.00</td></tr>'
 '<tr><td>Cart: moisturizer + travel size</td><td class="n">+$68.00</td></tr>'
 '<tr><td>Popup 10%</td><td class="n neg">−$6.80</td></tr>'
 '<tr><td>Free shipping, Lumi pays it</td><td class="n neg">−$7.00</td></tr>'
 '<tr><td>Processing</td><td class="n neg">−$2.07</td></tr>'
 '<tr><td>Products</td><td class="n neg">−$20.00</td></tr>'
 '<tr class="tot"><td>Lumi keeps</td><td class="n acc">+$2.13</td></tr></table>'
 ,'n':'Mai spent sixty-one twenty. The shop kept two thirteen. Stop talking for a second.'},

{'h':'<h2 class="dim">So what did the points actually do?</h2>'
 '<p class="punch">They did not make Mai <em>like</em> Lumi.</p>'
 '<p style="margin-top:1.2em">They gave her a reason to choose Lumi <b>instead of the alternative</b>, in that moment — and a nudge to do it <b>now</b> rather than in three weeks.</p>'
 '<p class="punch" style="margin-top:1.2em">Loyalty does not buy affection.<br>It buys <em>timing and preference.</em></p>'
 ,'n':'If you remember one sentence about our product, make it that one.'},

{'h':'<h2>Three things, not one thing</h2><table>'
 '<tr><th>Subscription</th><th>Loyalty</th><th>Discount</th></tr>'
 '<tr><td>the next box is already agreed</td><td>a reason to choose <b>you</b> next time</td><td>this order is cheaper</td></tr></table>'
 '<p class="punch" style="margin-top:1.4em">Merchants mix these up constantly.<br>If you mix them up too, <em>you cannot help them.</em></p>'
 ,'n':'A standing order does not mean she chose you. It means she has not cancelled yet. Those are different, and the gap is what we sell.'},

{'h':'<h2>Two machines, opposite jobs</h2>'+svg_grow_vs_keep()
 ,'n':'A referred person arrives with trust already loaded, and you pay only when it works — unlike an ad, which you pay on hope. Remember this: next week it decides what you recommend to a real merchant.'},

{'h':'<h2>And if they want points — or credit?</h2>'+svg_points_credit()
 ,'n':'Both are real answers. Neither is the default. Considered, expensive, rare purchase — credit is clearer. Refill or consumable — points build the habit. Lots of returns — credit keeps the money in the shop. Wants members — points, named, on brand.'},

{'h':'<p class="punch">Points are the brand&rsquo;s <em>currency.</em></p>'
 '<p class="punch" style="margin-top:.8em">Store credit is just <em>money with your logo on it.</em></p>'
 ,'n':'Which is also why on-brand matters and is not decoration. If the widget looks like a generic app bolted on, it is not brand currency any more — it is a coupon machine, and you threw away the only reason you chose points.'},

{'k':'ask','h':'<h2>VIP tiers — spend $500 to reach Gold.</h2>'
 '<p class="punch">Why <em>$500?</em></p>'
 ,'n':'Let them flounder. Nobody can defend it, because today the number is guessed. That is the problem.'},

{'h':'<h2>Where the number actually comes from</h2><ul>'
 '<li>Pull customers with total spend, last 12 months</li><li>Sort, highest first</li>'
 '<li>Decide the share per tier — commonly <b class="acc">~5% top, ~20% middle</b></li>'
 '<li>The spend at that cut line <b>is</b> your threshold</li></ul>'
 '<p style="margin-top:1em">Then check both ways: is the top tier <b>big enough to matter</b>, and is the next tier <b>reachable in a year</b>?</p>'
 '<p class="punch" style="margin-top:1em">If you cannot say why the number is that number, <em>do not set it.</em></p>'
 ,'n':'A threshold nobody can reach is decoration. A threshold everybody clears is a discount for everyone — which is fear two with extra steps. And the reason tiers exist at all is fear two: otherwise you hand the same coupon to a first-time buyer and to someone who spends two thousand a year.'},

{'k':'drill','h':'<h2>Now you</h2>'
 '<ul><li>Pairs. <b>Two</b> brands — one with a strong repeat reason, one with a weak one</li>'
 '<li>Teardown <b>§4–5</b>, then prescribe</li></ul>'
 '<p class="punch" style="margin-top:1em">Points, credit, tiers or referral — and <em>what does the option you rejected lose?</em></p>'
 ,'n':'Homework: what is the real reason someone reorders from YOUR store? Five tickets restated in two sentences each, own words, Vietnamese fine, no questions to the merchant.'},
]

# ═══════════════ SESSION 4 — BRING IT TOGETHER ═══════════════
S4=[
{'h':'<h1>Bring it<br>together</h1><p class="dim" style="margin-top:1em">Session 4 · a real merchant, a real call</p>'
 ,'n':'Goal: given a real merchant, you can say whether it is ours, whether it needs us, and what to do about it.'},

{'h':'<h2>Three weeks ago you could not do any of this</h2><ul>'
 '<li>How does this shop make money on one order?</li>'
 '<li>How do people arrive, and where do they quit?</li>'
 '<li>Why would someone buy twice — and what is the brand doing about it?</li></ul>'
 '<p class="punch" style="margin-top:1.2em">Tonight we add the last one: <em>so what do we tell them?</em></p>'
 ,'n':'And you still have not opened Joy once.'},

{'k':'ask','h':'<p class="punch">Is Recharge a <em>subscription app?</em></p>'
 ,'n':'Let them say yes. Then say no — it is a solution for increasing lifetime value. Klaviyo is not an email app, it is a cheap way to talk to everyone at scale plus a CRM. We do not sell an app. We sell the solution the app is made of.'},

{'h':'<h2>Is it ours? Run the checklist</h2><table>'
 '<tr><td>Shopify or Plus</td><td class="n dim">□</td></tr>'
 '<tr><td>Category that repurchases <span class="dim">— beauty, apparel, wellness, kids, outdoor, pet, home</span></td><td class="n dim">□</td></tr>'
 '<tr><td>Roughly $5–40M</td><td class="n dim">□</td></tr>'
 '<tr><td><b>Klaviyo or Attentive</b> installed</td><td class="n dim">□</td></tr>'
 '<tr><td>Growing — raise, press, retail, viral</td><td class="n dim">□</td></tr>'
 '<tr><td><b>No</b> Rivo / Yotpo / Smile / LoyaltyLion / Growave</td><td class="n dim">□</td></tr></table>'
 '<p class="acc" style="margin-top:1em">Every line is visible from the public site. You never ask them.</p>'
 ,'n':'This is Joy\'s real ICP, not something invented for class. And you already know how to check every line — that was last week.'},

{'h':'<h2>The easiest win to recognise</h2>'
 '<p class="punch">Recharge or Appstle <em>+</em> Klaviyo <em>+</em> no loyalty app</p>'
 '<p style="margin-top:1.4em">They already pay for repeat revenue. They have nothing that gives a reason to <b>return</b>.</p>'
 ,'n':'Subscription is not loyalty — the next box being agreed is not the same as being chosen. That is exactly the gap we fill, and it is not a rip-and-replace.'},

{'k':'look','h':'<h2>The textbook case</h2><p class="punch">raewellness.co</p>'
 '<ul><li>Recharge, heavily used</li><li>Klaviyo</li><li>Wellness — natural repurchase</li>'
 '<li><b class="acc">/pages/rewards → 404</b></li></ul>'
 ,'n':'Do it live. Thirty seconds. View source, Ctrl-F recharge and klaviyo — both hit. Ctrl-F smile, loyaltylion, yotpo — nothing. Then type slash pages slash rewards. 404. That is the entire pitch, and they found it themselves without asking the merchant anything.'},

{'k':'ask','h':'<p class="punch">But does this shop need a loyalty program <em>at all?</em></p>'
 ,'n':'This is the question that separates you from a salesperson. Let it hang.'},

{'h':'<h2>A loyalty program is a multiplier</h2>'+svg_dots()+
 '<p class="punch" style="margin-top:.4em">Multiply a small number — <em>it is still small.</em></p>'
 ,'n':'Shop A has a perfect loyalty program and is going out of business. You cannot multiply your way out of a base of a hundred. A loyalty program is a multiplier on a base you already have. It is not a growth engine.'},

{'h':'<h2>So the first question is stage</h2>'+svg_stage()+
 '<p style="margin-top:.4em">Remember from last week — referral <b>grows</b> the base, loyalty <b>monetises</b> it.</p>'
 ,'n':'The shop that must NOT be sold points is often exactly the shop that should run referral. So "not ready" is never a dead end. It is a different recommendation.'},

{'h':'<p class="punch">"Not yet" is a <em>correct answer.</em></p>'
 '<p style="margin-top:1.4em">Telling a survival-stage shop to launch points is not service. It is selling them the wrong thing, it will not produce a result, and they will churn — <b>correctly</b>.</p>'
 ,'n':'If you cannot say "not yet" out loud, you are selling, not advising. And you lose the account anyway, six months later, with worse feelings.'},

{'h':'<h2 class="dim">The hardest thing you will have to say</h2>'
 '<p>They installed a bundle app. Their real leak is that <b>nobody comes back.</b></p>'
 '<p class="punch" style="margin:1.2em 0">They are fixing <em>the cart</em> while bleeding at <em>the second order.</em></p>'
 '<p class="punch">Do you <em>tell them?</em></p>'
 ,'n':'Yes. That is the service. That is the whole difference between answering the app and owning the outcome. And it costs something — you are telling a paying merchant that the thing they bought is not their problem.'},

{'h':'<h2>The conversation, replaced</h2>'
 '<p class="dim">Never: <span class="mono">"Points or store credit? OK, I\'ll show you where to turn it on."</span></p>'
 '<ul style="margin-top:1em"><li><b>1 Stage</b> — is there a base to sell back to?</li>'
 '<li><b>2 Base</b> — how many, how many return, typical basket</li>'
 '<li><b>3 Fear</b> — losing new people, or over-discounting?</li>'
 '<li><b>4 Mechanism</b> — referral, points, credit, tiers</li>'
 '<li><b>5 Numbers</b> — thresholds from their data, defended</li>'
 '<li><b>6 Placement</b> — from their journey, not the demo store</li></ul>'
 ,'n':'Only after all six does a screen appear. Steps one to five are the service. That is what we are actually paid for.'},

{'h':'<p class="punch">Only the last step is <em>a screen.</em></p>'
 '<p style="margin-top:1.4em">Everything before it is the thing a machine cannot do for them.</p>'
 ,'n':'Call back to the talk. AI took the execution. What is left for people is the outcome — judgement about one specific business, and being accountable for it.'},

{'h':'<h2>The gate</h2>'
 '<div class="card" style="margin-bottom:.8em"><h3>1 · A cold teardown</h3>'
 '<p class="dim">a brand you have never seen · 15 minutes · a lead accepts it</p></div>'
 '<div class="card" style="margin-bottom:.8em"><h3>2 · 8 of 12 restatements</h3>'
 '<p class="dim">timed, from your own queue</p></div>'
 '<div class="card"><h3>3 · Your store, launched, to standard</h3>'
 '<p class="dim">max three apps, every one defensible</p></div>'
 ,'n':'"Not yet" is a normal outcome here too. It means another stack of reps, not another lecture.'},

{'k':'drill','h':'<h2>Now you — the whole thing</h2>'
 '<ul><li><b>Two</b> brands side by side. One strong fit, one deliberately not ours</li>'
 '<li>Full teardown, then a <b>verdict out loud</b> with the reason</li>'
 '<li>Fit is learned by contrast — never one brand alone</li></ul>'
 '<p class="punch" style="margin-top:1em">Is it ours · does it need this · <em>what is the one thing we would change?</em></p>'
 ,'n':'A checklist memorised is trivia. A checklist run against a brand that fails it is judgement. That is what we are grading.'},

{'h':'<p class="punch">You have not opened Joy <em>once.</em></p>'
 '<p style="margin-top:1.4em">And you can already tell a merchant whether we can help them, and why.</p>'
 '<p class="dim" style="margin-top:1.2em">That was the whole point.</p>'
 ,'n':'End here. Do not add anything. Sit down.'},
]

if __name__=='__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print('Building:')
    build('session-1-basics.html','Session 1 — How a shop makes money','Session 1 · The basics',S1)
    build('session-2-breakdown.html','Session 2 — Break down a brand','Session 2 · Break down a brand',S2)
    build('session-3-retention.html','Session 3 — Why people come back','Session 3 · Retention & loyalty',S3)
    build('session-4-together.html','Session 4 — Bring it together','Session 4 · Bring it together',S4)
    print('Done. ← → to move · S for speaker notes · Cmd-P to PDF.')
