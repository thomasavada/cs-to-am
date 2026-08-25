#!/usr/bin/env python3
"""Session decks — Neo-Grid Bold (frontend-slides by zarazhangrui).
Fixed 1920x1080 stage, 12x8 grid, Space Grotesk + JetBrains Mono, neon lemon on putty ecru.
Run: python3 build.py"""
import os, html as H

D = os.path.dirname(os.path.abspath(__file__))
# Images are referenced from assets/ by default — keeps the HTML small and diffable.
# Set EMBED=1 to inline them as base64 for a single self-contained file you can email.
EMBED = os.environ.get('EMBED') == '1'
def _asset(n):
    jpg = os.path.join(D, 'assets', n + '.jpg')
    if not os.path.exists(jpg): return ''
    if not EMBED: return f'assets/{n}.jpg'
    import base64
    return 'data:image/jpeg;base64,' + base64.b64encode(open(jpg,'rb').read()).decode()
SNEAKER, DSC, RAE404 = _asset('sneaker'), _asset('dsc-store'), _asset('rae-404')
DSCTHUMB, CHASETHUMB = _asset('dsc-thumb'), _asset('chase-thumb')
CROWN, HALFDAYS, HEXCLAD, HEXPOPUP = _asset('crownaffair'), _asset('halfdays'), _asset('hexclad'), _asset('hexclad-popup')

CSS = """
:root{--paper:#F5F4EF;--bg:#ECECE8;--ink:#0A0A0A;--lemon:#E6FF3D;--muted:#8A8A85;--stage-bg:#1A1A1A}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:100%;height:100%;margin:0;overflow:hidden;background:var(--stage-bg)}
.deck-viewport{position:fixed;inset:0;overflow:hidden;background:var(--stage-bg)}
.deck-stage{position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:hidden;transform-origin:0 0;background:var(--bg)}
.slide{position:absolute;inset:0;width:1920px;height:1080px;overflow:hidden;display:block;
  visibility:hidden;opacity:0;pointer-events:none;background:var(--bg)}
.slide.active{visibility:visible;opacity:1;pointer-events:auto;z-index:1}
img,svg{max-width:100%;max-height:100%}

.frame{position:absolute;inset:40px;display:grid;grid-template-columns:repeat(12,1fr);
  grid-template-rows:repeat(8,1fr);gap:12px}
.card{background:var(--paper);position:relative;overflow:hidden;padding:26px 34px;display:flex;
  flex-direction:column;justify-content:center}
.card.ink{background:var(--ink);color:var(--paper)}
.card.lemon{background:var(--lemon);color:var(--ink)}
.card.photo{background:#000;padding:0;justify-content:stretch}
.card.photo img{width:100%;height:100%;object-fit:cover;object-position:top center;display:block;max-height:none}
.card.contain{background:#0d1117;padding:0}
.card.contain img{width:100%;height:100%;object-fit:contain;display:block;max-height:none}
.card.flat{justify-content:flex-start}
.card.plain{background:transparent;padding:0}

.d{font:700 132px/1.42 'Space Grotesk',Helvetica,Arial,sans-serif;letter-spacing:-.02em;text-transform:uppercase}
.t{font:700 88px/1.16 'Space Grotesk',Helvetica,Arial,sans-serif;letter-spacing:-.015em;text-transform:uppercase}
.st{font:700 56px/1.14 'Space Grotesk',Helvetica,Arial,sans-serif;letter-spacing:-.01em;text-transform:uppercase}
.n{font:700 156px/0.9 'Space Grotesk',Helvetica,Arial,sans-serif;letter-spacing:-.03em}
.n-lg{font:700 240px/0.85 'Space Grotesk',Helvetica,Arial,sans-serif;letter-spacing:-.04em}
.n-sm{font:700 96px/0.9 'Space Grotesk',Helvetica,Arial,sans-serif;letter-spacing:-.03em}
.ch{font:700 44px/1 'Space Grotesk',Helvetica,Arial,sans-serif;letter-spacing:-.01em;text-transform:uppercase}
.c3{font:700 30px/1.05 'Space Grotesk',Helvetica,Arial,sans-serif;text-transform:uppercase}
.b{font:400 28px/1.35 'Space Grotesk',Helvetica,Arial,sans-serif}
.bs{font:400 22px/1.45 'Space Grotesk',Helvetica,Arial,sans-serif}
.l{font:400 24px/1 'JetBrains Mono',ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase}
.ls{font:400 16px/1.3 'JetBrains Mono',ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase}
.lx{font:400 14px/1.3 'JetBrains Mono',ui-monospace,monospace;letter-spacing:.12em;text-transform:uppercase}
.mut{color:var(--muted)}.lem{color:var(--lemon)}.inkc{color:var(--ink)}
b,strong{font-weight:700}
em{font-style:normal;background:var(--lemon);color:var(--ink);padding:0 .14em;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.ink em{background:var(--lemon);color:var(--ink)}
.lemon em{background:var(--ink);color:var(--lemon)}
.mt{margin-top:20px}.mt2{margin-top:32px}.mb{margin-bottom:16px}
ul{list-style:none}
li{position:relative;padding-left:34px;margin:14px 0}
li:before{content:"";position:absolute;left:0;top:.52em;width:16px;height:4px;background:var(--ink)}
.ink li:before{background:var(--lemon)}.lemon li:before{background:var(--ink)}

table{width:100%;border-collapse:collapse}
td,th{padding:11px 0;text-align:left;border-bottom:2px solid rgba(10,10,10,.13);
  font:400 26px/1.2 'Space Grotesk',Helvetica,Arial,sans-serif}
.ink td,.ink th{border-color:rgba(245,244,239,.18)}
th{font:400 16px/1 'JetBrains Mono',monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
td.r{text-align:right;font-variant-numeric:tabular-nums;font-weight:700;white-space:nowrap;padding-right:56px}
td.r:last-child{padding-right:0}
table.duo td{width:25%}table.duo td.r{padding-right:64px}table.duo td.r:last-child{padding-right:0}
tr.tot td{border-bottom:none;border-top:4px solid var(--ink);font-weight:700;font-size:32px;padding-top:14px}
.ink tr.tot td{border-top-color:var(--lemon)}

.stack{display:flex;height:132px;border:4px solid var(--ink)}
.stack>div{display:flex;flex-direction:column;align-items:center;justify-content:center;
  border-right:4px solid var(--ink);overflow:hidden;min-width:70px;flex-shrink:0}
.stack>div:last-child{border-right:none}
.stack .v{font:700 40px/1 'Space Grotesk',sans-serif}
.stack .k{font:400 13px/1.15 'JetBrains Mono',monospace;letter-spacing:.06em;text-transform:uppercase;
  margin-top:7px;text-align:center;padding:0 6px;opacity:.72}
.stack .v.sm{font-size:24px;letter-spacing:-.02em}
.bar{height:74px;border:4px solid var(--ink);display:flex;align-items:center;padding:0 20px;
  font:700 34px/1 'Space Grotesk',sans-serif}
.tag{display:inline-block;padding:9px 20px;font:400 18px/1 'JetBrains Mono',monospace;
  letter-spacing:.1em;text-transform:uppercase;background:var(--ink);color:var(--paper)}
.tag.lem{background:var(--lemon);color:var(--ink)}
.rule{height:4px;background:var(--ink);margin:22px 0}
.ink .rule{background:var(--lemon)}
.pn{position:absolute;left:40px;bottom:40px;z-index:5;background:var(--ink);color:var(--paper);
  padding:9px 16px;font:400 20px/1 'JetBrains Mono',monospace;letter-spacing:.05em}
.kick{position:absolute;right:40px;top:40px;z-index:5;background:var(--lemon);color:var(--ink);
  padding:9px 18px;font:400 18px/1 'JetBrains Mono',monospace;letter-spacing:.1em;text-transform:uppercase}
.frow{display:flex;align-items:center;gap:16px;margin-bottom:6px}
.fbar{min-width:76px;height:52px;display:flex;align-items:center;justify-content:center;
  font:700 28px/1 'Space Grotesk',Helvetica,sans-serif;background:var(--ink);color:var(--paper)}
.fbar.win{background:var(--lemon);color:var(--ink)}
.fdrop{display:flex;align-items:baseline;gap:12px;margin:0 0 6px 8px;
  border-left:4px solid var(--muted);padding:4px 0 8px 16px}
.fdrop b.n{font:700 24px/1 'Space Grotesk',Helvetica,sans-serif;color:var(--bad)}
.url{font:400 20px/1.3 'JetBrains Mono',ui-monospace,monospace;color:var(--muted)}
a.go{display:inline-block;padding:9px 18px;margin:5px 8px 5px 0;background:var(--ink);color:var(--lemon);
  font:400 19px/1 'JetBrains Mono',ui-monospace,monospace;letter-spacing:.03em;text-decoration:none;
  border:3px solid var(--ink);white-space:nowrap}
a.go:hover{background:var(--lemon);color:var(--ink)}
.ink a.go{background:var(--lemon);color:var(--ink);border-color:var(--lemon)}
.ink a.go:hover{background:transparent;color:var(--lemon)}
.lemon a.go{background:var(--ink);color:var(--lemon);border-color:var(--ink)}
.lemon a.go:hover{background:transparent;color:var(--ink)}
a.go:after{content:" ↗";opacity:.65}
.dots{display:grid;gap:3px}
.dots i{display:block;width:100%;aspect-ratio:1}

#notes{position:fixed;left:0;right:0;bottom:0;max-height:44vh;overflow:auto;background:#0A0A0A;
  color:#F5F4EF;border-top:6px solid #E6FF3D;padding:20px 30px 34px;display:none;z-index:1000;
  font:400 19px/1.55 'Space Grotesk',Helvetica,Arial,sans-serif}
#notes.on{display:block}
#notes b{display:block;color:#E6FF3D;font:400 13px/1 'JetBrains Mono',monospace;
  letter-spacing:.16em;text-transform:uppercase;margin-bottom:9px}
#hud{position:fixed;right:16px;bottom:12px;z-index:1000;color:#8A8A85;
  font:400 13px/1 'JetBrains Mono',monospace;letter-spacing:.06em}
@media print{html,body{width:1920px;height:auto;overflow:visible;background:#fff}
 .deck-viewport{position:static;overflow:visible}
 .deck-stage{position:static;width:auto;height:auto;transform:none!important}
 .slide{position:relative;visibility:visible!important;opacity:1!important;break-after:page}
 #notes,#hud{display:none!important}}
@media (prefers-reduced-motion:reduce){*{animation-duration:.01ms!important;transition-duration:.2s!important}}
"""

JS = """
const stage=document.querySelector('.deck-stage'),S=[...document.querySelectorAll('.slide')];
const N=document.getElementById('notes'),NB=document.getElementById('nb'),HUD=document.getElementById('hud');
let i=0;
function fit(){const s=Math.min(innerWidth/1920,innerHeight/1080);
 stage.style.transform=`translate(${(innerWidth-1920*s)/2}px,${(innerHeight-1080*s)/2}px) scale(${s})`;}
function go(n){i=Math.max(0,Math.min(S.length-1,n));
 S.forEach((s,k)=>s.classList.toggle('active',k===i));
 HUD.textContent=(i+1)+' / '+S.length;
 NB.innerHTML=S[i].dataset.notes||'<span style="color:#8A8A85">no notes</span>';
 if(location.hash!=='#'+(i+1))location.hash=i+1;}
addEventListener('resize',fit);
addEventListener('hashchange',()=>go(parseInt(location.hash.slice(1)||'1')-1));
addEventListener('keydown',e=>{
 if(['ArrowRight','ArrowDown',' ','PageDown'].includes(e.key)){e.preventDefault();go(i+1)}
 else if(['ArrowLeft','ArrowUp','PageUp'].includes(e.key)){e.preventDefault();go(i-1)}
 else if(e.key==='Home')go(0); else if(e.key==='End')go(S.length-1);
 else if(e.key.toLowerCase()==='s'||e.key.toLowerCase()==='n')N.classList.toggle('on');});
addEventListener('click',e=>{if(e.target.tagName!=='A')go(i+1)});
/* Cards clip at overflow:hidden, so any cell whose content exceeds its grid rows would
   silently lose text. autofit() shrinks the card instead. Floor is 0.6 — if a card is still
   clipped at 0.6 it needs more rows, not more shrinking. Check with the browser sweep in
   sessions/README-check.md */
function autofit(){
 document.querySelectorAll('.card').forEach(c=>{
  c.style.zoom='';
  const sl=c.closest('.slide'); const was=sl.classList.contains('active');
  if(!was) sl.classList.add('active');
  let k=1;
  while(c.scrollHeight-c.clientHeight>2 && k>0.5){ k-=0.03; c.style.zoom=k; }
  if(!was) sl.classList.remove('active');
 });}
if(document.fonts&&document.fonts.ready){document.fonts.ready.then(autofit);}else{addEventListener('load',autofit);}
fit();go(parseInt(location.hash.slice(1)||'1')-1);
"""


class _V(__import__('html.parser',fromlist=['HTMLParser']).HTMLParser):
    """Catches swallowed markup: an attribute value containing '<' means an unclosed quote
    ate the rest of the document (the data-x bug). Also counts real slide sections."""
    def __init__(self):
        super().__init__(); self.sections=0; self.bad=[]
    def handle_starttag(self, tag, attrs):
        if tag=='section': self.sections+=1
        for k,v in attrs:
            if v and ('<' in v or len(v)>4000 and 'base64' not in v):
                self.bad.append(f'<{tag} {k}="{v[:70]}...">')

def validate(fn, expected):
    p=_V(); p.feed(open(fn).read())
    errs=[]
    if p.sections!=expected: errs.append(f'{p.sections} sections parsed, expected {expected}')
    if p.bad: errs.append(f'{len(p.bad)} swallowed-markup attribute(s): {p.bad[0]}')
    if errs:
        print(f'  !! {fn}: ' + ' | '.join(errs)); return False
    return True

def cell(c1,c2,r1,r2,inner,cls=''):
    return (f'<div class="card {cls}" style="grid-column:{c1}/{c2};grid-row:{r1}/{r2}">{inner}</div>')

def slide(frame_html, notes='', kicker=None, num=None):
    # `num` is ignored — build() numbers slides by position so a split cannot desync them
    extra = f'<div class="kick">{kicker}</div>' if kicker else ''
    return {'html':f'<div class="frame">{frame_html}</div>{extra}','n':notes}

def build(fn, title, slides):
    secs=''
    for k,s in enumerate(slides):
        s.setdefault('n','')
        pn = '' if k==0 else f'<div class="pn">{k+1:02d}</div>'
        secs+=f'<section class="slide" data-notes="{H.escape(s["n"])}">{s["html"]}{pn}</section>'
    doc=(f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
         f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{H.escape(title)}</title>'
         '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">'
         f'<style>{CSS}</style></head><body>'
         f'<div class="deck-viewport"><div class="deck-stage">{secs}</div></div>'
         '<div id="hud"></div><div id="notes"><b>say</b><div id="nb"></div></div>'
         f'<script>{JS}</script></body></html>')
    open(fn,'w').write(doc)
    ok = validate(fn, len(slides))
    print(f'  {fn}  {len(slides)} slides  {len(doc)//1024}KB  {"ok" if ok else "BROKEN"}')

# ── small builders ──
def stack(segs):
    """segs=[(weight,'$21','make it',dark?)]"""
    out=''
    for w,v,k,dark in segs:
        bg='var(--ink)' if dark==1 else ('var(--lemon)' if dark==2 else 'var(--paper)')
        fg='var(--paper)' if dark==1 else 'var(--ink)'
        vc='v' if w>=7 else 'v sm'
        out+=(f'<div style="flex:{w} 1 auto;background:{bg};color:{fg}">'
              f'<div class="{vc}">{v}</div>'+(f'<div class="k">{k}</div>' if w>=7 else '')+'</div>')
    return f'<div class="stack">{out}</div>'

def logo(name, size=46):
    p = os.path.join(D,'assets','logos',name+'.png')
    if not os.path.exists(p): return ''
    src = ('data:image/png;base64,'+__import__('base64').b64encode(open(p,'rb').read()).decode()) if EMBED else f'assets/logos/{name}.png'
    return (f'<img src="{src}" alt="" style="width:{size}px;height:{size}px;object-fit:contain;'
            'vertical-align:middle;background:#fff;border-radius:8px;padding:4px;margin-right:10px">')

def applogo(name, label, size=46):
    return ('<span style="display:inline-flex;align-items:center;margin:0 22px 12px 0;white-space:nowrap">'
            + logo(name,size) + f'<span class="bs">{label}</span></span>')

def logorow(items, size=46):
    return '<div style="display:flex;flex-wrap:wrap;align-items:center">' + ''.join(applogo(n,l,size) for n,l in items) + '</div>'

def video(vid, title='', thumb=''):
    """YouTube player with a local thumbnail behind it, so the slide still reads
    if the embed is blocked or the room is offline. Click the chip to open on YouTube."""
    back = (f'<img src="{thumb}" alt="" style="position:absolute;inset:0;width:100%;height:100%;'
            'object-fit:cover;z-index:0">') if thumb else ''
    play = ('<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:1;'
            'width:78px;height:78px;border-radius:50%;background:rgba(10,10,10,.82);color:#E6FF3D;'
            'display:flex;align-items:center;justify-content:center;font-size:30px;pointer-events:none">&#9654;</div>')
    frame = ('<iframe src="https://www.youtube.com/embed/' + vid + '" title="' + title + '" '
             'allow="accelerometer;autoplay;clipboard-write;encrypted-media;picture-in-picture" '
             'allowfullscreen style="position:absolute;inset:0;width:100%;height:100%;border:0;z-index:2"></iframe>')
    return f'<div style="position:relative;width:100%;height:100%;background:#000">{back}{play}{frame}</div>' 

def src_row(mark, label, url, note):
    return ('<div class="frow" style="margin-bottom:10px">'
            + logo(mark,40) +
            '<div class="bs" style="flex:1"><b>' + label + '</b> <span class="mut">' + note + '</span></div>'
            + link(url) + '</div>')

def link(url, label=None):
    """A clickable chip. The deck's click-to-advance handler ignores <a>, so these open cleanly."""
    return f'<a class="go" href="https://{url}" target="_blank" rel="noopener">{label or url}</a>'

def img(src, cls='photo'):
    return f'<img src="{src}" alt="">' if src else '<div class="bs mut">image missing</div>'


def viz_funnel_real():
    """A funnel with real ecom numbers. 100 arrive, 2-3 pay. The drop is the lesson."""
    bands = [(100, 'land on the site', '100', 0),
             (10, 'add to cart', '10', 0),
             (7, 'start checkout', '7', 0),
             (3, 'pay', '3', 1)]
    drops = [(90, 'leave without adding a single thing', 'the product page did not convince them'),
             (3, 'never reach checkout', 'shipping appears, or the cart is clumsy'),
             (4, 'abandon at checkout', '<b>39%</b> of them over extra costs')]
    out = []
    for i, (pct, label, num, win) in enumerate(bands):
        w = max(pct, 4.5)
        cls = 'fbar win' if win else 'fbar'
        out.append('<div class="frow"><div class="' + cls + '" style="width:' + str(w) + '%">'
                   + num + '</div><div class="bs" style="white-space:nowrap"><b>' + label + '</b></div></div>')
        if i < len(drops):
            n, what, why = drops[i]
            out.append('<div class="fdrop"><b class="n">&minus;' + str(n) + '</b>'
                       '<div class="bs"><b>' + what + '</b> <span class="mut">&mdash; ' + why + '</span></div></div>')
    return '<div style="width:100%">' + ''.join(out) + '</div>'


# ═════════════════ SESSION 1 — THE BASICS ═════════════════
S1=[
slide(
 cell(1,10,1,7,'<div class="l mut">Session One</div>'
   '<div class="d mt">How a shop<br>makes<br><em>money</em></div>','ink')
 +cell(10,13,1,7,'<div class="l">Joy<br>CS &rarr; AM</div>'
   '<div class="ch mt2">The<br>basics</div>','lemon')
 +cell(1,13,7,9,'<div class="st">A shop is a business, not a website.</div>'
   '<div class="b mt mut">Two hours. No app. No Joy. One real brand, broken down together.</div>'),
 'Goal: a shop is a business, not a website. Today is arithmetic on real things. We break down one real brand together as we go, and you break down another at the end.'),

slide(
 cell(1,8,1,6,'<div class="l mut">Question one</div>'
   '<div class="t mt">You can buy<br>this shirt for<br><em>$30</em>.</div>'
   '<div class="st mt2">What do you sell it for?</div>')
 +cell(8,13,1,4,'<div class="c3">Write every answer up</div>'
   '<div class="bs mt">$45? $60? $90? Nobody is wrong yet. They are all guesses about the same thing: '
   '<b>how much does it cost to run a business?</b></div>')
 +cell(8,13,4,6,'<div class="c3">Then ask the second one</div>'
   '<div class="bs mt">&ldquo;How much of that do you <b>keep</b>?&rdquo; Almost everyone says half.</div>','lemon')
 +cell(1,13,6,9,'<div class="ch">By the end of today you will know why <em>half</em> is wildly wrong.</div>','ink'),
 'Shout it out. Write every answer on the board and judge none of them. Someone will say sixty. Keep them up there — you come back to them at the end.',
 kicker='Ask the room', num='02'),

slide(
 cell(1,8,1,6,'<div class="l mut">Start with something you have held</div>'
   '<div class="t mt">One<br>$100<br>shoe</div>'
   '<div class="b mt2">Where does the hundred dollars <b>actually go</b>?</div>'
   '<div class="bs mt mut">Nguồn: Brands Vietnam · Trí Thức Trẻ<br>Từ báo cáo tài chính Nike &amp; adidas 2015</div>')
 +cell(8,13,1,6,img(SNEAKER),'contain')
 +cell(1,13,6,9,'<div class="ls mut mb">adidas &middot; one pair &middot; US retail</div>'
   +stack([(21,'$21','make it',0),(5,'$5','ship',0),(8,'$8','marketing',0),
           (13,'$13','staff &amp; the rest',0),(1,'$1','tax',0),(2,'$2','profit',2),
           (50,'$50','the shop that sells it',1)])
   +'<div class="b mt"><b>adidas keeps $2.</b> The shop that sold it keeps about <b>$6</b>.</div>'),
 'Ask first: a hundred dollar shoe — how much do you think adidas makes? Let them guess. They will say forty, fifty. Then show it. Twenty-one dollars to make. Fifty goes to the shop. And after shipping, marketing, staff and tax, adidas keeps TWO DOLLARS. Nobody expects it.',
 kicker='Real numbers', num='03'),

slide(
 cell(1,7,1,9,f'<div class="l mut">{logo("nike",34)}Nike</div><div class="n-sm mt">$5</div>'
   '<div class="ls mut">kept &middot; 5.3% net margin</div><div class="rule"></div>'
   '<table><tr><td>make it</td><td class="r">$22</td></tr>'
   '<tr><td>ship, insure, customs</td><td class="r">$5</td></tr>'
   '<tr><td>marketing</td><td class="r">$5</td></tr>'
   '<tr><td>staff &amp; everything else</td><td class="r">$11</td></tr>'
   '<tr><td>tax</td><td class="r">$2</td></tr>'
   '<tr><td>the shop</td><td class="r">$50</td></tr></table>')
 +cell(7,13,1,9,f'<div class="l">{logo("adidas",34)}adidas</div><div class="n-sm mt">$2</div>'
   '<div class="ls">kept &middot; 2.5% net margin</div><div class="rule"></div>'
   '<table><tr><td>make it</td><td class="r">$21</td></tr>'
   '<tr><td>ship, insure, customs</td><td class="r">$5</td></tr>'
   '<tr><td><b>marketing</b></td><td class="r"><b>$8</b></td></tr>'
   '<tr><td><b>staff &amp; everything else</b></td><td class="r"><b>$13</b></td></tr>'
   '<tr><td>tax</td><td class="r">$1</td></tr>'
   '<tr><td>the shop</td><td class="r">$50</td></tr></table>','ink'),
 'The difference is almost entirely marketing — adidas spends eight where Nike spends five, and it comes straight out of the profit. This is a real business decision you can read in the numbers.',
 kicker='Same shoe, same $100', num='04'),

slide(
 cell(1,13,1,5,'<div class="d">$100 in.<br><em>$8</em> of profit out.</div>'
   '<div class="st mt mut">Split between two companies.</div>')
 +cell(1,8,5,9,'<div class="t">So where did the other <em>$92</em> go?</div>','lemon')
 +cell(8,13,5,9,'<div class="bs">Making it. Moving it. Marketing it. Selling it.</div>'
   '<div class="b mt2">Nobody in this chain is getting rich. That is why merchants care so much about margin, '
   'and why they flinch at a discount you think is small.</div>','ink'),
 'It is not greed. There is almost nothing there to give away. Let them sit with it before you move on.',
 kicker='Ask the room', num='05'),

slide(
 cell(1,13,1,3,'<div class="l mut">Two laws to remember</div>'
   '<div class="st mt">The further a product travels from the factory,<br>the <em>more mouths</em> it has to feed.</div>')
 +cell(1,13,3,5,'<div class="st">A discount does not eat the profit.<br>It eats <em>the layer paying for everything else.</em></div>')
 +cell(1,13,5,9,'<div class="ch lem">Do the arithmetic on that second one</div>'
   '<div class="b mt">adidas keeps <b>$2</b> on a $100 shoe.</div>'
   '<div class="b">A <b>10% discount</b> is <b>$10</b>.</div>'
   '<div class="ch mt2">That does not shrink the profit. It <em>erases it five times over.</em></div>'
   '<div class="bs mt mut">Every time a merchant flinches at a discount, this is the number in their head.</div>','ink'),
 'This is the single most useful thing in session one. It explains almost every discount conversation you will ever have with a merchant.',
 num='06'),

slide(
 cell(1,13,1,3,'<div class="l mut">Which is why DTC exists</div>'
   '<div class="t mt">Delete the layers.</div>')
 +cell(1,3,3,6,'<div class="c3">factory</div>','lemon')
 +cell(3,5,3,6,'<div class="c3">brand</div>','lemon')
 +cell(5,7,3,6,'<div class="c3 mut" style="text-decoration:line-through">distributor</div>')
 +cell(7,9,3,6,'<div class="c3 mut" style="text-decoration:line-through">shop</div>')
 +cell(9,13,3,6,'<div class="c3">you</div>','lemon')
 +cell(1,13,6,9,'<div class="st">They deleted the shop &mdash; and bought <em>an ad</em> instead.</div>'
   '<div class="b mt2 mut">A shop was a fixed cost. An ad is a cost you pay again for <b>every single customer.</b> '
   'That is the whole game, and it is why the second order matters so much.</div>','ink'),
 'Sell straight to the person, keep the layers. That is why a DTC brand can charge less and still keep more. But nothing is free.',
 num='07'),

slide(
 cell(1,7,1,6,'<div class="l mut">Watch together &middot; 90 seconds</div>'
   '<div class="t mt">Dollar<br>Shave<br>Club</div>'
   '<div class="b mt2">March 2012. The video that built a billion-dollar company.</div>')
 +cell(7,13,1,6,video('RBHMf7BNd8o','Dollar Shave Club 2012',DSCTHUMB),'photo')
 +cell(1,5,6,9,'<div class="n-sm">$4,500</div><div class="ls mut">shot in one day</div>')
 +cell(5,9,6,9,'<div class="n-sm">12,000</div><div class="ls mut">orders in 48 hours &middot; servers fell over</div>','lemon')
 +cell(9,13,6,9,'<div class="n-sm">$1B</div><div class="ls">sold to Unilever, 2016</div>','ink'),
 'Watch it, then ask: what did they actually delete? The supermarket shelf. And what replaced it — subscription replaced remembering to buy, referral replaced the shelf. Their innovation was the price structure, not the razor. Then show the store as it is today: still a subscription, still a starter set at $4.99.',
 kicker='youtube.com/watch?v=RBHMf7BNd8o', num='08'),

slide(
 cell(1,13,1,4,'<div class="l mut">Today&rsquo;s brand &middot; breakdown 1</div>'
   '<div class="t mt">On the screen.<br>Together.</div>')
 +cell(1,13,4,7,'<div class="st">What does it sell &mdash; and what do you think it <em>costs them to make?</em></div>','lemon')
 +cell(1,13,7,9,'<div class="b">Fill it on the sheet as we go. This is the same sheet you use alone in forty minutes.</div>','ink'),
 'Open the real site. Find the hero product and its price. Guess the cost to make it out loud, as a room. You will be roughly right — and being roughly right is the whole skill.',
 kicker='Open it live', num='09'),
]

S1 += [
slide(
 cell(1,6,1,9,'<div class="l mut">Whiteboard</div>'
   '<div class="t mt">Back to<br>your<br>shirt.</div>'
   '<div class="st mt2">$30 &rarr; you said <em>$60</em>.</div>'
   '<div class="b mt2 mut">Build it live, one line at a time. Do not show them the total.</div>')
 +cell(6,13,1,9,'<div class="ls mut mb">Order one</div>'
   '<table><tr><td>Sticker price</td><td class="r">$60.00</td></tr>'
   '<tr><td>15% off &mdash; a stranger needs a reason</td><td class="r">&minus;$9.00</td></tr>'
   '<tr><td class="mut">collected</td><td class="r mut">$51.00</td></tr>'
   '<tr><td>The shirt</td><td class="r">&minus;$30.00</td></tr>'
   '<tr><td>Shipping</td><td class="r">&minus;$6.00</td></tr>'
   '<tr><td>Processing</td><td class="r">&minus;$1.78</td></tr>'
   '<tr><td>Ads, to make this person show up</td><td class="r">&minus;$15.00</td></tr>'
   '<tr class="tot"><td>Kept</td><td class="r">&minus;$1.78</td></tr></table>','ink'),
 'You sold a shirt and you are down one dollar seventy-eight. Do not rush this — the room has to feel the sixty dollars disappear.',
 kicker='Build it live', num='10'),

slide(
 cell(1,13,1,4,'<div class="l mut">And nothing else is paid yet</div>'
   '<div class="t mt">Shopify plan &middot; apps &middot; salary &middot; rent &middot; tax</div>')
 +cell(1,7,4,9,'<div class="n-lg">&minus;$8</div>'
   '<div class="st mt">the honest number<br>on a $60 sale</div>','lemon')
 +cell(7,13,4,9,'<div class="b">The app stack alone is often <b>~10% of revenue</b> at this size.</div>'
   '<div class="ch mt2">So the shop did not make a thin profit.</div>'
   '<div class="ch mt lem">It lost money.</div>','ink'),
 'Stop here. Let it sit. Do not rescue them.',
 num='11'),

slide(
 cell(1,13,1,4,'<div class="d">So why would anybody<br><em>run this business?</em></div>')
 +cell(1,9,4,9,'<div class="c3 mut">Answers you will hear</div><div class="rule"></div>'
   '<div class="b mb">&ldquo;Sell more of them.&rdquo; <span class="mut">&mdash; volume does not help; every unit loses the same.</span></div>'
   '<div class="b mb">&ldquo;Raise the price.&rdquo; <span class="mut">&mdash; fewer people buy, and the ad costs more per sale.</span></div>'
   '<div class="b">&ldquo;Spend less on ads.&rdquo; <span class="mut">&mdash; then nobody arrives at all.</span></div>')
 +cell(9,13,4,9,'<div class="c3">The only answer that works</div>'
   '<div class="ch mt2">Sell to the <b>same person again</b>, when finding her costs <b>nothing</b>.</div>','lemon'),
 'Say nothing at first. Wait. They will offer volume, price and cheaper ads — let each one die on its own before you reveal the last panel.',
 kicker='Ask the room', num='12'),

slide(
 cell(1,13,1,3,'<div class="l mut">Order 2 &middot; same customer, eight weeks later</div>'
   '<div class="t mt">No ad. No first-order discount.</div>')
 +cell(1,7,3,6,'<div class="ls mut">Order 1</div>'
   '<div class="bar mt" style="width:22%;background:var(--ink);color:var(--paper)">&minus;$2</div>'
   '<div class="bs mt mut">paid for the ad. nothing else.</div>')
 +cell(7,13,3,6,'<div class="ls mut">Order 2</div>'
   '<div class="bar mt" style="background:var(--lemon)">+$22</div>'
   '<div class="bs mt mut">she came back on her own.</div>')
 +cell(1,13,6,9,'<div class="t">The business is not the shirt.<br>It is the <em>second shirt.</em></div>','ink'),
 'Same shirt, same price. Twenty-two dollars instead of minus two. The only difference is nobody had to pay to find her. Tell them to write this down — everything for the next four weeks comes back to it.',
 num='13'),

slide(
 cell(1,13,1,3,'<div class="l mut">So how much are you allowed to spend?</div>'
   '<div class="t mt">How long she stays decides<br>what you may <em>pay to get her.</em></div>')
 +cell(1,13,3,5,'<div class="ls mut mb">If she buys once</div>'
   '<div class="bar" style="width:23%;background:var(--paper)">$13.22</div>')
 +cell(1,13,5,7,'<div class="ls mut mb">If she buys three times</div>'
   '<div class="bar" style="background:var(--lemon)">$57 &mdash; now you can spend $30&ndash;40 and still win</div>')
 +cell(1,13,7,9,'<div class="b">Same product. Same ad. Same market. The brand that gets a second order '
   '<b>can outspend the brand that does not</b> &mdash; and eventually starves it out of the auction.</div>','ink'),
 'This is why retention is not a nice-to-have. It is how you afford to compete at all. It also explains why merchants chase AOV so hard — a fatter order raises the same ceiling.',
 num='14'),

slide(
 cell(1,13,1,2,'<div class="st">Not every product is the same business</div>')
 +cell(1,7,2,6,'<div class="l mut">Bought once</div>'
   '<div class="ch mt">mattress &middot; cookware &middot; luggage</div>'
   '<div class="rule"></div>'
   '<div class="b">One shot. So <b>squeeze order 1</b> &mdash; bundles, upsells, warranty, a free gift.</div>'
   '<div class="b mt">Growth comes from <b>new people</b>: referral, new products.</div>')
 +cell(7,13,2,6,'<div class="l">Bought again</div>'
   '<div class="ch mt">soap &middot; shampoo &middot; razors &middot; skincare</div>'
   '<div class="rule"></div>'
   '<div class="b">Many shots. Order 1 only has to <b>cover itself</b>.</div>'
   '<div class="b mt">The money is in orders 2, 3 and 4.</div>','lemon')
 +cell(1,13,6,9,'<div class="st">One question &mdash; <em>bought once, or bought again?</em> &mdash; '
   'predicts most of what a merchant does.</div>'
   '<div class="b mt mut">Including whether they need us at all. Session four is built on this.</div>','ink'),
 'Ask the room which one Halfdays is. Hold onto this — it comes back as the whole of session four.',
 num='15'),

slide(
 cell(1,13,1,2,'<div class="l mut">And every shop is these six boxes</div>')
 +cell(1,5,2,5,'<div class="c3">Get people in</div><div class="bs mt mut">ads, email, they remember you</div>')
 +cell(5,9,2,5,'<div class="c3">On the site</div><div class="bs mt mut">home, product, cart, popup</div>')
 +cell(9,13,2,5,'<div class="c3">Pay</div><div class="bs mt mut">checkout, discount, shipping</div>')
 +cell(1,5,5,8,'<div class="c3">After the order</div><div class="bs mt mut">email, where is my order, refund</div>')
 +cell(5,9,5,8,'<div class="c3">Come back</div><div class="bs mt">refill, drop, membership</div>','lemon')
 +cell(9,13,5,8,'<div class="c3">Money</div><div class="bs mt">order 1 cost them. order 2 is the win</div>','lemon')
 +cell(1,13,8,9,'<div class="b">Every merchant message you will ever read is about <b>one box.</b></div>','ink'),
 'Your map for next week. We live in COME BACK — but you cannot help someone there if you do not know the other five exist.',
 num='16'),

slide(
 cell(1,13,1,2,'<div class="t">Your two fears, as <em>arithmetic</em></div>')
 +cell(1,7,2,7,'<div class="n-sm">01</div><div class="ch mt">They vanish</div>'
   '<div class="rule"></div>'
   '<div class="b">I keep buying new people who never come back &mdash; only ever booking the first table.</div>')
 +cell(7,13,2,7,'<div class="n-sm">02</div><div class="ch mt">I discount the wrong people</div>'
   '<div class="rule"></div>'
   '<div class="b">The $9 handed to someone already buying. And adidas only keeps $2.</div>','ink')
 +cell(1,13,7,9,'<div class="st">These are not feelings. They are the two pictures you just built.</div>','lemon'),
 'When a merchant sounds scared, it is one of these two. Every single time.',
 num='17'),

slide(
 cell(1,8,1,9,'<div class="l mut">Now you &middot; 50 minutes</div>'
   '<div class="t mt">A brand you have <em>not</em> seen today.</div>'
   '<div class="rule"></div>'
   '<ul><li class="b">Pairs. Teardown sheet <b>&sect;0&ndash;1</b></li>'
   '<li class="b">Same questions we just did together</li>'
   '<li class="b">Every pair reports back</li></ul>')
 +cell(8,13,1,5,'<div class="ch">At that margin, how many orders before they are <em>ahead?</em></div>','lemon')
 +cell(8,13,5,9,'<div class="c3 lem">Homework</div>'
   '<div class="bs mt">&sect;0&ndash;1 on two more brands. Classify each bought-once or bought-again.</div>'
   '<div class="bs mt">And: what does one order cost <b>your</b> store?</div>','ink'),
 'The reporting-out is where the learning lands. Every pair, no exceptions, even if they are wrong.',
 kicker='They do it', num='18'),
]



def TITLE(n, kicker, big, sub, tag):
    return slide(
     cell(1,10,1,7,f'<div class="l mut">{kicker}</div><div class="d mt">{big}</div>','ink')
     +cell(10,13,1,7,'<div class="l">Joy<br>CS &rarr; AM</div>'+f'<div class="ch mt2">{tag}</div>','lemon')
     +cell(1,13,7,9,f'<div class="st">{sub[0]}</div><div class="b mt mut">{sub[1]}</div>'), n)

def WN(q, yt, yb, nt, nb, note, num=None, kicker=None):
    return slide(
     cell(1,13,1,3,f'<div class="t">{q}</div>')
     +cell(1,7,3,9,f'<div class="l">Why</div><div class="ch mt">{yt}</div><div class="rule"></div>'
                   f'<div class="b">{yb}</div>','lemon')
     +cell(7,13,3,9,f'<div class="l lem">Why not</div><div class="ch mt">{nt}</div><div class="rule"></div>'
                    f'<div class="b">{nb}</div>','ink'), note, kicker=kicker, num=num)

def BRANDBEAT(n, q, note, num, brand='', url=''):
    chips = ''.join(link(u.strip()) for u in url.split('&middot;')) if url else ''
    head = (f'<div class="t mt">{brand}</div><div class="mt">{chips}</div>'
            if brand else '<div class="t mt">On the screen.<br>Together.</div>')
    return slide(
     cell(1,13,1,4,f'<div class="l mut">Today&rsquo;s brand &middot; breakdown {n}</div>'+head)
     +cell(1,13,4,7,f'<div class="st">{q}</div>','lemon')
     +cell(1,13,7,9,'<div class="b">Fill it on the sheet as we go. This is the same sheet you use alone in forty minutes.</div>','ink'),
     note, kicker='Open it live', num=num)

# ── session 1: live store examples, clickable ──
_STORES = [
slide(
 cell(1,13,1,2,'<div class="l mut">Open all four. Same rule, four different numbers.</div>'
   '<div class="t mt">Why is free shipping <em>$30</em> here and <em>$95</em> there?</div>')
 +cell(1,4,2,6,f'{logo("raewellness",34)}'+'<div class="c3" style="display:inline">Rae Wellness</div><div class="n-sm mt">$30</div>'
   '<div class="bs mut">supplements, $19.99&ndash;$30</div><div class="mt">'+link('raewellness.co')+'</div>')
 +cell(4,7,2,6,f'{logo("crownaffair",34)}'+'<div class="c3" style="display:inline">Crown Affair</div><div class="n-sm mt">$75</div>'
   '<div class="bs mut">haircare, mid-price</div><div class="mt">'+link('crownaffair.com')+'</div>','lemon')
 +cell(7,10,2,6,f'{logo("halfdays",34)}'+'<div class="c3" style="display:inline">Halfdays</div><div class="n-sm mt">$95</div>'
   '<div class="bs mut">outerwear</div><div class="mt">'+link('halfdays.com')+'</div>')
 +cell(10,13,2,6,f'{logo("hexclad",34)}'+'<div class="c3" style="display:inline">HexClad</div><div class="n-sm mt">free</div>'
   '<div class="bs mut">$100+ pans</div><div class="mt">'+link('hexclad.com')+'</div>','ink')
 +cell(1,13,6,9,'<div class="st">Each number sits <em>just above</em> where that shop&rsquo;s average order '
   'already lands.</div>'
   '<div class="b mt mut">It is not a guess and it is not copied. It is the one lever that raises the basket '
   'without touching the price &mdash; and you can read it off four sites in two minutes.</div>','ink'),
 'Open all four in tabs before the session. Let the room guess the reason before you tell them. This is the first time they see a business decision they can read from the outside, and it is a good one to start with because the answer is clean.',
 kicker='Open them live'),

slide(
 cell(1,13,1,2,'<div class="l mut">Bought once, or bought again? Go and decide.</div>')
 +cell(1,7,2,6,'<div class="c3">Open these</div><div class="rule"></div>'
   '<div>'+link('hexclad.com','hexclad.com')+link('halfdays.com','halfdays.com')+'</div>'
   '<div>'+link('raewellness.co','raewellness.co')+link('crownaffair.com','crownaffair.com')+'</div>'
   '<div class="bs mt2 mut">For each: does it run out? wear out? is there a next size, next drop, next flavour?</div>')
 +cell(7,13,2,6,'<div class="c3 lem">Then predict the stack</div>'
   '<div class="bs mt">Bought once &rarr; expect <b>bundles and upsells</b>.</div>'
   '<div class="bs mt">Bought again &rarr; expect <b>subscription and email</b>.</div>'
   '<div class="bs mt2">Say it out loud <b>before</b> you look at the source.</div>','ink')
 +cell(1,13,6,9,'<div class="st">Then look. <em>Were you right?</em></div>'
   '<div class="b mt mut">This is the whole skill in one exercise: read the product, predict the business, '
   'check yourself. Being roughly right, fast, beats being precisely right, slowly.</div>','lemon'),
 'Do this live in tabs. It is the first time they make a prediction and get graded by reality in the same minute, which is where the confidence comes from.',
 kicker='Open them live'),

slide(
 cell(1,7,1,5,'<div class="l mut">And the one they all learn from</div>'
   '<div class="t mt">Dollar Shave Club, <em>today</em></div>'
   '<div class="b mt2">Fourteen years after the video. Still a subscription. Still a starter set.</div>'
   '<div class="mt">'+link('dollarshaveclub.com')+'</div>')
 +cell(7,13,1,5,'<div class="c3">Look for</div><div class="rule"></div>'
   '<div class="bs">the <b>$4.99 starter set</b> &mdash; a cheap first order on purpose</div>'
   '<div class="bs mt">how fast they push you to <b>subscribe</b></div>'
   '<div class="bs mt">how little the razor itself is discussed</div>','lemon')
 +cell(1,13,5,9,'<div class="st">They still sell the <em>second order</em>, not the first.</div>'
   '<div class="b mt mut">The cheap starter set is not generosity. It is the order-1 table from earlier: '
   'lose a little to win the customer, then make the money on every box after. '
   'You are looking at the arithmetic we just did on a whiteboard, running in public.</div>','ink'),
 'Close the money half here. The video showed them the idea; the live site shows them it still runs. Ask the room to find where the site pushes subscription — it is everywhere once you look.',
 kicker='Open it live'),
]

# ── session 1 drill: timeboxed, with a worked target ──
_DRILL1 = [
slide(
 cell(1,13,1,2,'<div class="l mut">Now you &middot; 45 minutes, in pairs</div>'
   '<div class="t mt">A brand you have <em>not</em> seen today.</div>')
 +cell(1,13,2,3,'<div class="frow"><div class="fbar" style="width:110px">3 min</div>'
   '<div class="bs"><b>Get your brand.</b> <span class="mut">One per pair, handed to you. Open it on your phone.</span></div></div>','flat')
 +cell(1,13,3,4,'<div class="frow"><div class="fbar" style="width:110px">12 min</div>'
   '<div class="bs"><b>Sheet &sect;0</b> <span class="mut">&mdash; what they sell, the hero product, its price, who buys it.</span></div></div>','flat')
 +cell(1,13,4,5,'<div class="frow"><div class="fbar win" style="width:110px">17 min</div>'
   '<div class="bs"><b>Sheet &sect;1 &mdash; the money on one unit.</b> '
   '<span class="mut">The hard part. Guess the cost to make. Take out shipping, fees, a discount, the ad.</span></div></div>','flat')
 +cell(1,13,5,6,'<div class="frow"><div class="fbar" style="width:110px">8 min</div>'
   '<div class="bs"><b>Write your answer</b> <span class="mut">to the question below. One number, one sentence.</span></div></div>','flat')
 +cell(1,13,6,7,'<div class="frow"><div class="fbar" style="width:110px">5 min</div>'
   '<div class="bs"><b>Swap sheets</b> <span class="mut">with the pair next to you. Mark theirs. Do you believe their number?</span></div></div>','flat')
 +cell(1,13,7,9,'<div class="st">At that margin, <em>how many orders</em> before they are ahead?</div>'
   '<div class="b mt mut">Every pair answers that out loud. Sixty seconds each. One number, one sentence &mdash; '
   'not a tour of the website.</div>','ink'),
 'Read the timings out and put them on the board. Without a clock a pair finishes section zero in eight minutes and then drifts. The swap at the end is not filler — marking somebody else forces them to decide what a good answer looks like.',
 kicker='They do it'),

slide(
 cell(1,13,1,2,'<div class="l mut">What a good one looks like &mdash; so you have a target</div>'
   '<div class="st mt">Rae Wellness &middot; a $25 daily supplement</div>')
 +cell(1,7,2,8,'<table style="font-size:24px">'
   '<tr><td>They charge</td><td class="r">$25.00</td></tr>'
   '<tr><td>Guess: cost to make <span class="mut">(powder, capsule, jar, label)</span></td><td class="r">&minus;$7.00</td></tr>'
   '<tr><td>Free shipping over $30, so they eat it</td><td class="r">&minus;$5.00</td></tr>'
   '<tr><td>Processing</td><td class="r">&minus;$1.03</td></tr>'
   '<tr><td class="mut">before any advertising</td><td class="r mut">$11.97</td></tr>'
   '<tr class="tot"><td>Say they pay $15 to find her</td><td class="r">&minus;$3.03</td></tr></table>')
 +cell(7,13,2,5,'<div class="c3 lem">The answer</div>'
   '<div class="b mt">&ldquo;They lose about three dollars on the first order. '
   'They need <b>two</b> before they are ahead &mdash; and it is a supplement, so a second order is realistic.&rdquo;</div>','ink')
 +cell(7,13,5,8,'<div class="c3">Why this is good</div>'
   '<div class="bs mt">Every number is a <b>guess</b>. None of them are researched. '
   'And it still produces a real answer somebody could act on.</div>')
 +cell(1,13,8,9,'<div class="c3">Nobody looked up a cost. <em>Guess, do not research.</em> '
   'Roughly right and fast beats precisely right and late.</div>','lemon'),
 'Put this up before they start and leave it up. Without a target they will either write one line or try to research real COGS and burn the whole session. The point of the slide is permission to guess.'),
]

def _step(t, bold, rest, win=0):
    cls = 'fbar win' if win else 'fbar'
    return ('<div class="frow"><div class="' + cls + '" style="width:110px">' + t + '</div>'
            '<div class="bs"><b>' + bold + '</b> <span class="mut">' + rest + '</span></div></div>')

# ── SESSION 2 drill ──
_DRILL2 = [
slide(
 cell(1,13,1,2,'<div class="l mut">Now you &middot; 45 minutes, in pairs</div>'
   '<div class="t mt">Diagnose a shop you have <em>not</em> seen.</div>')
 +cell(1,13,2,3,_step('3 min','Get your brand.','One per pair. Open it on a phone, cart empty, not logged in.'),'flat')
 +cell(1,13,3,4,_step('12 min','Walk it as a customer.','Ad or social &rarr; product &rarr; cart &rarr; checkout. Where would <b>you</b> quit?'),'flat')
 +cell(1,13,4,5,_step('10 min','Read the stack.','View source, Ctrl-F. Then /pages/rewards. What are they paying to fix?'),'flat')
 +cell(1,13,5,6,_step('12 min','List every problem you found.','All of them. Messy is fine. Do not rank yet.','1'),'flat')
 +cell(1,13,6,7,_step('8 min','Rank your top three.','And next to each: <b>what would it cost to fix?</b>'),'flat')
 +cell(1,13,7,9,'<div class="st">Three problems, ranked, with the cost of each.</div>'
   '<div class="b mt mut">If loyalty is not in your top three, <b>say so</b>. That is a correct answer and '
   'we would rather hear it here than from the merchant in six months.</div>','ink'),
 'Separating "list everything" from "rank them" matters. If they rank as they go they stop at the first thing they recognise. Make them dump first.',
 kicker='They do it'),

slide(
 cell(1,13,1,2,'<div class="l mut">What a good one looks like &mdash; Halfdays, which you already know</div>')
 +cell(1,13,2,3,'<div class="frow"><div class="fbar" style="width:64px">1</div>'
   '<div class="bs"><b>A 10% popup on premium outerwear.</b> '
   '<span class="mut">Free to change. Are they discounting people who were buying a $300 jacket anyway? Fear #2.</span></div></div>','flat')
 +cell(1,13,3,4,'<div class="frow"><div class="fbar" style="width:64px">2</div>'
   '<div class="bs"><b>Past buyers may never see the next drop.</b> '
   '<span class="mut">Cheap. Apparel repeats by season, not refill &mdash; so new arrivals to past purchasers is the lever.</span></div></div>','flat')
 +cell(1,13,4,5,'<div class="frow"><div class="fbar win" style="width:64px">3</div>'
   '<div class="bs"><b>Nothing gives a reason to choose them next season.</b> '
   '<span class="mut">Slowest and last. This is ours &mdash; and it is third, not first.</span></div></div>','flat')
 +cell(1,7,5,9,'<div class="c3">Why this is good</div><div class="rule"></div>'
   '<div class="b">Three problems, ordered by <b>people lost</b> and <b>cost to fix</b>. '
   'Two of them we do not sell. That is what makes the third one credible.</div>')
 +cell(7,13,5,9,'<div class="c3 lem">What a weak one looks like</div><div class="rule"></div>'
   '<div class="b">&ldquo;They should add a loyalty program.&rdquo;</div>'
   '<div class="bs mt2 mut">One item, unranked, no cost, and it happens to be the thing we sell. '
   'That is a pitch, not a diagnosis.</div>','ink'),
 'The weak example is the important half. Everyone can produce the weak version. Show them the difference explicitly or they will hand you the pitch and think it is a diagnosis.'),
]

# ── SESSION 3 drill ──
_DRILL3 = [
slide(
 cell(1,13,1,2,'<div class="l mut">Now you &middot; 45 minutes, in pairs</div>'
   '<div class="t mt">Two brands. One <em>recommendation</em> each.</div>')
 +cell(1,13,2,3,_step('3 min','Get your two brands.','One with a strong repeat reason, one with a weak one. Handed to you.'),'flat')
 +cell(1,13,3,4,_step('10 min','Brand A.','Why would a human buy this twice? What does the brand already do about it?'),'flat')
 +cell(1,13,4,5,_step('10 min','Brand B.','Same two questions. &ldquo;No reason&rdquo; is an allowed answer &mdash; and often the right one.'),'flat')
 +cell(1,13,5,6,_step('12 min','Prescribe one thing each.','Referral, points, credit, tiers, subscription &mdash; or <b>nothing yet</b>.','1'),'flat')
 +cell(1,13,6,7,_step('10 min','Name what you rejected.','And what that option would have lost. <b>This is the graded part.</b>'),'flat')
 +cell(1,13,7,9,'<div class="st">Anyone can pick something. Only somebody who understands it can say '
   '<em>what the alternative costs.</em></div>','ink'),
 'The rejected option is the whole grading criterion. Say that before they start, or they will spend forty minutes on the recommendation and thirty seconds on the part you are actually marking.',
 kicker='They do it'),

slide(
 cell(1,13,1,2,'<div class="l mut">What a good one looks like &mdash; both brands from earlier</div>')
 +cell(1,7,2,6,'<div class="c3">Crown Affair</div><div class="rule"></div>'
   '<div class="bs mut">refill product, no loyalty, Recharge already installed</div>'
   '<div class="b mt2"><b>Points, tied to the refill window.</b></div>'
   '<div class="bs mt2"><b>Rejected: store credit.</b> It would be understood faster &mdash; but credit is '
   'money with a logo on it. They have spent years building a brand; points can carry it, credit cannot.</div>','lemon')
 +cell(7,13,2,6,'<div class="c3">HexClad</div><div class="rule"></div>'
   '<div class="bs mut">$300 pan, five-year cycle, already runs Rivo</div>'
   '<div class="b mt2"><b>Referral and range &mdash; not a refill points scheme.</b></div>'
   '<div class="bs mt2"><b>Rejected: points on a repurchase cycle.</b> They would expire before she needs '
   'another pan. You would have added a cost and produced no second order.</div>','ink')
 +cell(1,13,6,9,'<div class="st">Both name the rejected option <em>and</em> what it loses.</div>'
   '<div class="b mt mut">Notice the second one recommends something we do not really sell. '
   'That is not a failure of the exercise &mdash; it is the exercise.</div>'),
 'Point at the HexClad half explicitly. If nobody in the room ever recommends something outside our product, they have not understood the job.'),
]

# ── SESSION 4 drill ──
_DRILL4 = [
slide(
 cell(1,13,1,2,'<div class="l mut">Now you &middot; 45 minutes, in pairs</div>'
   '<div class="t mt">Two brands. One <em>verdict</em> each.</div>')
 +cell(1,13,2,3,_step('3 min','Get your two brands.','One should pass and one should fail. You are not told which.'),'flat')
 +cell(1,13,3,4,_step('12 min','Run the checklist on both.','Line by line, out loud. Everything is visible from the public site.'),'flat')
 +cell(1,13,4,5,_step('10 min','Ask the harder question.','Do they need it <b>at all</b>? Base, stage &mdash; and check the one-star reviews.'),'flat')
 +cell(1,13,5,6,_step('12 min','Write the verdict.','Ours / not ours / not yet &mdash; plus <b>the one thing you would change</b>.','1'),'flat')
 +cell(1,13,6,7,_step('8 min','Defend it to another pair.','They try to talk you out of it. Change your mind if they are right.'),'flat')
 +cell(1,13,7,9,'<div class="st">Is it ours &middot; does it need this &middot; <em>what is the one thing we would change?</em></div>','ink'),
 'The defend-it step is what makes this a graduation drill rather than a worksheet. A verdict you cannot defend out loud is not a verdict.',
 kicker='They do it'),

slide(
 cell(1,13,1,2,'<div class="l mut">What a good one looks like</div>')
 +cell(1,7,2,7,'<div class="c3">Rae Wellness</div><div class="rule"></div>'
   '<div class="ch mt">Ours. <em>Now.</em></div>'
   '<div class="bs mt2">Shopify, wellness, repurchase, Klaviyo, Recharge heavily used, '
   '<b>/pages/rewards 404s</b>, no competitor.</div>'
   '<div class="bs mt2"><b>The one thing:</b> nothing gives a reason to choose them. Points on the refill '
   'window, surfaced in the Klaviyo flow they already run.</div>','lemon')
 +cell(7,13,2,7,'<div class="c3">HexClad</div><div class="rule"></div>'
   '<div class="ch mt">Not ours.</div>'
   '<div class="bs mt2"><b>Rivo is already installed.</b> Fails the checklist on the most visible line there is '
   '&mdash; found in sixty seconds, no opinion required.</div>'
   '<div class="bs mt2">And even without it: a $300 pan on a five-year cycle is the wrong shape for points. '
   'Two reasons, either one enough.</div>','ink')
 +cell(1,13,7,9,'<div class="st">A verdict is a <em>decision plus a reason a lead can check.</em></div>'
   '<div class="b mt mut">&ldquo;Feels like a good fit&rdquo; is not a verdict. '
   '&ldquo;Rivo is installed, here is the line in the source&rdquo; is.</div>'),
 'The last line is the standard. Anything that cannot be checked by somebody else in under a minute is an opinion, not a verdict.'),
]

# ── sources: every claim in the session, clickable ──
_SRC1 = slide(
 cell(1,13,1,2,'<div class="l mut">Where all of this came from</div>'
   '<div class="st mt">Check any of it. <em>None of it is mine.</em></div>')
 +cell(1,13,2,8,
   src_row('brandsvietnam','Bài toán chi phí — Nike &amp; adidas','brandsvietnam.com/12953-bai-toan-chi-phi-va-gia-thanh-tren-moi-doi-giay-nike-adidas','&mdash; the $100 shoe, from 2015 filings. In Vietnamese.')
  +src_row('youtube','Dollar Shave Club, the 2012 film','youtube.com/watch?v=RBHMf7BNd8o','&mdash; 90 seconds, $4,500, 12,000 orders in 48 hours')
  +src_row('dsc','Dollar Shave Club today','dollarshaveclub.com','&mdash; still a subscription, still a $4.99 starter set')
  +src_row('halfdays','Halfdays','halfdays.com','&mdash; free shipping $95')
  +src_row('crownaffair','Crown Affair','crownaffair.com','&mdash; free shipping $75')
  +src_row('raewellness','Rae Wellness','raewellness.co','&mdash; free shipping $30')
  +src_row('hexclad','HexClad','hexclad.com','&mdash; free shipping always, $100+ pans')
   ,'flat')
 +cell(1,13,8,9,'<div class="c3">Send this slide to the team. <em>Reading the source beats trusting the trainer.</em></div>','ink'),
 'Give them the links. A cohort whose problem was never English can read a Vietnamese source better than we can — and the shoe article is the single most persuasive thing in the session.',
 kicker='All clickable')

_SRC2 = slide(
 cell(1,13,1,2,'<div class="l mut">Where all of this came from</div>'
   '<div class="st mt">The whole diagnostic tree is <em>somebody else&rsquo;s work.</em></div>')
 +cell(1,7,2,7,'<div class="c3 mb">Watch this one</div>'
   +'<div style="height:74%;min-height:250px">'+video('42uhZYnyEXU','Chase Chappell — every ecom metric',CHASETHUMB)+'</div>'
   +'<div class="mt">'+link('youtube.com/watch?v=42uhZYnyEXU','open on YouTube')+'</div>'
   +'<div class="bs mt mut">44 min. Every metric, what it means, what to do. '
   'We use the <b>site and business</b> half; the ad-account half is not our altitude.</div>')
 +cell(7,13,2,7,
   src_row('baymard','Baymard Institute','baymard.com/lists/cart-abandonment-rate','&mdash; ~70% abandon, 39% over extra costs')
  +src_row('meta','Meta Ad Library','facebook.com/ads/library','&mdash; every live ad, any brand, free')
  +src_row('crownaffair','Crown Affair','crownaffair.com','&mdash; the ICP-matched winner')
  +src_row('hexclad','HexClad','hexclad.com','&mdash; the Plus store, and the 52% popup')
  +src_row('halfdays','Halfdays','halfdays.com','&mdash; the brand you diagnose')
   ,'flat')
 +cell(1,13,7,9,'<div class="c3">The stack map &mdash; 130 apps across 28 fields &mdash; is internal: '
   '<em>avada-know-the-drill</em>. Ask for access.</div>','ink'),
 'Play a minute of the Chase video if you have time — the site walkthrough around six minutes in is the clearest part. Otherwise just point at it and move on.',
 kicker='All clickable')

_SRC3 = slide(
 cell(1,13,1,2,'<div class="l mut">Where all of this came from</div>'
   '<div class="st mt">Two brands, one video, and your own inbox.</div>')
 +cell(1,7,2,7,'<div class="c3 mb">The retention half of the same video</div>'
   +'<div style="height:70%;min-height:230px">'+video('42uhZYnyEXU','Chase Chappell — retention diagnostics',CHASETHUMB)+'</div>'
   +'<div class="mt">'+link('youtube.com/watch?v=42uhZYnyEXU','open on YouTube')+'</div>'
   +'<div class="bs mt mut">The returning-rate trap and the three product types are from here.</div>')
 +cell(7,13,2,7,
   src_row('crownaffair','Crown Affair','crownaffair.com','&mdash; strong repeat, Recharge, no loyalty')
  +src_row('hexclad','HexClad','hexclad.com','&mdash; weak repeat, and runs Rivo anyway')
  +src_row('rivo2','Rivo case studies','rivo.io','&mdash; 19 studies, one number each, no feature lists')
  +src_row('klaviyo','Klaviyo','klaviyo.com','&mdash; the cheapest way to reach anyone')
  +src_row('attentive','Attentive','attentive.com','&mdash; SMS, ~100&times; the cost per message')
   ,'flat')
 +cell(1,13,7,9,'<div class="c3">And the best source in this session is <em>your own inbox</em> &mdash; '
   'the emails you got from your build-track order.</div>','ink'),
 'Point at the inbox line. Nothing on this list beats an email they received themselves about an order they placed.',
 kicker='All clickable')

_SRC4 = slide(
 cell(1,13,1,2,'<div class="l mut">Where all of this came from</div>'
   '<div class="st mt">The ICP is <em>ours</em>. Everything else is checkable.</div>')
 +cell(1,13,2,8,
   src_row('raewellness','Rae Wellness','raewellness.co','&mdash; Recharge + Klaviyo + /pages/rewards 404')
  +src_row('hexclad','HexClad','hexclad.com','&mdash; Rivo installed. Fails the checklist visibly.')
  +src_row('rivo2','Rivo &mdash; case studies','rivo.io','&mdash; 55&times; ROI banner, one hero number per card')
  +src_row('shopify','Shopify Plus signals','shopify.com/plus','&mdash; checkout extensions, markets, B2B')
  +src_row('recharge','Recharge','rechargepayments.com','&mdash; the subscription half of the easiest win')
  +src_row('klaviyo','Klaviyo','klaviyo.com','&mdash; the other half')
   ,'flat')
 +cell(1,13,8,9,'<div class="c3">Joy&rsquo;s ICP band and exclusions come from the outbound research &mdash; '
   '<em>Team Joy</em> in Obsidian. Ask for it.</div>','ink'),
 'The point of this slide is that nothing in the verdict rests on an opinion. Every line is somewhere they can go and look.',
 kicker='All clickable')

# ═════════════════ SESSION 2 — BREAK DOWN A BRAND ═════════════════
S2=[
TITLE('Goal: open a brand you have never seen and say what it is doing, and where it loses people. Today we do one together, slowly, then you do one alone.',
 'Session Two','Break<br>down<br><em>a brand</em>',
 ('The method. Phones out.','One sheet, any brand, no login. First time 45 minutes. By next month, fifteen.'),'The<br>method'),

slide(
 cell(1,8,1,5,'<div class="l mut">The rule</div>'
   '<div class="t mt">Outside-in.</div>'
   '<div class="b mt2">If you cannot see it on the <b>public site</b>, it is not on the sheet.</div>')
 +cell(8,13,1,5,'<div class="c3">Not needed</div><div class="rule"></div>'
   '<ul><li class="bs">an ad account</li><li class="bs">a merchant interview</li>'
   '<li class="bs">the Joy admin</li><li class="bs">their permission</li></ul>')
 +cell(1,13,5,9,'<div class="st">Everything you need is already <em>public.</em></div>'
   '<div class="b mt2 mut">That is not a limitation. It is the reason you can judge a merchant '
   'before the first call &mdash; and why an AM walks in already knowing something.</div>','ink'),
 'This is the skill the whole course exists to give you. Everything else is context for it.', num='02'),

slide(
 cell(1,7,1,6,'<div class="l mut">A shop</div>'
   '<div class="n-sm mt">Gone.</div><div class="rule"></div>'
   '<div class="b">She walks in. She browses. She leaves.</div>'
   '<div class="b mt">No name. No record. You will never know she was there.</div>')
 +cell(7,13,1,6,'<div class="l">Online</div>'
   '<div class="n-sm mt">A list.</div><div class="rule"></div>'
   '<div class="b">Came from that ad. Viewed it three times. Left at shipping.</div>'
   '<div class="b mt">And you can talk to her <b>tomorrow</b>.</div>','lemon')
 +cell(1,13,6,9,'<div class="st">That one difference is why the popup exists, why retargeting exists, '
   'and why <em>loyalty works at all.</em></div>'
   '<div class="b mt mut">A loyalty program is identity applied over time. In a shop you need a plastic card. '
   'Online it is just an account.</div>','ink'),
 'This is the difference between a shop and a website, and nearly every app in ecom exists because of it.', num='03'),

slide(
 cell(1,13,1,2,'<div class="l mut">The path you are looking for</div>'
   '<div class="st mt">Out of <em>100</em> people who land&hellip;</div>')
 +cell(1,9,2,9,viz_funnel_real())
 +cell(9,13,2,5,'<div class="ch">Nearly everyone leaves.</div>'
   '<div class="b mt2">A 2&ndash;3% conversion rate is <b>normal</b>, not broken. '
   'Ninety-seven people walking out is the <b>everyday condition</b> of every shop you will ever read.</div>','lemon')
 +cell(9,13,5,7,'<div class="c3">So the question is never</div>'
   '<div class="bs mt">&ldquo;why did they leave?&rdquo;</div>'
   '<div class="c3 mt2 lem">It is</div>'
   '<div class="bs mt"><b>&ldquo;which step lost the most, and is that step fixable?&rdquo;</b></div>','ink')
 +cell(9,13,7,9,'<div class="bs mut">Biggest single leak here</div>'
   '<div class="c3 mt">the product page &mdash; 90 of 100</div>')
 ,'Put the real numbers up before any theory. A hundred people arrive and two or three pay. When a merchant says conversion is bad, they usually mean it is 2% instead of 3% — and that half a percent is the whole argument. Ask the room where they would look first: the answer is the product page, because that is where 90 of the 100 went.',
 num='04'),

BRANDBEAT(1,'Where do they get their <em>people</em> from?',
 'Ad Library first — are they running ads, and what do the ads promise? Then: Instagram linked? A blog? A quiz? A popup? Name the main door out loud before moving on.','05','Halfdays','halfdays.com'),

slide(
 cell(1,8,1,5,'<div class="l mut">Click the ad. Land on the page.</div>'
   '<div class="t mt">Does the page <em>repeat the promise?</em></div>'
   '<div class="b mt2">Same photo? Same claim? Same price? Same offer?</div>')
 +cell(8,13,1,5,'<div>'+link('facebook.com/ads/library','Meta Ad Library')+'</div>'
   '<div class="b mt2">An ad is not a picture of a product. It is <b>an argument aimed at one person</b>: '
   'name her problem, prove it, make it urgent.</div>')
 +cell(1,13,5,9,'<div class="st">The most common way to waste $30 in this business:</div>'
   '<div class="ch mt2 lem">the ad promises one thing and the page says another.</div>'
   '<div class="b mt2 mut">She assumes she misread it, and leaves. Nobody ever tells the merchant.</div>','ink'),
 'Do this live with Halfdays. Find a real ad, click through, and judge the match as a room.',
 kicker='Open it live', num='06'),


WN('Should a shop run a popup?',
 'Yes &mdash; it buys her identity',
 'Not the sale &mdash; the <b>email</b>. Without it you cannot recover a cart, send a refill reminder, or retarget. '
 'Everything after this step depends on it.',
 'No &mdash; not like that',
 'Fires instantly, on mobile, before she has seen anything &mdash; she bounces. And the 10% goes to people '
 'who would have paid full price. <b>Fear #2 in the first thirty seconds.</b>',
 'A popup is not good or bad. Timing and offer decide which column it lands in. Trigger the Halfdays popup live and let the room judge which one it is.',
 num='07', kicker='Open it live'),

slide(
 cell(1,7,1,6,'<div class="l mut">The product page answers three silent questions</div>'
   '<div class="st mt">Will this<br>work for me?</div>'
   '<div class="st mt">Can I<br>trust you?</div>'
   '<div class="st mt">What if<br>I hate it?</div>')
 +cell(7,13,1,4,'<div class="ch">Reviews answer all three</div>'
   '<div class="b mt">Cheaper than any copy you could write. With faces, better still.</div>','lemon')
 +cell(7,13,4,6,'<div class="c3">And a hidden returns policy kills the sale</div>'
   '<div class="bs mt mut">A stranger will not risk $42 on a shop that will not say what happens if it fails.</div>')
 +cell(1,13,6,9,'<div class="b">On today&rsquo;s brand: are there reviews? With faces? '
   'Is the returns policy findable in <b>one click</b>?</div>','ink'),
 'These three questions are what a product page is FOR. Everything on it either answers one of them or is decoration.', num='08'),

WN('Subscribe &amp; save, or a bundle?',
 'Subscription buys LTV',
 'The next order is already agreed. Predictable revenue, and she stops shopping around. '
 'Costs about <b>15% margin, forever</b>.',
 'Bundle buys AOV',
 'A fatter order <b>today</b> &mdash; right when there may never be a second one. '
 'Less margin per unit, but the cash is now.',
 'Different problems, opposite answers. A shop with a repeat problem needs the first. A shop with thin orders needs the second. Do not let anyone say them in the same breath. And note the trap — a sub discount so deep the shop loses money on its most loyal customers. Fear two again.',
 num='09'),

slide(
 cell(1,8,1,5,'<div class="l mut">The cart</div>'
   '<div class="t mt">&ldquo;You are <em>$12 away</em> from free shipping.&rdquo;</div>')
 +cell(8,13,1,5,'<div class="b">She would rather add <b>$12 of product</b> than pay <b>$7 of shipping</b> for nothing.</div>'
   '<div class="b mt2">The strongest lever in ecom, and it costs the merchant nothing to try.</div>','lemon')
 +cell(1,13,5,9,'<div class="ch">But set it too high&hellip;</div>'
   '<div class="b mt">&hellip;and it stops being a nudge and becomes <b>a wall</b>. '
   'The threshold has to sit above the point where the maths works, or the merchant is just paying postage.</div>','ink'),
 'Add to cart live so they watch the bar move.', kicker='Open it live', num='10'),

slide(
 cell(1,13,1,2,'<div class="t">Checkout &mdash; where intent goes to <em>die</em></div>')
 +cell(1,5,2,6,'<div class="n">39%</div><div class="ls mt">abandon over extra costs</div>'
   '<div class="bs mt mut">shipping, tax, fees. The number one reason.</div>','lemon')
 +cell(5,9,2,6,'<div class="n">70%</div><div class="ls mt">of all carts abandoned</div>'
   '<div class="bs mt mut">that is normal, not failure</div>','ink')
 +cell(9,13,2,6,'<div class="c3">Baymard Institute</div>'
   '<div class="bs mt mut">baymard.com/lists/cart-abandonment-rate</div>'
   '<div class="bs mt">Real research. Cite it &mdash; merchants respect it.</div>')
 +cell(1,13,6,9,'<ul><li class="b">The <b>discount code box</b> is a leak &mdash; they leave to hunt a code</li>'
   '<li class="b">Express wallets: five fields become <b>one thumbprint</b></li>'
   '<li class="b">Guest checkout &mdash; do not force an account on a stranger</li></ul>'),
 'A seven dollar fee on a forty-two dollar order reads as a seventeen percent price rise. It is the surprise, not the price.', num='11'),

slide(
 cell(1,13,1,4,'<div class="d">&ldquo;Conversion is down&rdquo;<br>is <em>not a problem.</em></div>')
 +cell(1,13,4,6,'<div class="st">It is a symptom of a leak at <b>one specific step.</b></div>')
 +cell(1,7,6,9,'<div class="ch">An AM finds the step.</div>','lemon')
 +cell(7,13,6,9,'<div class="ch mut">CS forwards the sentence.</div>','ink'),
 'That sentence is the difference between the two jobs. That is all it is.', num='12'),

slide(
 cell(1,7,1,6,'<div class="l mut">Now read what they installed</div>'
   '<div class="t mt">View<br>source.</div>'
   '<div class="b mt2">Right-click &rarr; View Page Source &rarr; Ctrl-F</div>'
   '<div class="bs mt mut">Then the footer &middot; /account &middot; /pages/rewards</div>')
 +cell(7,13,1,6,'<div class="ls mb">search for these</div>'+logorow([
   ('klaviyo','klaviyo'),('attentive','attentive'),('recharge','recharge'),('skio','skio'),
   ('smile','smile'),('yotpo','yotpo'),('loyaltylion','loyaltylion'),('rivo','rivo'),
   ('okendo','okendo'),('judgeme','judge.me'),('gorgias','gorgias'),('rebuy','rebuy')],40),'ink')
 +cell(1,13,6,9,'<div class="st">Sixty seconds, and you know more than <em>a discovery call</em> would tell you.</div>','lemon'),
 'Do it live on Halfdays. It is genuinely fun to watch.', kicker='Open it live', num='13'),

slide(
 cell(1,13,1,2,'<div class="t">The stack is a <em>confession</em></div>')
 +cell(1,13,2,7,'<table style="font-size:24px">'
   '<tr><th>They installed</th><th>So they believe their problem is</th></tr>'
   f'<tr><td>{logo("klaviyo",38)}{logo("attentive",38)}<b>Klaviyo / Attentive</b></td><td>&ldquo;I cannot reach my visitors again&rdquo;</td></tr>'
   f'<tr><td>{logo("alia",38)}<b>a popup tool</b></td><td>&ldquo;too many people leave anonymous&rdquo;</td></tr>'
   f'<tr><td>{logo("okendo",38)}{logo("judgeme",38)}<b>Okendo / Judge.me</b></td><td>&ldquo;strangers do not trust me yet&rdquo;</td></tr>'
   f'<tr><td>{logo("rebuy",38)}<b>Rebuy / bundle</b></td><td>&ldquo;my orders are too thin&rdquo; &mdash; AOV</td></tr>'
   f'<tr><td>{logo("recharge",38)}{logo("skio",38)}<b>Recharge / Skio</b></td><td>&ldquo;customers buy once and vanish&rdquo; &mdash; LTV</td></tr>'
   f'<tr><td>{logo("smile",38)}{logo("rivo",38)}<b>a loyalty app</b></td><td>&ldquo;I have a base and nothing brings them back&rdquo;</td></tr>'
   '<tr><td class="mut">nothing at all</td><td class="mut">very early &mdash; or nobody is minding the shop</td></tr>'
   '</table>','flat')
 +cell(1,13,7,9,'<div class="st">Nobody installs a bundle app for fun.</div>'
   '<div class="b mt mut">They installed it at 11pm after looking at a number that scared them. '
   'The stack tells you what the owner is afraid of <b>before they say a word</b>.</div>','ink'),
 'This is the AM read, and it is the single most useful thing in the whole course.', num='14'),

BRANDBEAT(2,'What are they <em>paying to fix</em> &mdash; and is it their real leak?',
 'Halfdays runs Klaviyo, Yotpo Reviews and Rebuy — and no loyalty. Rebuy says they think their orders are too thin. Klaviyo says they want to reach people again. Nothing says they have solved coming back. Now ask whether that matches where you actually watched people fall out.','15','Halfdays','halfdays.com'),

slide(
 cell(1,8,1,9,'<div class="l mut">Now you &middot; 45 minutes</div>'
   '<div class="t mt">Diagnose a shop you have <em>not</em> seen.</div><div class="rule"></div>'
   '<ul><li class="b">Pairs, <b>phones out</b>, real money in the cart</li>'
   '<li class="b">Walk it as a customer. Fill <b>&sect;0&ndash;6</b></li>'
   '<li class="b">Write down <b>every problem you find</b> &mdash; then <b>rank them</b></li></ul>')
 +cell(8,13,1,5,'<div class="ch">Three problems, ranked. And <em>what it would cost</em> to fix each one.</div>'
   '<div class="bs mt2 mut">If loyalty is not in your top three, say so.</div>','lemon')
 +cell(8,13,5,9,'<div class="c3 lem">Homework</div>'
   '<div class="bs mt">A full teardown on two more brands.</div>'
   '<div class="bs mt">Walk your own store. Mark where you would quit.</div>'
   '<div class="bs mt">Three tickets &mdash; which step is each really about?</div>','ink'),
 'Stop before paying. Nobody buys anything on the projector.', kicker='They do it', num='16'),
]

# ── session 1: live store examples, clickable ──
_STORES = [
slide(
 cell(1,13,1,2,'<div class="l mut">Open all four. Same rule, four different numbers.</div>'
   '<div class="t mt">Why is free shipping <em>$30</em> here and <em>$95</em> there?</div>')
 +cell(1,4,2,6,f'{logo("raewellness",34)}'+'<div class="c3" style="display:inline">Rae Wellness</div><div class="n-sm mt">$30</div>'
   '<div class="bs mut">supplements, $19.99&ndash;$30</div><div class="mt">'+link('raewellness.co')+'</div>')
 +cell(4,7,2,6,f'{logo("crownaffair",34)}'+'<div class="c3" style="display:inline">Crown Affair</div><div class="n-sm mt">$75</div>'
   '<div class="bs mut">haircare, mid-price</div><div class="mt">'+link('crownaffair.com')+'</div>','lemon')
 +cell(7,10,2,6,f'{logo("halfdays",34)}'+'<div class="c3" style="display:inline">Halfdays</div><div class="n-sm mt">$95</div>'
   '<div class="bs mut">outerwear</div><div class="mt">'+link('halfdays.com')+'</div>')
 +cell(10,13,2,6,f'{logo("hexclad",34)}'+'<div class="c3" style="display:inline">HexClad</div><div class="n-sm mt">free</div>'
   '<div class="bs mut">$100+ pans</div><div class="mt">'+link('hexclad.com')+'</div>','ink')
 +cell(1,13,6,9,'<div class="st">Each number sits <em>just above</em> where that shop&rsquo;s average order '
   'already lands.</div>'
   '<div class="b mt mut">It is not a guess and it is not copied. It is the one lever that raises the basket '
   'without touching the price &mdash; and you can read it off four sites in two minutes.</div>','ink'),
 'Open all four in tabs before the session. Let the room guess the reason before you tell them. This is the first time they see a business decision they can read from the outside, and it is a good one to start with because the answer is clean.',
 kicker='Open them live'),

slide(
 cell(1,13,1,2,'<div class="l mut">Bought once, or bought again? Go and decide.</div>')
 +cell(1,7,2,6,'<div class="c3">Open these</div><div class="rule"></div>'
   '<div>'+link('hexclad.com','hexclad.com')+link('halfdays.com','halfdays.com')+'</div>'
   '<div>'+link('raewellness.co','raewellness.co')+link('crownaffair.com','crownaffair.com')+'</div>'
   '<div class="bs mt2 mut">For each: does it run out? wear out? is there a next size, next drop, next flavour?</div>')
 +cell(7,13,2,6,'<div class="c3 lem">Then predict the stack</div>'
   '<div class="bs mt">Bought once &rarr; expect <b>bundles and upsells</b>.</div>'
   '<div class="bs mt">Bought again &rarr; expect <b>subscription and email</b>.</div>'
   '<div class="bs mt2">Say it out loud <b>before</b> you look at the source.</div>','ink')
 +cell(1,13,6,9,'<div class="st">Then look. <em>Were you right?</em></div>'
   '<div class="b mt mut">This is the whole skill in one exercise: read the product, predict the business, '
   'check yourself. Being roughly right, fast, beats being precisely right, slowly.</div>','lemon'),
 'Do this live in tabs. It is the first time they make a prediction and get graded by reality in the same minute, which is where the confidence comes from.',
 kicker='Open them live'),

slide(
 cell(1,7,1,5,'<div class="l mut">And the one they all learn from</div>'
   '<div class="t mt">Dollar Shave Club, <em>today</em></div>'
   '<div class="b mt2">Fourteen years after the video. Still a subscription. Still a starter set.</div>'
   '<div class="mt">'+link('dollarshaveclub.com')+'</div>')
 +cell(7,13,1,5,'<div class="c3">Look for</div><div class="rule"></div>'
   '<div class="bs">the <b>$4.99 starter set</b> &mdash; a cheap first order on purpose</div>'
   '<div class="bs mt">how fast they push you to <b>subscribe</b></div>'
   '<div class="bs mt">how little the razor itself is discussed</div>','lemon')
 +cell(1,13,5,9,'<div class="st">They still sell the <em>second order</em>, not the first.</div>'
   '<div class="b mt mut">The cheap starter set is not generosity. It is the order-1 table from earlier: '
   'lose a little to win the customer, then make the money on every box after. '
   'You are looking at the arithmetic we just did on a whiteboard, running in public.</div>','ink'),
 'Close the money half here. The video showed them the idea; the live site shows them it still runs. Ask the room to find where the site pushes subscription — it is everywhere once you look.',
 kicker='Open it live'),
]

# ── session 1 drill: timeboxed, with a worked target ──
_DRILL1 = [
slide(
 cell(1,13,1,2,'<div class="l mut">Now you &middot; 45 minutes, in pairs</div>'
   '<div class="t mt">A brand you have <em>not</em> seen today.</div>')
 +cell(1,13,2,3,'<div class="frow"><div class="fbar" style="width:110px">3 min</div>'
   '<div class="bs"><b>Get your brand.</b> <span class="mut">One per pair, handed to you. Open it on your phone.</span></div></div>','flat')
 +cell(1,13,3,4,'<div class="frow"><div class="fbar" style="width:110px">12 min</div>'
   '<div class="bs"><b>Sheet &sect;0</b> <span class="mut">&mdash; what they sell, the hero product, its price, who buys it.</span></div></div>','flat')
 +cell(1,13,4,5,'<div class="frow"><div class="fbar win" style="width:110px">17 min</div>'
   '<div class="bs"><b>Sheet &sect;1 &mdash; the money on one unit.</b> '
   '<span class="mut">The hard part. Guess the cost to make. Take out shipping, fees, a discount, the ad.</span></div></div>','flat')
 +cell(1,13,5,6,'<div class="frow"><div class="fbar" style="width:110px">8 min</div>'
   '<div class="bs"><b>Write your answer</b> <span class="mut">to the question below. One number, one sentence.</span></div></div>','flat')
 +cell(1,13,6,7,'<div class="frow"><div class="fbar" style="width:110px">5 min</div>'
   '<div class="bs"><b>Swap sheets</b> <span class="mut">with the pair next to you. Mark theirs. Do you believe their number?</span></div></div>','flat')
 +cell(1,13,7,9,'<div class="st">At that margin, <em>how many orders</em> before they are ahead?</div>'
   '<div class="b mt mut">Every pair answers that out loud. Sixty seconds each. One number, one sentence &mdash; '
   'not a tour of the website.</div>','ink'),
 'Read the timings out and put them on the board. Without a clock a pair finishes section zero in eight minutes and then drifts. The swap at the end is not filler — marking somebody else forces them to decide what a good answer looks like.',
 kicker='They do it'),

slide(
 cell(1,13,1,2,'<div class="l mut">What a good one looks like &mdash; so you have a target</div>'
   '<div class="st mt">Rae Wellness &middot; a $25 daily supplement</div>')
 +cell(1,7,2,8,'<table style="font-size:24px">'
   '<tr><td>They charge</td><td class="r">$25.00</td></tr>'
   '<tr><td>Guess: cost to make <span class="mut">(powder, capsule, jar, label)</span></td><td class="r">&minus;$7.00</td></tr>'
   '<tr><td>Free shipping over $30, so they eat it</td><td class="r">&minus;$5.00</td></tr>'
   '<tr><td>Processing</td><td class="r">&minus;$1.03</td></tr>'
   '<tr><td class="mut">before any advertising</td><td class="r mut">$11.97</td></tr>'
   '<tr class="tot"><td>Say they pay $15 to find her</td><td class="r">&minus;$3.03</td></tr></table>')
 +cell(7,13,2,5,'<div class="c3 lem">The answer</div>'
   '<div class="b mt">&ldquo;They lose about three dollars on the first order. '
   'They need <b>two</b> before they are ahead &mdash; and it is a supplement, so a second order is realistic.&rdquo;</div>','ink')
 +cell(7,13,5,8,'<div class="c3">Why this is good</div>'
   '<div class="bs mt">Every number is a <b>guess</b>. None of them are researched. '
   'And it still produces a real answer somebody could act on.</div>')
 +cell(1,13,8,9,'<div class="c3">Nobody looked up a cost. <em>Guess, do not research.</em> '
   'Roughly right and fast beats precisely right and late.</div>','lemon'),
 'Put this up before they start and leave it up. Without a target they will either write one line or try to research real COGS and burn the whole session. The point of the slide is permission to guess.'),
]

def _step(t, bold, rest, win=0):
    cls = 'fbar win' if win else 'fbar'
    return ('<div class="frow"><div class="' + cls + '" style="width:110px">' + t + '</div>'
            '<div class="bs"><b>' + bold + '</b> <span class="mut">' + rest + '</span></div></div>')

# ── SESSION 2 drill ──
_DRILL2 = [
slide(
 cell(1,13,1,2,'<div class="l mut">Now you &middot; 45 minutes, in pairs</div>'
   '<div class="t mt">Diagnose a shop you have <em>not</em> seen.</div>')
 +cell(1,13,2,3,_step('3 min','Get your brand.','One per pair. Open it on a phone, cart empty, not logged in.'),'flat')
 +cell(1,13,3,4,_step('12 min','Walk it as a customer.','Ad or social &rarr; product &rarr; cart &rarr; checkout. Where would <b>you</b> quit?'),'flat')
 +cell(1,13,4,5,_step('10 min','Read the stack.','View source, Ctrl-F. Then /pages/rewards. What are they paying to fix?'),'flat')
 +cell(1,13,5,6,_step('12 min','List every problem you found.','All of them. Messy is fine. Do not rank yet.','1'),'flat')
 +cell(1,13,6,7,_step('8 min','Rank your top three.','And next to each: <b>what would it cost to fix?</b>'),'flat')
 +cell(1,13,7,9,'<div class="st">Three problems, ranked, with the cost of each.</div>'
   '<div class="b mt mut">If loyalty is not in your top three, <b>say so</b>. That is a correct answer and '
   'we would rather hear it here than from the merchant in six months.</div>','ink'),
 'Separating "list everything" from "rank them" matters. If they rank as they go they stop at the first thing they recognise. Make them dump first.',
 kicker='They do it'),

slide(
 cell(1,13,1,2,'<div class="l mut">What a good one looks like &mdash; Halfdays, which you already know</div>')
 +cell(1,13,2,3,'<div class="frow"><div class="fbar" style="width:64px">1</div>'
   '<div class="bs"><b>A 10% popup on premium outerwear.</b> '
   '<span class="mut">Free to change. Are they discounting people who were buying a $300 jacket anyway? Fear #2.</span></div></div>','flat')
 +cell(1,13,3,4,'<div class="frow"><div class="fbar" style="width:64px">2</div>'
   '<div class="bs"><b>Past buyers may never see the next drop.</b> '
   '<span class="mut">Cheap. Apparel repeats by season, not refill &mdash; so new arrivals to past purchasers is the lever.</span></div></div>','flat')
 +cell(1,13,4,5,'<div class="frow"><div class="fbar win" style="width:64px">3</div>'
   '<div class="bs"><b>Nothing gives a reason to choose them next season.</b> '
   '<span class="mut">Slowest and last. This is ours &mdash; and it is third, not first.</span></div></div>','flat')
 +cell(1,7,5,9,'<div class="c3">Why this is good</div><div class="rule"></div>'
   '<div class="b">Three problems, ordered by <b>people lost</b> and <b>cost to fix</b>. '
   'Two of them we do not sell. That is what makes the third one credible.</div>')
 +cell(7,13,5,9,'<div class="c3 lem">What a weak one looks like</div><div class="rule"></div>'
   '<div class="b">&ldquo;They should add a loyalty program.&rdquo;</div>'
   '<div class="bs mt2 mut">One item, unranked, no cost, and it happens to be the thing we sell. '
   'That is a pitch, not a diagnosis.</div>','ink'),
 'The weak example is the important half. Everyone can produce the weak version. Show them the difference explicitly or they will hand you the pitch and think it is a diagnosis.'),
]

# ── SESSION 3 drill ──
_DRILL3 = [
slide(
 cell(1,13,1,2,'<div class="l mut">Now you &middot; 45 minutes, in pairs</div>'
   '<div class="t mt">Two brands. One <em>recommendation</em> each.</div>')
 +cell(1,13,2,3,_step('3 min','Get your two brands.','One with a strong repeat reason, one with a weak one. Handed to you.'),'flat')
 +cell(1,13,3,4,_step('10 min','Brand A.','Why would a human buy this twice? What does the brand already do about it?'),'flat')
 +cell(1,13,4,5,_step('10 min','Brand B.','Same two questions. &ldquo;No reason&rdquo; is an allowed answer &mdash; and often the right one.'),'flat')
 +cell(1,13,5,6,_step('12 min','Prescribe one thing each.','Referral, points, credit, tiers, subscription &mdash; or <b>nothing yet</b>.','1'),'flat')
 +cell(1,13,6,7,_step('10 min','Name what you rejected.','And what that option would have lost. <b>This is the graded part.</b>'),'flat')
 +cell(1,13,7,9,'<div class="st">Anyone can pick something. Only somebody who understands it can say '
   '<em>what the alternative costs.</em></div>','ink'),
 'The rejected option is the whole grading criterion. Say that before they start, or they will spend forty minutes on the recommendation and thirty seconds on the part you are actually marking.',
 kicker='They do it'),

slide(
 cell(1,13,1,2,'<div class="l mut">What a good one looks like &mdash; both brands from earlier</div>')
 +cell(1,7,2,6,'<div class="c3">Crown Affair</div><div class="rule"></div>'
   '<div class="bs mut">refill product, no loyalty, Recharge already installed</div>'
   '<div class="b mt2"><b>Points, tied to the refill window.</b></div>'
   '<div class="bs mt2"><b>Rejected: store credit.</b> It would be understood faster &mdash; but credit is '
   'money with a logo on it. They have spent years building a brand; points can carry it, credit cannot.</div>','lemon')
 +cell(7,13,2,6,'<div class="c3">HexClad</div><div class="rule"></div>'
   '<div class="bs mut">$300 pan, five-year cycle, already runs Rivo</div>'
   '<div class="b mt2"><b>Referral and range &mdash; not a refill points scheme.</b></div>'
   '<div class="bs mt2"><b>Rejected: points on a repurchase cycle.</b> They would expire before she needs '
   'another pan. You would have added a cost and produced no second order.</div>','ink')
 +cell(1,13,6,9,'<div class="st">Both name the rejected option <em>and</em> what it loses.</div>'
   '<div class="b mt mut">Notice the second one recommends something we do not really sell. '
   'That is not a failure of the exercise &mdash; it is the exercise.</div>'),
 'Point at the HexClad half explicitly. If nobody in the room ever recommends something outside our product, they have not understood the job.'),
]

# ── SESSION 4 drill ──
_DRILL4 = [
slide(
 cell(1,13,1,2,'<div class="l mut">Now you &middot; 45 minutes, in pairs</div>'
   '<div class="t mt">Two brands. One <em>verdict</em> each.</div>')
 +cell(1,13,2,3,_step('3 min','Get your two brands.','One should pass and one should fail. You are not told which.'),'flat')
 +cell(1,13,3,4,_step('12 min','Run the checklist on both.','Line by line, out loud. Everything is visible from the public site.'),'flat')
 +cell(1,13,4,5,_step('10 min','Ask the harder question.','Do they need it <b>at all</b>? Base, stage &mdash; and check the one-star reviews.'),'flat')
 +cell(1,13,5,6,_step('12 min','Write the verdict.','Ours / not ours / not yet &mdash; plus <b>the one thing you would change</b>.','1'),'flat')
 +cell(1,13,6,7,_step('8 min','Defend it to another pair.','They try to talk you out of it. Change your mind if they are right.'),'flat')
 +cell(1,13,7,9,'<div class="st">Is it ours &middot; does it need this &middot; <em>what is the one thing we would change?</em></div>','ink'),
 'The defend-it step is what makes this a graduation drill rather than a worksheet. A verdict you cannot defend out loud is not a verdict.',
 kicker='They do it'),

slide(
 cell(1,13,1,2,'<div class="l mut">What a good one looks like</div>')
 +cell(1,7,2,7,'<div class="c3">Rae Wellness</div><div class="rule"></div>'
   '<div class="ch mt">Ours. <em>Now.</em></div>'
   '<div class="bs mt2">Shopify, wellness, repurchase, Klaviyo, Recharge heavily used, '
   '<b>/pages/rewards 404s</b>, no competitor.</div>'
   '<div class="bs mt2"><b>The one thing:</b> nothing gives a reason to choose them. Points on the refill '
   'window, surfaced in the Klaviyo flow they already run.</div>','lemon')
 +cell(7,13,2,7,'<div class="c3">HexClad</div><div class="rule"></div>'
   '<div class="ch mt">Not ours.</div>'
   '<div class="bs mt2"><b>Rivo is already installed.</b> Fails the checklist on the most visible line there is '
   '&mdash; found in sixty seconds, no opinion required.</div>'
   '<div class="bs mt2">And even without it: a $300 pan on a five-year cycle is the wrong shape for points. '
   'Two reasons, either one enough.</div>','ink')
 +cell(1,13,7,9,'<div class="st">A verdict is a <em>decision plus a reason a lead can check.</em></div>'
   '<div class="b mt mut">&ldquo;Feels like a good fit&rdquo; is not a verdict. '
   '&ldquo;Rivo is installed, here is the line in the source&rdquo; is.</div>'),
 'The last line is the standard. Anything that cannot be checked by somebody else in under a minute is an opinion, not a verdict.'),
]

# ── sources: every claim in the session, clickable ──
_SRC1 = slide(
 cell(1,13,1,2,'<div class="l mut">Where all of this came from</div>'
   '<div class="st mt">Check any of it. <em>None of it is mine.</em></div>')
 +cell(1,13,2,8,
   src_row('brandsvietnam','Bài toán chi phí — Nike &amp; adidas','brandsvietnam.com/12953-bai-toan-chi-phi-va-gia-thanh-tren-moi-doi-giay-nike-adidas','&mdash; the $100 shoe, from 2015 filings. In Vietnamese.')
  +src_row('youtube','Dollar Shave Club, the 2012 film','youtube.com/watch?v=RBHMf7BNd8o','&mdash; 90 seconds, $4,500, 12,000 orders in 48 hours')
  +src_row('dsc','Dollar Shave Club today','dollarshaveclub.com','&mdash; still a subscription, still a $4.99 starter set')
  +src_row('halfdays','Halfdays','halfdays.com','&mdash; free shipping $95')
  +src_row('crownaffair','Crown Affair','crownaffair.com','&mdash; free shipping $75')
  +src_row('raewellness','Rae Wellness','raewellness.co','&mdash; free shipping $30')
  +src_row('hexclad','HexClad','hexclad.com','&mdash; free shipping always, $100+ pans')
   ,'flat')
 +cell(1,13,8,9,'<div class="c3">Send this slide to the team. <em>Reading the source beats trusting the trainer.</em></div>','ink'),
 'Give them the links. A cohort whose problem was never English can read a Vietnamese source better than we can — and the shoe article is the single most persuasive thing in the session.',
 kicker='All clickable')

_SRC2 = slide(
 cell(1,13,1,2,'<div class="l mut">Where all of this came from</div>'
   '<div class="st mt">The whole diagnostic tree is <em>somebody else&rsquo;s work.</em></div>')
 +cell(1,7,2,7,'<div class="c3 mb">Watch this one</div>'
   +'<div style="height:74%;min-height:250px">'+video('42uhZYnyEXU','Chase Chappell — every ecom metric',CHASETHUMB)+'</div>'
   +'<div class="mt">'+link('youtube.com/watch?v=42uhZYnyEXU','open on YouTube')+'</div>'
   +'<div class="bs mt mut">44 min. Every metric, what it means, what to do. '
   'We use the <b>site and business</b> half; the ad-account half is not our altitude.</div>')
 +cell(7,13,2,7,
   src_row('baymard','Baymard Institute','baymard.com/lists/cart-abandonment-rate','&mdash; ~70% abandon, 39% over extra costs')
  +src_row('meta','Meta Ad Library','facebook.com/ads/library','&mdash; every live ad, any brand, free')
  +src_row('crownaffair','Crown Affair','crownaffair.com','&mdash; the ICP-matched winner')
  +src_row('hexclad','HexClad','hexclad.com','&mdash; the Plus store, and the 52% popup')
  +src_row('halfdays','Halfdays','halfdays.com','&mdash; the brand you diagnose')
   ,'flat')
 +cell(1,13,7,9,'<div class="c3">The stack map &mdash; 130 apps across 28 fields &mdash; is internal: '
   '<em>avada-know-the-drill</em>. Ask for access.</div>','ink'),
 'Play a minute of the Chase video if you have time — the site walkthrough around six minutes in is the clearest part. Otherwise just point at it and move on.',
 kicker='All clickable')

_SRC3 = slide(
 cell(1,13,1,2,'<div class="l mut">Where all of this came from</div>'
   '<div class="st mt">Two brands, one video, and your own inbox.</div>')
 +cell(1,7,2,7,'<div class="c3 mb">The retention half of the same video</div>'
   +'<div style="height:70%;min-height:230px">'+video('42uhZYnyEXU','Chase Chappell — retention diagnostics',CHASETHUMB)+'</div>'
   +'<div class="mt">'+link('youtube.com/watch?v=42uhZYnyEXU','open on YouTube')+'</div>'
   +'<div class="bs mt mut">The returning-rate trap and the three product types are from here.</div>')
 +cell(7,13,2,7,
   src_row('crownaffair','Crown Affair','crownaffair.com','&mdash; strong repeat, Recharge, no loyalty')
  +src_row('hexclad','HexClad','hexclad.com','&mdash; weak repeat, and runs Rivo anyway')
  +src_row('rivo2','Rivo case studies','rivo.io','&mdash; 19 studies, one number each, no feature lists')
  +src_row('klaviyo','Klaviyo','klaviyo.com','&mdash; the cheapest way to reach anyone')
  +src_row('attentive','Attentive','attentive.com','&mdash; SMS, ~100&times; the cost per message')
   ,'flat')
 +cell(1,13,7,9,'<div class="c3">And the best source in this session is <em>your own inbox</em> &mdash; '
   'the emails you got from your build-track order.</div>','ink'),
 'Point at the inbox line. Nothing on this list beats an email they received themselves about an order they placed.',
 kicker='All clickable')

_SRC4 = slide(
 cell(1,13,1,2,'<div class="l mut">Where all of this came from</div>'
   '<div class="st mt">The ICP is <em>ours</em>. Everything else is checkable.</div>')
 +cell(1,13,2,8,
   src_row('raewellness','Rae Wellness','raewellness.co','&mdash; Recharge + Klaviyo + /pages/rewards 404')
  +src_row('hexclad','HexClad','hexclad.com','&mdash; Rivo installed. Fails the checklist visibly.')
  +src_row('rivo2','Rivo &mdash; case studies','rivo.io','&mdash; 55&times; ROI banner, one hero number per card')
  +src_row('shopify','Shopify Plus signals','shopify.com/plus','&mdash; checkout extensions, markets, B2B')
  +src_row('recharge','Recharge','rechargepayments.com','&mdash; the subscription half of the easiest win')
  +src_row('klaviyo','Klaviyo','klaviyo.com','&mdash; the other half')
   ,'flat')
 +cell(1,13,8,9,'<div class="c3">Joy&rsquo;s ICP band and exclusions come from the outbound research &mdash; '
   '<em>Team Joy</em> in Obsidian. Ask for it.</div>','ink'),
 'The point of this slide is that nothing in the verdict rests on an opinion. Every line is somewhere they can go and look.',
 kicker='All clickable')

# ═════════════════ SESSION 2 — WHY PEOPLE COME BACK ═════════════════
S3=[
TITLE('Goal: why a person buys a second time, and what actually makes them. Today we break down TWO brands — one with a strong reason to return, one with none.',
 'Session Three','Why people<br>come<br><em>back</em>',
 ('Retention and loyalty. Our own subject.','Last session ended when she paid. Everything today is after the money changed hands.'),'Our<br>subject'),

slide(
 cell(1,13,1,3,'<div class="l mut">The wait</div>'
   '<div class="t mt" style="font-family:\'JetBrains Mono\',monospace;text-transform:none">paid &mdash;&mdash;&mdash;&mdash; ? &mdash;&mdash;&mdash;&mdash; arrived</div>')
 +cell(1,7,3,7,'<div class="ch">Nothing happens here.</div><div class="rule"></div>'
   '<div class="b">That is the problem. This gap is where every <b>&ldquo;where is my order&rdquo;</b> ticket is born '
   '&mdash; usually the biggest ticket category in ecom.</div>')
 +cell(7,13,3,7,'<div class="ch">You already live in this one.</div><div class="rule"></div>'
   '<div class="b">A late parcel someone <b>warned you about</b> is fine.</div>'
   '<div class="b mt">A late parcel nobody mentioned is a refund and a one-star review.</div>','lemon')
 +cell(1,13,7,9,'<div class="b">How many WISMO tickets did you close last week? That number is a <b>shipping</b> problem, not a support problem.</div>','ink'),
 'Ask the room for the actual number. It will be large, and it will be the first time they have thought of it as somebody else fault.', num='02'),

slide(
 cell(1,13,1,2,'<div class="t">The eight weeks <em>after</em> she pays</div>')
 +cell(1,13,2,6,'<table>'
   '<tr><th>When</th><th>Email</th><th>Job</th></tr>'
   '<tr><td class="mut">immediately</td><td>confirmation</td><td>reassurance</td></tr>'
   '<tr><td class="mut">ships</td><td>tracking</td><td>kill the WISMO ticket</td></tr>'
   '<tr><td class="mut">delivered</td><td>how to use it</td><td><b>make sure she uses it</b></td></tr>'
   '<tr><td class="mut">~week 2</td><td>review request</td><td>proof for the next stranger</td></tr>'
   '<tr class="tot"><td>~week 6</td><td>&ldquo;running low?&rdquo;</td><td>the money email</td></tr></table>','flat')
 +cell(1,7,6,9,'<div class="c3">Notice the review timing</div>'
   '<div class="bs mt">It is asked when she has <b>used</b> it &mdash; not when it arrived. '
   'A day-one review is a review of the packaging.</div>')
 +cell(7,13,6,9,'<div class="ch">Week 6 is worth more than <em>the ad</em> that found her.</div>','lemon'),
 'You arrive before she runs out and before she thinks about alternatives. One automated email, sent to someone who already likes them, beats thirty dollars of advertising.', num='03'),

BRANDBEAT(1,'What do they send you <em>after</em> you buy?',
 'Crown Affair runs Klaviyo, Attentive AND Postscript plus Recharge — the fullest owned-channel stack you will see. Every way back from the last ten minutes is installed here except one: ours. Also use the team own inbox from their build-track orders.','04','Crown Affair','crownaffair.com'),

slide(
 cell(1,13,1,4,'<div class="d">Why would a human buy<br><em>this</em> twice?</div>')
 +cell(1,13,4,6,'<div class="st">Ask it about <b>both</b> brands on the table today.</div>')
 +cell(1,13,6,9,'<div class="b">Let the room struggle on the weak one. <b>Do not rescue them.</b> '
   'The struggle is the lesson, and it is the whole setup for the last session.</div>','ink'),
 'This is the question the entire course has been walking toward.', kicker='Ask the room', num='05'),

slide(
 cell(1,6,1,9,'<div class="l mut">And here is what they do instead</div>'
   '<div class="t mt">52% off,<br><em>for an email.</em></div>'
   '<div class="rule"></div>'
   '<div class="b">HexClad, today. A brand with no natural repeat, discounting hard to win the first order.</div>'
   '<div class="b mt2">That is a rational answer for a product bought once &mdash; and a <b>terrible</b> '
   'habit to build if you ever want a second order at full price.</div>')
 +cell(6,13,1,9,img(HEXPOPUP),'photo'),
 'Show it before the why/why-not. It makes the next slide concrete: this is a real brand making a real choice, and you can see the trade-off on screen.',
 kicker='Open it live'),

WN('Does a loyalty program help this shop?',
 'Lumi &mdash; a refill brand',
 '$42 moisturizer, runs out every 8 weeks. She has to rebuy <b>something</b> &mdash; points decide it is Lumi, '
 'and decide it is <b>now</b> rather than in three weeks.',
 'HexClad &mdash; a $300 pan',
 'A pan is a five-year decision. Points on a refill cycle would <b>expire before they were worth anything</b>. '
 'And yet &mdash; <b>HexClad runs a loyalty program.</b> Go and look at what it actually rewards.',
 'Do NOT say HexClad should not run loyalty — they do run it, Rivo is installed, and the room can check in thirty seconds. Say: they run it, so go and look at what it rewards. They will find referral and buying the NEXT thing — a lid, a knife, another size — not re-buying the same pan. That is the high-ticket answer, and the brand proves it instead of being a strawman.',
 num='06'),

slide(
 cell(1,13,1,3,'<div class="l mut">Lumi, all the way through</div>'
   '<div class="t mt">One order with no ad attached<br>is worth <em>eight</em> of the first.</div>')
 +cell(1,7,3,6,'<div class="ls mut">Order 1 &middot; she spent $61.20</div>'
   '<div class="bar mt" style="width:26%;background:var(--paper)">+$2.13</div>')
 +cell(7,13,3,6,'<div class="ls mut">Order 2 &middot; she spent $42.00</div>'
   '<div class="bar mt" style="background:var(--lemon)">+$17.28</div>')
 +cell(1,13,6,9,'<table class="duo">'
   '<tr><td>Ad to reach Mai</td><td class="r">&minus;$30.00</td>'
   '<td>Free shipping, Lumi pays it</td><td class="r">&minus;$7.00</td></tr>'
   '<tr><td>Cart: moisturizer + travel size</td><td class="r">+$68.00</td>'
   '<td>Processing</td><td class="r">&minus;$2.07</td></tr>'
   '<tr class="tot"><td>Popup 10%</td><td class="r">&minus;$6.80</td>'
   '<td>Products &rarr; keeps</td><td class="r">+$2.13</td></tr></table>','ink'),
 'Mai spent sixty-one twenty and the shop kept two thirteen. Same shop, same product, same customer — the only difference on order two is nobody had to pay to find her.', num='07'),

slide(
 cell(1,13,1,4,'<div class="l mut">So what did the points actually do?</div>'
   '<div class="t mt">They did not make Mai <em>like</em> Lumi.</div>')
 +cell(1,13,4,6,'<div class="b">They gave her a reason to choose Lumi <b>instead of the alternative</b>, in that moment '
   '&mdash; and a nudge to do it <b>now</b> rather than in three weeks.</div>')
 +cell(1,13,6,9,'<div class="d">Loyalty does not buy affection.<br>It buys <em>timing and preference.</em></div>','lemon'),
 'If they remember one sentence about our product for the rest of their career, make it that one.', num='08'),

slide(
 cell(1,13,1,2,'<div class="t">Three things, <em>not one thing</em></div>')
 +cell(1,5,2,6,'<div class="c3">Subscription</div><div class="rule"></div>'
   '<div class="b">the next box is already agreed</div>')
 +cell(5,9,2,6,'<div class="c3">Loyalty</div><div class="rule"></div>'
   '<div class="b">a reason to choose <b>you</b> next time</div>','lemon')
 +cell(9,13,2,6,'<div class="c3">Discount</div><div class="rule"></div>'
   '<div class="b">this order is cheaper</div>')
 +cell(1,13,6,9,'<div class="st">A standing order does not mean she <em>chose</em> you.</div>'
   '<div class="b mt2 mut">It means she has not cancelled yet. Those are different things &mdash; '
   'and the gap between them is exactly what we sell.</div>','ink'),
 'Merchants mix these three up constantly. If you mix them up too, you cannot help them.', num='09'),

slide(
 cell(1,13,1,2,'<div class="t">Two machines, <em>opposite jobs</em></div>')
 +cell(1,7,2,7,'<div class="n-sm">Referral</div><div class="ch mt">grows the base</div><div class="rule"></div>'
   '<div class="b">New people arrive with <b>trust already loaded</b>. And you pay only when it works &mdash; '
   'unlike an ad, which you pay on hope.</div>','lemon')
 +cell(7,13,2,7,'<div class="n-sm">Loyalty</div><div class="ch mt">monetises the base</div><div class="rule"></div>'
   '<div class="b">The <b>same people</b>, chosen again. Nothing new arrives.</div>','ink')
 +cell(1,13,7,9,'<div class="st">Remember this. Next session it decides <em>what you recommend</em> to a real merchant.</div>'),
 'The shop that must NOT be sold points is often exactly the shop that should run referral. So "not ready" is never a dead end.', num='10'),

WN('They ask for store credit. Do you switch it on?',
 'Credit fits &mdash; considered, rare, returns',
 'Expensive one-off purchases, or a shop with lots of returns. Credit is <b>understood instantly</b> '
 'and keeps the money in the shop instead of refunding it out.',
 'Points fit &mdash; refill, habit, membership',
 'Credit is <b>money with your logo on it</b> &mdash; transactional, no attachment, and you are holding their cash. '
 'Points are the brand&rsquo;s currency, and they build a habit.',
 'Neither is the default. Ask stage, product, repurchase cycle, return rate — then recommend, and be able to say what the other option loses. That last part is the job.',
 num='11'),

slide(
 cell(1,7,1,5,'<div class="l mut">Points</div><div class="st mt">The brand&rsquo;s <em>currency</em></div>'
   '<div class="rule"></div>'
   '<ul><li class="bs">abstract &mdash; needs explaining</li><li class="bs">feels like belonging, progress</li>'
   '<li class="bs">you name it, you theme it</li><li class="bs">some are never redeemed</li></ul>')
 +cell(7,13,1,5,'<div class="l">Store credit</div><div class="st mt">Money with your <em>logo</em> on it</div>'
   '<div class="rule"></div>'
   '<ul><li class="bs">understood instantly</li><li class="bs">feels like a transaction</li>'
   '<li class="bs">looks like money, not like you</li><li class="bs">spent fast &mdash; you hold their cash</li></ul>','lemon')
 +cell(1,13,5,9,'<div class="ch">Which is why <em>on-brand</em> is not decoration.</div>'
   '<div class="b mt2">If the widget looks like a generic app bolted on, it is <b>not brand currency any more</b> '
   '&mdash; it is a coupon machine, and you threw away the only reason you chose points.</div>','ink'),
 'This is the sharpest thing in the loyalty half. On-brand has a mechanical reason, not a cosmetic one.', num='12'),

slide(
 cell(1,13,1,4,'<div class="d">VIP tiers.<br>Spend $500 to reach Gold.</div>')
 +cell(1,13,4,9,'<div class="d">Why <em>$500?</em></div>','lemon'),
 'Let them flounder. Nobody can defend it, because today the number is guessed. That is the problem.',
 kicker='Ask the room', num='13'),

slide(
 cell(1,7,1,6,'<div class="l mut">Where the number comes from</div>'
   '<ul><li class="b">Pull customers with total spend, last 12 months</li>'
   '<li class="b">Sort, highest first</li>'
   '<li class="b">Decide the share per tier &mdash; commonly <b>~5% top, ~20% middle</b></li>'
   '<li class="b">The spend at that cut line <b>is</b> your threshold</li></ul>')
 +cell(7,13,1,3,'<div class="c3">Too high</div><div class="bs mt">nobody reaches it &mdash; decoration</div>')
 +cell(7,13,3,6,'<div class="c3">Too low</div><div class="bs mt">everybody clears it &mdash; a discount for everyone. '
   '<b>Fear #2 with extra steps.</b></div>','ink')
 +cell(1,13,6,9,'<div class="st">If you cannot say <em>why the number is that number</em>, do not set it.</div>'
   '<div class="b mt mut">And the reason tiers exist at all is fear two: otherwise you hand the same coupon '
   'to a first-time buyer and to someone who spends $2,000 a year.</div>','lemon'),
 'Sanity-check both ways: is the top tier big enough to be worth running, and is the next tier reachable in a year?', num='14'),

slide(
 cell(1,8,1,9,'<div class="l mut">Now you &middot; 50 minutes</div>'
   '<div class="t mt">Two brands.<br>One <em>recommendation</em> each.</div><div class="rule"></div>'
   '<ul><li class="b">One with a strong repeat reason, one with a weak one</li>'
   '<li class="b">Teardown <b>&sect;4&ndash;5</b>, then prescribe</li></ul>')
 +cell(8,13,1,5,'<div class="ch">Points, credit, tiers or referral &mdash; and <em>what does the option you rejected lose?</em></div>','lemon')
 +cell(8,13,5,9,'<div class="c3 lem">The grading criterion</div>'
   '<div class="bs mt">Anyone can pick something. Only somebody who understands it can say '
   '<b>what the alternative costs.</b></div>','ink'),
 'Homework: what is the real reason someone reorders from YOUR store? Five tickets restated in two sentences each, own words, Vietnamese fine, no questions to the merchant.',
 kicker='They do it', num='15'),
]


S1.append(slide(
 cell(1,13,1,2,'<div class="l mut">The other way to raise that ceiling</div>'
   '<div class="t mt">Do not get more customers.<br>Make each order <em>fatter.</em></div>')
 +cell(1,7,2,6,'<div class="ch">Double AOV, double ROAS &mdash; without touching the ads</div>'
   '<div class="b mt2">$35 &rarr; $70 takes a 1.2x return to <b>2.4x</b>. Same ads, same spend, same everything.</div>','lemon')
 +cell(7,13,2,6,'<div class="c3">How merchants actually do it</div><div class="rule"></div>'
   '<ul><li class="bs">bundles, 4-packs, pre-built pairs</li><li class="bs">upsell in cart, on site, at checkout</li>'
   '<li class="bs"><b>free-shipping threshold set $1 above current AOV</b></li></ul>')
 +cell(1,13,6,9,'<div class="st">And a floor worth knowing: below about <em>$35</em> an order, '
   'almost nothing scales.</div>'
   '<div class="b mt mut">The ad cost and the shipping eat it. When a merchant with a $22 average order asks why '
   'ads are not working, that is usually the answer &mdash; and it is not an ads problem.</div>','ink'),
 'The threshold rule is the concrete one to remember: one dollar above where their average order sits today. Set it lower and it does nothing; set it far higher and it reads as a wall. Source: Chase Chappell, and it matches what we see in accounts.',
 num='23'))

# ── the merchant problem decoder ──
_DECODER = [
slide(
 cell(1,13,1,2,'<div class="l mut">A merchant never says &ldquo;I have a leak at the product page&rdquo;</div>'
   '<div class="st mt">They say a <em>number is bad.</em> Here is how to translate.</div>')
 +cell(1,13,2,8,'<table style="font-size:23px">'
   '<tr><th>What they say</th><th>What it actually means</th><th>Where</th></tr>'
   '<tr><td><b>Sales flat, ROAS great</b></td><td>ads are re-reaching people who already buy</td><td class="mut">come back</td></tr>'
   '<tr><td><b>Low returning rate</b></td><td>nothing brings them back &mdash; fix depends on what they sell</td><td class="mut">come back</td></tr>'
   '<tr><td><b>Low AOV</b></td><td>not enough money per order</td><td class="mut">cart</td></tr>'
   '<tr><td><b>Low ROAS, but clicks and CVR fine</b></td><td><b>AOV is the issue</b> &mdash; nothing is broken</td><td class="mut">money</td></tr>'
   '<tr><td><b>Good clicks, cheap reach, low CVR</b></td><td>a <b>site</b> problem, not an ads problem</td><td class="mut">product page</td></tr>'
   '<tr><td><b>Low CVR but high AOV</b></td><td><b>normal.</b> A $1,700 machine will never convert like a candle</td><td class="mut">&mdash;</td></tr>'
   '<tr><td><b>8% add to cart, 1% conversion</b></td><td><b>shipping too expensive</b> &mdash; or something is literally broken</td><td class="mut">checkout</td></tr>'
   '</table>','flat')
 +cell(1,13,8,9,'<div class="c3">You are not memorising this. You are learning the <em>path</em> &mdash; '
   'so you could rebuild most of it yourself.</div>','ink'),
 'Do not hand this out as a list. Use it as the answer key while pairs work a real brand: they name the symptom, they say where on the journey it lives, THEN you check it here. Source is Chase Chappell — the site and business half only.',
 num='25a'),

slide(
 cell(1,7,1,6,'<div class="l mut">When the product page is the problem</div>'
   '<div class="t mt">Move everything <em>upward.</em></div>'
   '<div class="b mt2">On first load she should see the offer, the proof and the price &mdash; without scrolling once.</div>')
 +cell(7,13,1,6,'<ul><li class="bs"><b>Three bullets</b> stating the offer, up top</li>'
   '<li class="bs"><b>Five to seven images</b> &mdash; ingredients, benefits, serving, lifestyle</li>'
   '<li class="bs"><b>Subscribe &amp; save selected by default</b></li>'
   '<li class="bs"><b>Remove the quantity selector</b> &mdash; she can add more from the cart</li>'
   '<li class="bs">Show the pack she actually picked. Six-pack? Show six.</li>'
   '<li class="bs"><b>Banner + free shipping above the fold</b></li>'
   '<li class="bs">Collapse the padding</li></ul>')
 +cell(1,13,6,9,'<div class="st">Ninety of a hundred people left on this page. '
   'These seven fixes cost <em>nothing</em> and no app is required.</div>'
   '<div class="b mt mut">Which is worth saying to a merchant who is about to buy their fourth app: '
   'the biggest leak on your site is free to fix.</div>','ink'),
 'This is the single most actionable list in the course, and it is the leak the funnel just showed them — 90 of 100. Nobody needs to sell them anything to fix it.',
 num='25b'),

slide(
 cell(1,13,1,2,'<div class="l mut">8% add to cart, 1% conversion &mdash; something is broken</div>'
   '<div class="st mt">Ninety percent of the time it is just <em>shipping.</em></div>')
 +cell(1,7,2,5,'<div class="c3">$30 product. $20 to ship.</div>'
   '<div class="b mt2">She added it, saw the total, and left. Not the price of the product &mdash; '
   '<b>the surprise</b>.</div>','lemon')
 +cell(1,7,5,7,'<div style="display:flex;gap:34px;align-items:baseline">'
   '<div><div class="n-sm">39%</div><div class="ls mut">abandon over extra costs<br>&mdash; the #1 reason</div></div>'
   '<div><div class="n-sm">70%</div><div class="ls mut">of all carts abandoned<br>&mdash; normal, not failure</div></div>'
   '</div><div class="bs mt2 mut">Baymard Institute &mdash; cite it, merchants respect it</div>','ink')
 +cell(7,13,2,7,'<div class="c3">And when it is not shipping</div><div class="rule"></div>'
   '<ul><li class="bs">a button <b>covering</b> the button</li>'
   '<li class="bs">cart page <b>and</b> drawer cart both loading</li>'
   '<li class="bs"><b>a loyalty widget over the checkout button</b></li>'
   '<li class="bs">a support widget over the CTA</li>'
   '<li class="bs">three payment options instead of fifteen</li>'
   '<li class="bs">targeting a country they cannot ship to</li></ul>')
 +cell(1,13,7,9,'<div class="d">One of those is <em>our app.</em></div>','ink'),
 'Read the list slowly and let them hear it. Then land the last panel.',
 num='25c'),

slide(
 cell(1,13,1,3,'<div class="l mut">Read it again</div>'
   '<div class="st mt">&ldquo;A loyalty button that is 10% off if you claim it &mdash; but the checkout button '
   'is here, and a support button there, and the only spot you can click is <em>this little spot.</em>&rdquo;</div>'
   '<div class="bs mt mut">&mdash; and that is a conversion killer.</div>')
 +cell(1,7,3,7,'<div class="ch">Our widget can be the reason<br>their checkout is failing.</div>'
   '<div class="b mt2">Which is why <b>placement is not a preference.</b> It costs the merchant money.</div>','lemon')
 +cell(7,13,3,7,'<div class="c3">So when a merchant says<br>&ldquo;can you move the widget?&rdquo;</div>'
   '<div class="b mt2">That is <b>not</b> fussiness. They may have watched their conversion rate fall.</div>'
   '<div class="ch mt2 lem">Move it &mdash; then ask what changed.</div>','ink')
 +cell(1,13,7,9,'<div class="st">The one app on their site you are responsible for '
   'is on the shortlist of things that break checkout.</div>'
   '<div class="b mt mut">Nobody else in this company is going to tell them. You will be the one who sees it.</div>'),
 'This is the most uncomfortable slide in session one and the most useful. It converts an annoying ticket — move the widget — into a real signal, and it makes them the person who catches it.',
 num='25d'),
]

_DIAGNOSE = slide(
 cell(1,13,1,3,'<div class="l mut">Every merchant message you will ever get is one of these</div>'
   '<div class="t mt">A <em>symptom.</em> Never a cause.</div>')
 +cell(1,7,3,6,'<div class="c3">What lands in your queue</div><div class="rule"></div>'
   '<div class="bs">&ldquo;Rewards aren&rsquo;t working&rdquo;</div>'
   '<div class="bs">&ldquo;Conversion is down&rdquo;</div>'
   '<div class="bs">&ldquo;Sales are flat&rdquo;</div>'
   '<div class="bs">&ldquo;People aren&rsquo;t coming back&rdquo;</div>'
   '<div class="bs">&ldquo;The widget looks wrong&rdquo;</div>')
 +cell(7,13,3,6,'<div class="c3">What is actually true</div><div class="rule"></div>'
   '<div class="b">Each one has <b>a cause somewhere on the path</b> &mdash; and it is almost never '
   'where the merchant is pointing.</div>','lemon')
 +cell(1,13,6,9,'<div class="st">Today: a shop you have never seen. Find what is <em>actually</em> wrong. '
   'Then say <em>which one to fix first.</em></div>'
   '<div class="b mt mut">Not to fix it yourself &mdash; to find it, name it, and rank it. '
   'That is the whole job, and nobody else in the company is doing it.</div>','ink'),
 'Set the frame before any content. Every complaint is a symptom. The path is where causes live. And the skill that separates an AM is not finding problems — it is knowing which one matters most.',
 num='02')

_RANK = slide(
 cell(1,13,1,3,'<div class="l mut">Finding problems is the easy half</div>'
   '<div class="t mt">Which one do you <em>fix first?</em></div>')
 +cell(1,7,3,7,'<div class="c3">Rank by two things only</div><div class="rule"></div>'
   '<div class="b"><b>1 &middot; How many people does it lose?</b><br>'
   '<span class="mut">90 of 100 left at the product page. Nothing else on the site is close.</span></div>'
   '<div class="b mt2"><b>2 &middot; What does it cost to fix?</b><br>'
   '<span class="mut">Three bullets and better photos cost nothing. A subscription programme costs months.</span></div>')
 +cell(7,13,3,7,'<div class="ch">So the order is usually</div>'
   '<div class="rule"></div>'
   '<div class="bs">1. something is <b>broken</b> &mdash; free to fix, fix today</div>'
   '<div class="bs">2. the <b>product page</b> &mdash; free, biggest leak</div>'
   '<div class="bs">3. <b>shipping and checkout</b> &mdash; cheap, second biggest</div>'
   '<div class="bs">4. <b>AOV</b> &mdash; bundles, thresholds</div>'
   '<div class="bs">5. <b>coming back</b> &mdash; slowest, and where we live</div>','ink')
 +cell(1,13,7,9,'<div class="st">Notice where <em>we</em> come.</div>'
   '<div class="b mt mut">Last. A merchant with a broken checkout button does not need a loyalty program &mdash; '
   'and if we sell them one, it will not work, and they will be right to blame us. '
   '<b>Recommending someone else&rsquo;s fix first is how you earn the conversation about ours.</b></div>','lemon'),
 'This is the most senior thing in the session. Anyone can list problems. Ranking them by people-lost and cost-to-fix is judgement — and being honest that we come last is what makes the recommendation credible when we finally do come up.',
 num='15')

# ── audit a winner first: an ICP-matched store, and a Plus store ──
_WINNER = [
slide(
 cell(1,13,1,3,'<div class="l mut">Before we go looking for what is broken</div>'
   '<div class="t mt">You cannot see <em>wrong</em><br>until you have seen <em>right.</em></div>')
 +cell(1,7,3,7,'<div class="c3">What we could do</div><div class="rule"></div>'
   '<div class="b">Hand you a list of faults and send you hunting. You would find some &mdash; and have '
   'no idea whether the rest of the shop was fine or a disaster.</div>')
 +cell(7,13,3,7,'<div class="c3">What we are going to do</div><div class="rule"></div>'
   '<div class="b">Audit <b>a store that matches our ICP</b>, all the way through. '
   'That becomes the picture you compare everything else against.</div>','lemon')
 +cell(1,13,7,9,'<div class="st">Every diagnosis is a <em>comparison.</em> First you need something to compare to.</div>','ink'),
 'Give a room a checklist of faults and they become fault-finders. Give them a working machine first and they can tell the difference - which is the actual skill.'),

slide(
 cell(1,6,1,6,'<div class="l mut">An ICP-matched store</div>'
   '<div class="t mt">Crown<br>Affair</div>'
   '<div>'+link('crownaffair.com')+'</div>'
   '<div class="rule"></div>'
   '<div class="b">Haircare. Oil, shampoo, tools. Things that <b>run out</b>.</div>'
   '<div class="bs mt2 mut">Free shipping $75 &mdash; just above their average order. Deliberate.</div>')
 +cell(6,13,1,6,img(CROWN),'photo')
 +cell(1,13,6,9,'<div class="st">Fill the sheet as we go. Same questions &mdash; on a shop that <em>works.</em></div>'),
 'Open the real site and let them look before you say anything. Ask what they notice first - usually the quiz.',
 kicker='Open it live'),

slide(
 cell(1,13,1,2,'<div class="l mut">Every step, and what is doing the job</div>')
 +cell(1,5,2,5,'<div class="c3">Get people in</div><div class="rule"></div>'
   '<div class="bs"><b>Klaviyo</b> &mdash; email at scale</div>'
   '<div class="bs"><b>Attentive + Postscript</b> &mdash; SMS</div>')
 +cell(5,9,2,5,'<div class="c3">On the site</div><div class="rule"></div>'
   '<div class="bs"><b>A product quiz</b> &mdash; find your hair type</div>'
   '<div class="bs"><b>Okendo</b> &mdash; reviews with faces</div>')
 +cell(9,13,2,5,'<div class="c3">Pay</div><div class="rule"></div>'
   '<div class="bs"><b>Bundles</b> &mdash; pre-built sets</div>'
   '<div class="bs"><b>Free shipping $75</b></div>')
 +cell(1,5,5,8,'<div class="c3">After the order</div><div class="rule"></div>'
   '<div class="bs"><b>Gorgias</b> &mdash; support with order context</div>')
 +cell(5,9,5,8,'<div class="c3">Come back</div><div class="rule"></div>'
   '<div class="bs"><b>Recharge</b> &mdash; subscribe and refill</div>'
   '<div class="bs">the product genuinely runs out</div>','lemon')
 +cell(9,13,5,8,'<div class="c3">Money</div><div class="rule"></div>'
   '<div class="bs">bundles raise the basket, subscription raises the lifetime</div>')
 +cell(1,13,8,9,'<div class="c3">Nothing here is an accident. Somebody chose each one &mdash; and pays for it monthly.</div>','ink'),
 'Walk each box on the real site. This is the reference model: a full machine, every step covered. When they read a broken shop next, the gaps will be obvious because this picture is in their head.'),

slide(
 cell(1,13,1,3,'<div class="l mut">So what is missing?</div>'
   '<div class="t mt">Type <em>/pages/rewards</em>.</div>')
 +cell(1,7,3,7,'<div class="n-lg">404</div>'
   '<div class="ls mut">no loyalty &middot; and no competitor installed either</div>','lemon')
 +cell(7,13,3,7,'<div class="ch">A shop doing nearly everything right</div>'
   '<div class="b mt2">Quiz, reviews, bundles, email, SMS, subscription, support, a threshold set on purpose.</div>'
   '<div class="b mt2">And <b>nothing</b> giving a customer a reason to choose <b>them</b> over the next haircare brand.</div>','ink')
 +cell(1,13,7,9,'<div class="st">That gap is the whole reason this job exists.</div>'
   '<div class="b mt mut">Not because their shop is bad &mdash; because it is <b>good</b>, and they have '
   'run out of the easy fixes. <b>This is what a merchant ready for us looks like from the outside.</b></div>'),
 'This is the payoff. They now know what ready-for-us looks like - not a struggling shop, a strong one with one gap. Session four turns this into the ICP checklist.',
 kicker='Open it live'),

slide(
 cell(1,5,1,6,'<div class="l mut">What a Plus store looks like</div>'
   '<div class="t mt">HexClad</div>'
   '<div>'+link('hexclad.com')+'</div>'
   '<div class="rule"></div>'
   '<div class="bs">Bigger merchant, bigger stack &mdash; readable from the source in a minute.</div>')
 +cell(5,9,1,6,img(HEXCLAD),'photo')
 +cell(9,13,1,6,'<div class="c3">How to tell it is Plus</div><div class="rule"></div>'
   '<ul><li class="bs"><b>Checkout extensions</b> &mdash; the checkout itself is customised</li>'
   '<li class="bs"><b>Markets</b> &mdash; more than one country and currency</li>'
   '<li class="bs"><b>B2B</b> on the same store</li>'
   '<li class="bs">Shop Pay everywhere, many payment options</li>'
   '<li class="bs">A deeper stack &mdash; and usually a competitor already in it</li></ul>','lemon')
 +cell(1,13,6,9,'<div class="st">Why it matters: a Plus merchant asking about <em>checkout</em> is asking a real question.</div>'
   '<div class="b mt mut">The same question from a standard-plan merchant often has no answer &mdash; '
   'their checkout cannot be changed. Knowing which one you are talking to saves everybody a week.</div>','ink'),
 'Standard Shopify checkout is mostly fixed; Plus can be customised with extensions and scripts. If CS cannot tell the difference they will promise things that are impossible, or refuse things that are easy.',
 kicker='Open it live'),

slide(
 cell(1,13,1,3,'<div class="d">Now you have a <em>picture</em><br>in your head.</div>')
 +cell(1,13,3,6,'<div class="st">Everything from here is: what does this shop have that Crown Affair has &mdash; '
   'and what is <em>missing?</em></div>')
 +cell(1,13,6,9,'<div class="b">That is what diagnosis actually is. Not spotting faults. '
   '<b>Comparing against a machine you already understand.</b></div>'
   '<div class="b mt2 mut">It works both ways &mdash; sometimes the shop you are reading has something '
   'Crown Affair does not, and that is worth noticing too.</div>','ink'),
 'Hold this frame for the rest of the session. Every decoder row, every leak, every broken checkout is a comparison against the working machine they just walked.'),
]

# ── one deep dive per decoder row ──
_DD_AOV = slide(
 cell(1,13,1,3,'<div class="l mut">Decoder row &middot; low AOV</div>'
   '<div class="t mt">Not enough money <em>per order.</em></div>')
 +cell(1,7,3,7,'<div class="c3">The fixes, fastest first</div><div class="rule"></div>'
   '<ul><li class="bs"><b>Multi-packs</b> &mdash; a 4-pack or 6-pack at a discount instead of one unit</li>'
   '<li class="bs"><b>Pre-built pairs</b> &mdash; moisturizer + exfoliator, chosen for them</li>'
   '<li class="bs"><b>Variation packs</b> &mdash; three colours of the lip gloss in one box</li>'
   '<li class="bs">Upsell <b>in cart</b>, <b>on site</b>, and in the <b>popup</b></li>'
   '<li class="bs">Cross-sell into things that pair</li></ul>')
 +cell(7,13,3,5,'<div class="ch">The threshold rule</div>'
   '<div class="b mt">If their average order is <b>$39</b>, set free shipping at <b>$40</b>.</div>'
   '<div class="bs mt">She has to spend one dollar more &mdash; so she adds a $15 item.</div>','lemon')
 +cell(7,13,5,7,'<div class="c3">And gift thresholds</div>'
   '<div class="bs mt">Spend $100, get a free hat. Spend $150, get something better.</div>','ink')
 +cell(1,13,7,9,'<div class="st">A floor worth knowing: below about <em>$35</em> an order, almost nothing scales.</div>'
   '<div class="b mt mut">The ad cost and the shipping eat it. When a merchant with a $22 average order asks '
   'why ads are not working &mdash; that is usually the answer, and it is not an ads problem.</div>'),
 'This is the fastest lever in ecom and it needs no new traffic. Note the threshold rule precisely: one dollar above where their average order already sits. Set it lower and it does nothing; set it far higher and it reads as a wall.',
 num='dd1')

_DD_ROAS = slide(
 cell(1,13,1,3,'<div class="l mut">Decoder row &middot; low ROAS, but clicks and CVR are fine</div>'
   '<div class="t mt">Nothing is broken.</div>')
 +cell(1,7,3,6,'<div class="c3">Read the whole set together</div><div class="rule"></div>'
   '<table style="font-size:23px">'
   '<tr><td>Cheap reach</td><td class="r">&#10003;</td></tr>'
   '<tr><td>Good clicks</td><td class="r">&#10003;</td></tr>'
   '<tr><td>Good conversion &mdash; 4%</td><td class="r">&#10003;</td></tr>'
   '<tr class="tot"><td>Return on ad spend</td><td class="r">1.2&times;</td></tr></table>')
 +cell(7,13,3,6,'<div class="ch">So what is left?</div>'
   '<div class="st mt2">They are not making <em>enough money per customer.</em></div>','lemon')
 +cell(1,13,6,9,'<div class="d">Double AOV $35 &rarr; $70 and ROAS goes <em>1.2 &rarr; 2.4</em></div>'
   '<div class="st mt">&mdash; without touching the ads at all.</div>','ink'),
 'Everything looks healthy and the business still does not work. This is the case where a merchant blames the ads and everybody wastes a month on creative. The number to fix is the basket, not the campaign.',
 num='dd2')

_DD_NORMAL = slide(
 cell(1,13,1,3,'<div class="l mut">Decoder row &middot; low conversion, high AOV</div>'
   '<div class="t mt">This one is <em>normal.</em><br>Do not panic. Do not escalate.</div>')
 +cell(1,7,3,7,'<div class="c3">The example to remember</div><div class="rule"></div>'
   '<div class="b">A <b>$1,700</b> portable basketball shooting machine.</div>'
   '<div class="b mt2">It is never going to convert like a $30 candle. '
   'Nobody buys one on a Tuesday because they saw a reel.</div>')
 +cell(7,13,3,7,'<div class="c3 lem">And it still works</div>'
   '<div class="b mt2">Cheap reach, plenty of clicks, few buyers &mdash; but each one is worth so much '
   'that the maths is fine on their costs.</div>'
   '<div class="bs mt2">Payment plans nudge it up a little. That is all it needs.</div>','ink')
 +cell(1,13,7,9,'<div class="st">Knowing which numbers are <em>supposed</em> to look bad is part of the job.</div>'
   '<div class="b mt mut">A merchant panicking about a 0.4% conversion rate on a $1,700 product '
   'needs reassurance, not a fix &mdash; and being the person who can say that calmly is worth a lot.</div>','lemon'),
 'This is the counterweight to everything else in the session. Not every bad-looking number is a problem, and an AM who cannot tell the difference will send merchants chasing ghosts.',
 num='dd3')

# ── the real board: every field, filed by funnel step ──
_STACKMAP = [
slide(
 cell(1,13,1,2,'<div class="l mut">The short list was seven apps. Here is the real board.</div>'
   '<div class="t mt">~28 fields. <em>One</em> of them is ours.</div>')
 +cell(1,4,2,7,'<div class="ls lem">GET PEOPLE IN</div><div class="rule"></div>'
   '<div class="bs"><b>Creator/affiliate</b><br><span class="mut">GOAFFPRO &middot; Refersion &middot; Superfiliate</span></div>'
   '<div class="bs mt"><b>Attribution</b><br><span class="mut">Northbeam &middot; Triple Whale</span></div>'
   '<div class="bs mt"><b>Server-side events</b><br><span class="mut">Elevar</span></div>'
   '<div class="bs mt"><b>Post-purchase survey</b><br><span class="mut">Fairing</span></div>','ink')
 +cell(4,7,2,7,'<div class="ls mut">ON THE SITE</div><div class="rule"></div>'
   '<div class="bs"><b>Capture</b><br><span class="mut">Alia &middot; Privy &middot; Dotdigital</span></div>'
   '<div class="bs mt"><b>Reviews</b><br><span class="mut">Okendo &middot; Judge.me &middot; Fera &middot; Yotpo Reviews</span></div>'
   '<div class="bs mt"><b>Quiz</b> <span class="mut">Octane AI</span> &middot; <b>Video</b> <span class="mut">Tolstoy</span></div>'
   '<div class="bs mt"><b>Search</b> <span class="mut">Algolia &middot; Nosto</span></div>'
   '<div class="bs mt"><b>Landing</b> <span class="mut">PageFly &middot; Replo &middot; Weaverse</span></div>')
 +cell(7,10,2,7,'<div class="ls mut">PAY</div><div class="rule"></div>'
   '<div class="bs"><b>Subscriptions</b><br><span class="mut">Recharge &middot; Skio &middot; Appstle</span></div>'
   '<div class="bs mt"><b>Bundles/upsell</b> <span class="mut">Rebuy</span></div>'
   '<div class="bs mt"><b>Checkout</b> <span class="mut">Checkout Blocks &middot; Shop Pay</span></div>'
   '<div class="bs mt"><b>BNPL</b> <span class="mut">Klarna &middot; Afterpay</span></div>'
   '<div class="bs mt"><b>Price testing</b> <span class="mut">Intelligems</span></div>'
   '<div class="bs mt"><b>Tax &middot; Cross-border</b> <span class="mut">Avalara &middot; Global-e</span></div>')
 +cell(10,13,2,7,'<div class="ls mut">AFTER THE ORDER</div><div class="rule"></div>'
   '<div class="bs"><b>Tracking</b> <span class="mut">AfterShip</span></div>'
   '<div class="bs mt"><b>Order editing</b> <span class="mut">Order Editing</span></div>'
   '<div class="bs mt"><b>Returns</b><br><span class="mut">Loop &middot; Happy Returns &middot; Redo</span></div>'
   '<div class="bs mt"><b>Support</b> <span class="mut">Gorgias</span></div>'
   '<div class="rule"></div><div class="ls lem">COME BACK &mdash; ours</div>'
   '<div class="bs mt"><b>Email</b> <span class="mut">Klaviyo &middot; Drip</span> &middot; <b>SMS</b> <span class="mut">Attentive &middot; Postscript</span></div>'
   '<div class="bs mt"><b>Loyalty</b><br><span class="mut">Joy &middot; Smile &middot; Rivo &middot; LoyaltyLion &middot; Yotpo &middot; BON</span></div>','lemon')
 +cell(1,13,7,9,'<div class="st">A merchant&rsquo;s day is spent on the <em>other twenty-seven.</em></div>'
   '<div class="b mt mut">If we walk in talking only about points, we are talking about about 4% of their board. '
   'The AM read is the whole board &mdash; which is why you learn the path before you learn the app.</div>','ink'),
 'This is the scale check. Not a criticism of Joy — a reminder that our field is one worry among many, and that six named competitors all ship the same points, tiers and referrals. That is session one argument made concrete: the app cannot be why they choose us.',
 num='28a'),

slide(
 cell(1,13,1,2,'<div class="l mut">A name in the source is a signal, not a verdict</div>'
   '<div class="t mt">Same word. <em>Opposite</em> conclusion.</div>')
 +cell(1,7,2,6,'<div class="ch">yotpo-product-reviews</div><div class="rule"></div>'
   '<div class="b">Yotpo <b>Reviews</b> &mdash; on-site trust. Nothing to do with loyalty.</div>'
   '<div class="bs mt2 mut">Rae Wellness runs exactly this, and has <b>no</b> loyalty program.</div>')
 +cell(7,13,2,6,'<div class="ch">loyalty-program &middot; swell &middot; Rivo.global_config</div><div class="rule"></div>'
   '<div class="b">Yotpo <b>Loyalty</b> / Rivo / Smile &mdash; <b>a competitor is installed.</b></div>'
   '<div class="bs mt2">HexClad runs exactly this.</div>','ink')
 +cell(1,13,6,9,'<div class="st">Confirm <em>which product</em> before you tell anyone a brand already has loyalty.</div>'
   '<div class="b mt mut">And check it is switched <b>on</b> &mdash; a disabled flag in the source is not a live install. '
   'Getting this wrong on a call is the fastest way to lose a merchant&rsquo;s trust.</div>','lemon'),
 'Yotpo sells reviews, SMS and loyalty as separate products. Four false Rivo hits have been observed from dead theme CSS alone. This slide is what separates a careful read from a guess.',
 num='28b'),

slide(
 cell(1,7,1,6,'<div class="l mut">One job, taken to ten out of ten</div>'
   f'<div class="mt">{logo("alia",64)}</div>'
   '<div class="t">Alia</div>'
   '<div class="bs mut" style="font-family:\'JetBrains Mono\',monospace">field: capture &mdash; a popup</div>'
   '<div class="rule"></div>'
   '<div class="b">Everyone ships a popup. Alia&rsquo;s whole company rests on noticing what a normal one <b>does</b>.</div>')
 +cell(7,13,1,6,'<div class="ch">&ldquo;Blanket discount popups buy signups that never convert &mdash; '
   'and <em>train shoppers to wait for 15% off.</em>&rdquo;</div>'
   '<div class="bs mt2">Their words, not ours.</div>','lemon')
 +cell(1,13,6,9,'<div class="st">That is <b>fear #2</b>, and the deals trap, in one sentence.</div>'
   '<div class="b mt2 mut">Alia did not build a better popup. They noticed the popup was <b>causing</b> '
   'the merchant&rsquo;s problem &mdash; so they made the coupon <b>earned</b> instead of given. '
   'Then went deep, not wide: twelve researched formats, AI triggering, testing. One job, done to ten.</div>','ink'),
 'The question is never "what does this app do". It is "what does this app BELIEVE?" Alia believes a blanket discount is a leak. Joy has to be able to say what it believes too — and if nobody in the room can, that is the finding.',
 num='28c'),

slide(
 cell(1,7,1,4,'<div class="l mut">An app that exists because of <em>one ticket</em></div>'
   f'<div class="mt">{logo("shopify",56)}</div>'
   '<div class="t">Order<br>Editing</div>'
   '<div class="bs mut" style="font-family:\'JetBrains Mono\',monospace">one job: let her fix an unfulfilled order</div>')
 +cell(7,13,1,4,'<div class="b">&ldquo;A wrong address, size, variant or forgotten item becomes a support ticket '
   '&mdash; and can turn into a <b>mis-shipment</b> if the warehouse acts first.&rdquo;</div>'
   '<div class="bs mt2">You have all worked this ticket. Somebody built a company around it.</div>','lemon')
 +cell(1,13,4,7,'<table style="font-size:24px">'
   '<tr><td>She mistypes her address</td><td class="r mut">30 seconds of her time</td></tr>'
   '<tr><td>She emails support</td><td class="r mut">a ticket in your queue</td></tr>'
   '<tr><td>The warehouse ships first</td><td class="r mut">a parcel in the wrong place</td></tr>'
   '<tr><td>Refund or reship</td><td class="r">the order&rsquo;s whole margin, gone</td></tr>'
   '<tr class="tot"><td>She tells someone</td><td class="r">and leaves a review</td></tr></table>','flat')
 +cell(1,13,7,9,'<div class="st">A ticket is never just a ticket. It has a <em>cost downstream</em> &mdash; '
   'and that cost is why the app exists.</div>'
   '<div class="b mt mut">See the chain and you stop clearing tickets and start reading them as '
   '<b>evidence about the business</b>. That is the whole difference between the two jobs.</div>','ink'),
 'Use this one with our team specifically — they have lived it. It is the moment "apps are solutions" stops being abstract, because they already know the pain the solution was built for.',
 num='28d'),
]

# ── the question under all the others: is the product worth returning to? ──
_PRODUCT = [
slide(
 cell(1,13,1,3,'<div class="l mut">Before a single channel, a single point, a single email</div>'
   '<div class="t mt">Why would she buy it <em>again?</em></div>')
 +cell(1,7,3,6,'<div class="ch">&ldquo;Because she liked it.&rdquo;</div>'
   '<div class="rule"></div>'
   '<div class="b">That is the whole answer. Everything else in this session is <b>a way of reminding her</b> '
   'of something she already wants.</div>')
 +cell(7,13,3,6,'<div class="ch">So the real question is</div>'
   '<div class="st mt2">Did she <em>like it?</em><br>Do we <em>know?</em></div>','lemon')
 +cell(1,13,6,9,'<div class="d">A loyalty program is a multiplier.</div>'
   '<div class="st mt">Multiply a small base and it is still small.<br>'
   'Multiply a <em>bad product</em> and it is still <em>nothing.</em></div>','ink'),
 'This is the honest first answer and almost nobody gives it, because it is not sellable. If the product does not earn a second purchase, no mechanism creates one. Points on a product she did not like just means you paid her to be disappointed twice. Say it plainly — the room will trust everything after it more.',
 num='04a'),

slide(
 cell(1,13,1,2,'<div class="l mut">Six reasons she does not come back &mdash; in the order you should check them</div>')
 +cell(1,13,2,3,'<div class="frow"><div class="fbar" style="width:82px">1</div>'
   '<div class="bs"><b>The product is not good enough.</b> '
   '<span class="mut">She used it and was not impressed. &rarr; fix the product. Nothing else works.</span></div></div>','flat')
 +cell(1,13,3,4,'<div class="frow"><div class="fbar" style="width:82px">2</div>'
   '<div class="bs"><b>She never actually used it.</b> '
   '<span class="mut">It is in a drawer. &rarr; onboarding, the &ldquo;how to use it&rdquo; email.</span></div></div>','flat')
 +cell(1,13,4,5,'<div class="frow"><div class="fbar" style="width:82px">3</div>'
   '<div class="bs"><b>There is no natural repeat.</b> '
   '<span class="mut">A mattress, even a great one. &rarr; accessories, range, referral &mdash; not points.</span></div></div>','flat')
 +cell(1,13,5,6,'<div class="frow"><div class="fbar" style="width:82px">4</div>'
   '<div class="bs"><b>She forgot.</b> '
   '<span class="mut">She would buy again and it never crossed her mind. &rarr; email, SMS, the week-6 reminder.</span></div></div>','flat')
 +cell(1,13,6,7,'<div class="frow"><div class="fbar win" style="width:82px">5</div>'
   '<div class="bs"><b>No reason to choose <em>you</em> over the alternative.</b> '
   '<span class="mut">She is buying &mdash; from somebody. &rarr; <b>this is where we live.</b></span></div></div>','flat')
 +cell(1,13,7,8,'<div class="frow"><div class="fbar" style="width:82px">6</div>'
   '<div class="bs"><b>She would, but it is a hassle.</b> '
   '<span class="mut">&rarr; subscription &mdash; agree the next one in advance.</span></div></div>','flat')
 +cell(1,13,8,9,'<div class="c3">Everything above rung 5 has to be true <em>before</em> our product does anything at all.</div>','ink'),
 'Work down the list with a real merchant and you will usually stop above rung five. That is not bad news — it is the most useful thing you can tell them, and it is the thing a salesperson will not say.',
 num='04b'),

slide(
 cell(1,7,1,6,'<div class="l mut">And you can check rung 1 from outside</div>'
   '<div class="t mt">Read the <em>reviews</em> &mdash; but read the <b>complaints.</b></div>'
   '<div class="b mt2">Not the star rating. The one- and two-star text, and the recent ones.</div>')
 +cell(7,13,1,3,'<div class="c3">Complaints about shipping, packaging, support</div>'
   '<div class="bs mt">The product is fine. The <b>operation</b> is leaking. Rungs 2&ndash;6 are live options.</div>','lemon')
 +cell(7,13,3,6,'<div class="c3">Complaints about the product itself</div>'
   '<div class="bs mt">&ldquo;did not work for me&rdquo; &middot; &ldquo;not worth the price&rdquo; &middot; &ldquo;broke&rdquo;</div>'
   '<div class="bs mt"><b>Retention work is premature.</b> Say so.</div>','ink')
 +cell(1,13,6,9,'<div class="st">Reviews are the only honest thing on a product page &mdash; '
   'and they are <em>public.</em></div>'
   '<div class="b mt mut">Which means you can answer &ldquo;is this product worth coming back to?&rdquo; '
   'in three minutes, for free, before anybody asks you about points.</div>'),
 'This is the outside-in test for rung one. And it is a genuinely uncomfortable finding to deliver — you are telling a merchant their product is the problem. Do it anyway, gently, with the reviews on screen so it is their customers saying it, not you.',
 num='04c'),
]

# ── the ways back: inserted after the brand beat, before "why would a human buy twice" ──
WAYS = [
slide(
 cell(1,13,1,2,'<div class="l mut">Before we talk about loyalty</div>'
   '<div class="t mt">How many ways are there to <em>bring her back?</em></div>')
 +cell(1,5,2,6,'<div class="l">Owned</div><div class="rule"></div>'
   +logorow([('klaviyo','email'),('attentive','SMS'),('smile','loyalty')],34)+
   '<div class="b">&hellip; and her account</div>'
   '<div class="bs mt2">You can reach her again for <b>almost nothing</b>, forever.</div>','lemon')
 +cell(5,9,2,6,'<div class="c3">Rented</div><div class="rule"></div>'
   '<div class="b">organic social &middot; community &middot; creators</div>'
   '<div class="bs mt2 mut">You built the audience. <b>The algorithm decides</b> who sees it.</div>')
 +cell(9,13,2,6,'<div class="c3">Paid</div><div class="rule"></div>'
   '<div class="b">retargeting ads &middot; paid partnerships</div>'
   '<div class="bs mt2 mut">Works immediately. <b>You pay every single time.</b></div>','ink')
 +cell(1,13,6,9,'<div class="st">The diagnostic question:</div>'
   '<div class="ch mt2 lem">How many ways can this shop reach a past customer <em>for free?</em></div>'
   '<div class="b mt2 mut">If the answer is none, that is the finding &mdash; and it is bigger than any loyalty program.</div>','ink'),
 'This is the map for the next ten minutes. Owned, rented, paid. Every merchant conversation about "getting people back" lives in one of these three columns, and most merchants have never separated them.', num='05'),

slide(
 cell(1,13,1,2,'<div class="t">The cost of one message</div>')
 +cell(1,13,2,6,'<table>'
   '<tr><th>Channel</th><th>Roughly costs</th><th>Reach it gets</th><th>Use it for</th></tr>'
   f'<tr><td>{logo("klaviyo",34)}<b>Email</b></td><td>fractions of a cent</td><td>~20&ndash;40% opened</td><td>everything &mdash; the default</td></tr>'
   f'<tr><td>{logo("attentive",34)}{logo("postscript",34)}<b>SMS</b></td><td>cents per message</td><td><b>~90%+ read, in minutes</b></td><td>time-boxed moments only</td></tr>'
   '<tr><td><b>WhatsApp</b></td><td>per conversation</td><td>very high, conversational</td><td>markets where it <b>is</b> the phone</td></tr>'
   '<tr><td><b>Retargeting</b></td><td>real money, every time</td><td>whoever still matches</td><td>people who did not convert</td></tr>'
   '<tr><td class="mut">Organic social</td><td class="mut">time, not money</td><td class="mut">whatever the algorithm gives</td><td class="mut">staying in mind</td></tr>'
   '</table>','flat')
 +cell(1,13,6,9,'<div class="st">Email is not the best channel. It is the <em>cheapest</em> one.</div>'
   '<div class="b mt2 mut">Which is why it is the default, why every merchant runs Klaviyo, '
   'and why an email list is the most valuable thing a small shop owns.</div>','ink'),
 'Do not let them think email is old-fashioned. It is the only channel where sending to everyone costs almost nothing, which means it is the only one you can use every week without going broke.', num='06'),

slide(
 cell(1,7,1,5,'<div class="l mut">SMS</div><div class="t mt">Read in <em>minutes.</em></div>'
   '<div class="b mt2">Roughly a hundred times more expensive per message than email &mdash; '
   'and read by almost everyone, almost immediately.</div>')
 +cell(7,13,1,5,'<div class="c3 lem">So use it for</div>'
   '<ul><li class="bs">a drop going live</li><li class="bs">a sale ending today</li>'
   '<li class="bs">back in stock</li><li class="bs">an order problem</li></ul>','ink')
 +cell(1,13,5,9,'<div class="ch">Never for a newsletter.</div>'
   '<div class="b mt2">Overuse and she does not just ignore it &mdash; <b>she unsubscribes</b>, '
   'and you have lost the most powerful channel you had, permanently. '
   'A merchant asking &ldquo;can I text everyone weekly?&rdquo; is about to burn an asset.</div>','lemon'),
 'The asymmetry matters: an ignored email costs nothing, an unwanted SMS costs you the channel. That is why the rules are different.', num='07'),

slide(
 cell(1,7,1,6,'<div class="l mut">WhatsApp</div><div class="t mt">For most of the world,<br>this <em>is</em> the phone.</div>'
   '<div class="b mt2">Vietnam, India, Brazil, Indonesia, most of Europe, most of Latin America. '
   'Not the US &mdash; which is why US-centric advice keeps missing it.</div>')
 +cell(7,13,1,4,'<div class="c3">What makes it different</div>'
   '<div class="bs mt">Support and selling happen in <b>the same thread</b>. She can just reply. '
   'It reads like a person, not a broadcast.</div>')
 +cell(7,13,4,6,'<div class="c3">What it demands</div>'
   '<div class="bs mt">Explicit opt-in, and pre-approved templates for anything you send first. '
   'You cannot just blast.</div>','ink')
 +cell(1,13,6,9,'<div class="st">If a merchant sells into these markets and is <em>only</em> doing email, '
   'they are missing the channel their customers actually live in.</div>','lemon'),
 'This is a place where our team has an advantage over US-based competitors — they use WhatsApp themselves and understand it natively.', num='08'),

slide(
 cell(1,7,1,5,'<div class="l mut">Retargeting</div>'
   '<div class="t mt">Not paying to <em>find</em> her.</div>'
   '<div class="b mt2">Paying to <b>remind</b> her. She is already matched &mdash; from the pixel, '
   'or from the email list uploaded as an audience.</div>')
 +cell(7,13,1,5,'<div class="c3 lem">Why it is cheaper</div>'
   '<div class="bs mt">Prospecting pays to reach strangers, most of whom will never care. '
   'Retargeting reaches people who <b>already raised a hand</b>.</div>'
   '<div class="bs mt">Same ad money, far better odds.</div>','ink')
 +cell(1,13,5,9,'<div class="ch">But it is shrinking.</div>'
   '<div class="b mt2">Privacy changes mean fewer people can be matched at all. '
   'Every year, <b>a bigger share of &ldquo;come back&rdquo; has to happen on channels you own</b> '
   '&mdash; which is the whole argument for email, SMS, and an account she logs into.</div>','lemon'),
 'This is the strategic point: the paid route to bringing people back is getting less reliable, so the owned route matters more every year. That is a tailwind for us.', num='09'),

slide(
 cell(1,7,1,6,'<div class="l mut">Organic social &amp; content</div>'
   '<div class="t mt">Rented reach.</div>'
   '<div class="b mt2">Free in money. <b>Expensive in time.</b> And you do not control who sees it &mdash; '
   'you built the audience, the algorithm decides.</div>')
 +cell(7,13,1,3,'<div class="c3">What it is good at</div>'
   '<div class="bs mt">Staying in her head <b>between</b> purchases, so that when the need comes back, '
   'you are the name she already knows.</div>')
 +cell(7,13,3,6,'<div class="c3">What it cannot do</div>'
   '<div class="bs mt">Reach a <b>specific</b> customer at a <b>specific</b> moment. '
   'You cannot post at one person who is about to run out.</div>','ink')
 +cell(1,13,6,9,'<div class="b">Which is exactly the gap email, SMS and loyalty fill. '
   'Social makes her <b>remember</b> you. Owned channels make her <b>buy</b>.</div>','lemon'),
 'Merchants often over-invest here because it feels like marketing. It builds memory, not orders. Both matter — but do not let them confuse the two.', num='10'),

slide(
 cell(1,13,1,2,'<div class="t">Deals and sales &mdash; the fastest way, and <em>the most dangerous</em></div>')
 +cell(1,7,2,6,'<div class="c3 lem">It works immediately</div>'
   '<div class="b mt">Nothing brings people back faster than money off. '
   'BFCM, a seasonal sale, a winback code &mdash; the orders arrive.</div>','ink')
 +cell(7,13,2,6,'<div class="c3">And then it keeps working</div>'
   '<div class="b mt">Which is the problem. Do it every November and people <b>learn to wait for November</b>. '
   'You did not discover demand. You <b>moved</b> it &mdash; and taught them the real price is lower.</div>','lemon')
 +cell(1,13,6,9,'<div class="st">This is <em>fear #2</em>, at the scale of a whole calendar.</div>'
   '<div class="b mt2 mut">A merchant whose only way back is a sale has not built retention. '
   'They have built a habit of waiting. That is the conversation to have with them &mdash; '
   'and it is the one nobody else is having.</div>','ink'),
 'This is one of the most useful things you can say to a merchant, and almost nobody says it. Everyone sells them more discounting tools.', num='11'),
]

# ═════════════════ SESSION 3 — BRING IT TOGETHER ═════════════════
S4=[
TITLE('Goal: given a real merchant, say whether it is ours, whether it needs us, and what to do. Today: two brands side by side, one of which we should turn down.',
 'Session Four','Bring it<br><em>together</em>',
 ('A real merchant. A real call.','Two brands side by side &mdash; and one of them we are going to turn down.'),'The<br>verdict'),

slide(
 cell(1,8,1,6,'<div class="l mut">Two sessions ago you could not do any of this</div>'
   '<ul><li class="b">How does this shop make money on one order?</li>'
   '<li class="b">How do people arrive, and where do they quit?</li>'
   '<li class="b">Why would someone buy twice &mdash; and what is the brand doing about it?</li></ul>')
 +cell(8,13,1,6,'<div class="ch">Today we add the last one:</div>'
   '<div class="st mt2">So what do we <em>tell them?</em></div>','lemon')
 +cell(1,13,6,9,'<div class="st">And you still have not opened Joy <em>once.</em></div>','ink'),
 'Let that land. This is the moment the course pays off.', num='02'),

slide(
 cell(1,13,1,4,'<div class="d">Is Recharge a<br><em>subscription app?</em></div>')
 +cell(1,7,4,9,'<div class="n-sm">No.</div><div class="rule"></div>'
   '<div class="b">It is a solution for increasing <b>lifetime value</b>.</div>'
   '<div class="b mt">Klaviyo is not an email app &mdash; it is a cheap way to talk to everyone at scale, '
   'plus a CRM that remembers birthdays and order history.</div>','lemon')
 +cell(7,13,4,9,'<div class="ch">We do not sell an app.</div>'
   '<div class="ch mt2 lem">We sell the solution the app is <em>made of.</em></div>','ink'),
 'Let them say yes first. Then say no. Everything today depends on this reframe.',
 kicker='Ask the room', num='03'),

slide(
 cell(1,8,1,9,'<div class="l mut">Is it ours? Run the checklist</div><div class="rule"></div>'
   '<table>'
   '<tr><td>Shopify or Plus</td><td class="r mut">&#9744;</td></tr>'
   '<tr><td>Category that repurchases</td><td class="r mut">&#9744;</td></tr>'
   '<tr><td>Roughly $5&ndash;40M</td><td class="r mut">&#9744;</td></tr>'
   '<tr><td><b>Klaviyo or Attentive</b> installed</td><td class="r mut">&#9744;</td></tr>'
   '<tr><td>Growing &mdash; raise, press, retail, viral</td><td class="r mut">&#9744;</td></tr>'
   f'<tr><td><b>No</b> {logo("rivo",30)}{logo("yotpo",30)}{logo("smile",30)}{logo("loyaltylion",30)}</td><td class="r mut">&#9744;</td></tr></table>'
   '<div class="bs mt mut">beauty &middot; apparel &middot; wellness &middot; kids &middot; outdoor &middot; pet &middot; home</div>','flat')
 +cell(8,13,1,5,'<div class="ch">Every line is visible from the <em>public site.</em></div>'
   '<div class="b mt2">You never ask them. And you already know how to check every one &mdash; that was last session.</div>','lemon')
 +cell(8,13,5,9,'<div class="c3 lem">The easiest win to recognise</div>'
   +logorow([('recharge','Recharge'),('klaviyo','Klaviyo')],34)+
   '<div class="bs mt">&hellip; and <b>no loyalty app</b>.</div>'
   '<div class="bs mt">They already pay for repeat revenue and have nothing that gives a reason to return.</div>','ink'),
 'This is Joy real ICP, not something invented for class.', num='04'),

slide(
 cell(1,7,1,6,'<div class="l mut">The textbook case</div>'
   '<div class="t mt">rae<br>wellness</div><div>'+link('raewellness.co')+'</div><div class="rule"></div>'
   '<ul><li class="bs">Recharge, heavily used</li><li class="bs">Klaviyo</li>'
   '<li class="bs">Wellness &mdash; natural repurchase</li></ul>'
   '<div class="ch mt2">/pages/rewards<br><em>&rarr; 404</em></div>')
 +cell(7,13,1,6,img(RAE404),'photo')
 +cell(1,13,6,9,'<div class="st">Thirty seconds. No login. No discovery call.</div>'
   '<div class="b mt2 mut">Ctrl-F recharge &mdash; hit. klaviyo &mdash; hit. smile, loyaltylion, yotpo &mdash; nothing. '
   'Then type <b>/pages/rewards</b>. That 404 is the entire pitch, and <b>they found it themselves.</b></div>','ink'),
 'Do it live rather than showing the screenshot, if the wifi holds. The screenshot is the fallback.',
 kicker='Open it live', num='05'),

slide(
 cell(1,13,1,4,'<div class="d">But does this shop need<br>a loyalty program <em>at all?</em></div>')
 +cell(1,13,4,9,'<div class="st">This is the question that separates you from <em>a salesperson.</em></div>','lemon'),
 'Let it hang. Do not answer it for them.', kicker='Ask the room', num='06'),

slide(
 cell(1,13,1,2,'<div class="t">A loyalty program is a <em>multiplier</em></div>')
 +cell(1,7,2,7,'<div class="l mut">Shop A</div><div class="ch mt">100 customers &middot; 100% loyal</div>'
   '<div class="mt" style="display:grid;grid-template-columns:repeat(20,1fr);gap:3px;max-width:66%">'
   +''.join('<i style="display:block;width:100%;aspect-ratio:1;background:var(--ink)"></i>' for _ in range(100))
   +'</div><div class="ch mt2">&asymp;100 extra orders<br><span class="mut">still dead</span></div>')
 +cell(7,13,2,7,'<div class="l">Shop B</div><div class="ch mt">20,000 customers &middot; 5% loyal</div>'
   '<div class="mt" style="display:grid;grid-template-columns:repeat(40,1fr);gap:2px">'
   +''.join(f'<i style="display:block;width:100%;aspect-ratio:1;background:{"var(--ink)" if k%20==0 else "rgba(10,10,10,.18)"}"></i>' for k in range(600))
   +'</div><div class="ch mt2">&asymp;3,000&ndash;4,000 extra orders<br><span>real money</span></div>','lemon')
 +cell(1,13,7,9,'<div class="st">Multiply a small number &mdash; <em>it is still small.</em></div>'
   '<div class="b mt mut">Shop A has a perfect loyalty program and is going out of business.</div>','ink'),
 'You cannot multiply your way out of a base of a hundred. This is the arithmetic behind every "not yet".', num='07'),

WN('A shop with 100 customers wants points. Do you sell it?',
 'No &mdash; they need a bigger base first',
 'Perfect retention on 100 people is still 100 people. They need <b>referral and acquisition</b> first. '
 'Points multiply a base that is not there yet.',
 'And if you sell it anyway',
 'It will not produce a result. They churn in six months &mdash; <b>correctly</b> &mdash; and blame us. '
 'You did not win an account. You borrowed one.',
 'Telling a survival-stage shop to launch points is not service. It is selling them the wrong thing. And "not ready" is never a dead end — it is a different recommendation.',
 num='08'),

slide(
 cell(1,13,1,3,'<div class="l mut">&ldquo;Not yet&rdquo; has two causes, and only one of them is about size</div>'
   '<div class="t mt">No base &mdash; or <em>no product</em> worth returning to.</div>')
 +cell(1,7,3,6,'<div class="ch">No base yet</div><div class="rule"></div>'
   '<div class="b">A real product, too few people. <b>Fixable, and quickly</b> &mdash; '
   'referral and acquisition. Come back to us in six months.</div>','lemon')
 +cell(7,13,3,6,'<div class="ch">No reason to return</div><div class="rule"></div>'
   '<div class="b">Read the one-star reviews. If the complaints are about <b>the product itself</b>, '
   'no mechanism we sell will create a second order.</div>','ink')
 +cell(1,13,6,9,'<div class="st">One is a <em>timing</em> answer. The other is a <em>product</em> answer.</div>'
   '<div class="b mt mut">Do not give the timing answer to a product problem. They will come back in six months '
   'with the same base and the same reviews, and we will have wasted everybody&rsquo;s year.</div>'),
 'Rung one from last session. Check the reviews before you promise them anything — it is three minutes and it changes what you say.',
 num='08a'),

slide(
 cell(1,13,1,2,'<div class="t">Then the question is <em>stage</em></div>')
 +cell(1,13,2,4,'<div style="display:flex;align-items:center;gap:30px">'
   '<div class="ch" style="flex:1">no real base yet</div><div class="st">&rarr;</div>'
   '<div class="ch lem" style="flex:1">expand it &mdash; REFERRAL</div></div>','ink')
 +cell(1,13,4,6,'<div style="display:flex;align-items:center;gap:30px">'
   '<div class="ch" style="flex:1">a base, but they buy once</div><div class="st">&rarr;</div>'
   '<div class="ch" style="flex:1">a reason to return &mdash; POINTS</div></div>','lemon')
 +cell(1,13,6,8,'<div style="display:flex;align-items:center;gap:30px">'
   '<div class="ch" style="flex:1">a base, discounting everyone</div><div class="st">&rarr;</div>'
   '<div class="ch" style="flex:1">stop the blanket discount &mdash; TIERS</div></div>','lemon')
 +cell(1,13,8,9,'<div class="b">Referral <b>grows</b> the base. Loyalty <b>monetises</b> it. Never confuse the two.</div>'),
 'The shop that must NOT be sold points is often exactly the shop that should run referral.', num='09'),

slide(
 cell(1,13,1,3,'<div class="l mut">The hardest thing you will have to say</div>'
   '<div class="t mt">They installed a bundle app.<br>Their real leak is that <em>nobody comes back.</em></div>')
 +cell(1,13,3,6,'<div class="st">They are fixing <b>the cart</b> while bleeding at <b>the second order.</b></div>')
 +cell(1,7,6,9,'<div class="d">Do you tell them?</div>','ink')
 +cell(7,13,6,9,'<div class="d">Yes.</div>'
   '<div class="b mt">That is the service. And it costs something &mdash; you are telling a paying merchant '
   'that the thing they bought is not their problem.</div>','lemon'),
 'That is the whole difference between answering the app and owning the outcome.', num='10'),

slide(
 cell(1,8,1,9,'<div class="l mut">The conversation, replaced</div>'
   '<div class="bs mut mt" style="font-family:\'JetBrains Mono\',monospace">Never: &ldquo;Points or store credit? '
   'OK, I&rsquo;ll show you where to turn it on.&rdquo;</div><div class="rule"></div>'
   '<ul><li class="b"><b>1 Stage</b> &mdash; is there a base to sell back to?</li>'
   '<li class="b"><b>2 Base</b> &mdash; how many, how many return, typical basket</li>'
   '<li class="b"><b>3 Fear</b> &mdash; losing new people, or over-discounting?</li>'
   '<li class="b"><b>4 Mechanism</b> &mdash; referral, points, credit, tiers</li>'
   '<li class="b"><b>5 Numbers</b> &mdash; thresholds from their data, defended</li>'
   '<li class="b"><b>6 Placement</b> &mdash; from their journey, not the demo store</li></ul>')
 +cell(8,13,1,5,'<div class="ch">Only step <em>6</em> is a screen.</div>'
   '<div class="b mt2">Steps one to five are the service. That is what we are actually paid for.</div>','lemon')
 +cell(8,13,5,9,'<div class="c3 lem">Remember the talk</div>'
   '<div class="bs mt">AI took the execution. What is left for people is the <b>outcome</b> &mdash; '
   'judgement about one specific business, and being accountable for it.</div>','ink'),
 'This is the closing argument of the whole course.', num='11'),

slide(
 cell(1,13,1,2,'<div class="t">The gate</div>')
 +cell(1,5,2,7,'<div class="n-sm">01</div><div class="ch mt">A cold teardown</div><div class="rule"></div>'
   '<div class="bs">A brand you have never seen. Fifteen minutes. A lead accepts it.</div>')
 +cell(5,9,2,7,'<div class="n-sm">02</div><div class="ch mt">8 of 12 restatements</div><div class="rule"></div>'
   '<div class="bs">Timed, from your own queue.</div>','lemon')
 +cell(9,13,2,7,'<div class="n-sm">03</div><div class="ch mt">Your store, launched</div><div class="rule"></div>'
   '<div class="bs">To standard. Max three apps, every one defensible.</div>','ink')
 +cell(1,13,7,9,'<div class="b">&ldquo;Not yet&rdquo; is a normal outcome here too. It means <b>another stack of reps</b> '
   '&mdash; not another lecture.</div>'),
 'They leave knowing exactly what they are measured on. No surprises.', num='12'),

slide(
 cell(1,8,1,9,'<div class="l mut">Now you &middot; 50 minutes</div>'
   '<div class="t mt">Two brands.<br>One <em>verdict</em> each.</div><div class="rule"></div>'
   '<ul><li class="b">One strong fit, one deliberately <b>not ours</b></li>'
   '<li class="b">Full teardown, then a verdict <b>out loud</b> with the reason</li>'
   '<li class="b">Fit is learned by contrast &mdash; never one brand alone</li></ul>')
 +cell(8,13,1,5,'<div class="ch">Is it ours &middot; does it need this &middot; <em>what is the one thing we would change?</em></div>','lemon')
 +cell(8,13,5,9,'<div class="c3 lem">How this is graded</div>'
   '<div class="bs mt">A checklist memorised is trivia.</div>'
   '<div class="bs mt">A checklist run against a brand that <b>fails</b> it is judgement.</div>','ink'),
 'That distinction is what we are grading, and it is the difference between a support person and an account manager.',
 kicker='They do it', num='13'),

slide(
 cell(1,13,1,5,'<div class="d">You have not opened Joy <em>once.</em></div>','ink')
 +cell(1,13,5,9,'<div class="st">And you can already tell a merchant whether we can help them, and why.</div>'
   '<div class="b mt2">That was the whole point.</div>','lemon'),
 'End here. Do not add anything. Sit down.', num='14'),
]

# ── merge sessions 1 + 2 into one ──
S3 = S3[:4] + _PRODUCT + WAYS + S3[4:-1] + _DRILL3 + [_SRC3]

_RTRAP = [
slide(
 cell(1,13,1,3,'<div class="l mut">A trap you will meet in a real account</div>'
   '<div class="t mt">Sales are flat.<br>But ROAS looks <em>great.</em></div>')
 +cell(1,7,3,7,'<div class="c3">What is actually happening</div><div class="rule"></div>'
   '<div class="b">The ads are being shown to <b>people who already buy</b>. They would have bought anyway. '
   'Meta counts the sale, ROAS looks wonderful, and the business does not grow a dollar.</div>')
 +cell(7,13,3,7,'<div class="c3 lem">The number that reveals it</div>'
   '<div class="n-sm mt">80%</div><div class="ls">returning customers</div>'
   '<div class="bs mt2">Healthy on its own. <b>Fatal</b> if it is also who the ads are hitting.</div>','ink')
 +cell(1,13,7,9,'<div class="st">A high returning rate is a <em>good thing</em>. '
   'It becomes a problem only when acquisition stops reaching anyone new.</div>'
   '<div class="b mt mut">The fix is not our product &mdash; it is excluding past customers and the email list '
   'from acquisition. But <b>spotting it</b> is exactly the AM read, and almost nobody spots it.</div>','lemon'),
 'This is the most valuable diagnostic in the whole session, because the merchant thinks everything is fine — the dashboard is green. You are the one who says: check who those sales are coming from.',
 num='12a'),

slide(
 cell(1,13,1,2,'<div class="t">Low returning rate &mdash; the fix depends entirely on <em>what they sell</em></div>')
 +cell(1,5,2,7,'<div class="l">Consumable</div><div class="ch mt">soap, supplements, skincare</div>'
   '<div class="rule"></div>'
   '<div class="b"><b>Subscription</b> is the biggest lever, then reminders and remarketing. '
   'This is where loyalty works hardest.</div>','lemon')
 +cell(5,9,2,7,'<div class="c3">Clothing &amp; repeat-catalogue</div><div class="rule"></div>'
   '<div class="b">Do not just push one hero SKU. Show past buyers the <b>2nd to 5th</b> best sellers, '
   'new arrivals, the next drop. Loyalty and credit help here, but range does more.</div>')
 +cell(9,13,2,7,'<div class="c3">High-ticket, bought once</div><div class="rule"></div>'
   '<div class="b">Sell them a <b>consumable accessory</b> &mdash; the cleaning kit, the refill, the spare. '
   'That is how a one-time product gets a second order at all.</div>','ink')
 +cell(1,13,7,9,'<div class="st">So &ldquo;they do not come back&rdquo; is <em>three different problems</em> '
   'with three different answers.</div>'
   '<div class="b mt mut">And only one of them is mainly ours.</div>'),
 'This upgrades what we said about HexClad. The honest answer for high-ticket is not only referral — it is find the consumable attached to the durable thing. A basketball machine sells balls. A pan sells a cleaning kit.',
 num='12b'),
]




# ── Session 1 intro: the CS problem, the AM difference, why now, what it does for you ──
INTRO = [
slide(
 cell(1,10,1,7,'<div class="l mut">Session One</div>'
   '<div class="d mt">How a shop<br>works &mdash; and<br>how to <em>read one</em></div>','ink')
 +cell(10,13,1,7,'<div class="l">Joy<br>CS &rarr; AM</div><div class="ch mt2">The<br>basics</div>','lemon')
 +cell(1,13,7,9,'<div class="st">A shop is a business, not a website.</div>'
   '<div class="b mt mut">But first: why we are all sitting here on a working day.</div>'),
 'Goal: a shop is a business, not a website. Before any of that, ten minutes on why this course exists at all — because if they think it is extra homework for a promotion, they will not do the reps.'),

slide(
 cell(1,13,1,4,'<div class="l mut">A ticket lands. Right now.</div>'
   '<div class="d mt">&ldquo;Rewards aren&rsquo;t working.&rdquo;</div>')
 +cell(1,13,4,9,'<div class="st">What do you write back?</div>'
   '<div class="b mt2 mut">Out loud. Take three answers before you move on.</div>','lemon'),
 'Somebody will say "could you explain more" or "can you send a screenshot". Let it sit. Do not correct it yet — you are about to.',
 kicker='Ask the room', num='02'),

slide(
 cell(1,7,1,7,'<div class="l mut">What we write today</div>'
   '<div class="ch mt">&ldquo;Could you please provide more details?&rdquo;</div>'
   '<div class="rule"></div>'
   '<div class="b mut">&rarr; she explains again</div>'
   '<div class="b mut">&rarr; we copy</div>'
   '<div class="b mut">&rarr; we forward</div>')
 +cell(7,13,1,7,'<div class="l">What the other job writes</div>'
   '<div class="ch mt">&ldquo;Members aren&rsquo;t using the reward, so it isn&rsquo;t creating a second order.&rdquo;</div>'
   '<div class="rule"></div>'
   '<div class="b">&ldquo;Do they <b>not see</b> the balance &mdash; or do they see it and it is <b>not worth</b> using?&rdquo;</div>','lemon')
 +cell(1,13,7,9,'<div class="st">Both take the same number of minutes.</div>'
   '<div class="ch mt lem">Only one of them <em>did the thinking.</em></div>','ink'),
 'Say the loop without shame: merchant talks, I do not get it, can you explain more, they write the ticket for me, I copy, I forward. That is transcription. It is not a character flaw — it is what happens when you have no picture of a shop for their words to land on.',
 num='03'),

slide(
 cell(1,13,1,2,'<div class="t">Two jobs</div>')
 +cell(1,13,2,7,'<table style="font-size:24px">'
   '<tr><th></th><th>CS</th><th>AM</th></tr>'
   '<tr><td class="mut">You are judged on</td><td>the <b>ticket</b></td><td>the <b>shop</b></td></tr>'
   '<tr><td class="mut">Who starts</td><td>they write to you</td><td><b>you</b> open it</td></tr>'
   '<tr><td class="mut">You must know</td><td>the <b>app</b></td><td>the <b>business</b></td></tr>'
   '<tr><td class="mut">Done means</td><td>ticket closed</td><td>the <b>result showed up</b></td></tr>'
   '<tr><td class="mut">You lose when</td><td>backlog, slow reply</td><td>churn you never saw coming</td></tr>'
   '</table>','flat')
 +cell(1,13,7,9,'<div class="t">You can close every ticket perfectly<br>and still <em>lose the account.</em></div>','ink'),
 'That is not a complaint about CS. It is the reason the second job exists — the two scoreboards barely overlap, so every CS number can be green while every AM number is red.',
 num='04'),

slide(
 cell(1,13,1,3,'<div class="l mut">Why now &middot; 1</div>'
   '<div class="t mt">The machine already answers<br>&ldquo;<em>where do I click?</em>&rdquo;</div>')
 +cell(1,7,3,7,'<div class="c3">What it does better than us</div><div class="rule"></div>'
   '<ul><li class="bs">instantly, 24/7, every language</li><li class="bs">perfect, polite English</li>'
   '<li class="bs">reads the docs, writes the reply</li><li class="bs">never tired, never annoyed</li></ul>')
 +cell(7,13,3,7,'<div class="c3">What it cannot do</div><div class="rule"></div>'
   '<ul><li class="bs">decide if points suit <b>this</b> merchant</li>'
   '<li class="bs">own whether her customers came back</li>'
   '<li class="bs">be accountable across a quarter</li></ul>','lemon')
 +cell(1,13,7,9,'<div class="st">AI does not take the job. It takes <em>the execution.</em></div>'
   '<div class="b mt mut">Which means the half of the job that is left for people is the <b>outcome</b>. '
   'Notice too which half the machine is best at: <b>the English.</b> '
   'If your plan is to win on English, you picked the one race already lost.</div>','ink'),
 'Frame this as elevation, not threat. Nobody has automated being accountable for whether it worked.',
 num='05'),

slide(
 cell(1,13,1,3,'<div class="l mut">Why now &middot; 2</div>'
   '<div class="t mt">Every loyalty app has<br>the <em>same features.</em></div>')
 +cell(1,7,3,7,'<div class="c3">Rivo &middot; Yotpo &middot; Smile &middot; LoyaltyLion &middot; Growave</div>'
   '<div class="rule"></div>'
   '<div class="b">Points. Tiers. Referrals. Widgets. All of them. Any feature we ship, they ship within a quarter.</div>'
   '<div class="b mt2">So the app <b>cannot</b> be what a merchant chooses us for.</div>')
 +cell(7,13,3,7,'<div class="ch">What is left to compete on</div>'
   '<div class="st mt2">Whether the merchant actually <em>gets a result</em> &mdash; and how fast.</div>','lemon')
 +cell(1,13,7,9,'<div class="st">We are not selling software. We are selling <em>the outcome the software produces.</em></div>'
   '<div class="b mt mut">Which means the people who can produce that outcome are not a support cost. '
   'They are the product.</div>','ink'),
 'This is the company-level version of the same argument. Features are commoditised in a quarter. Service is not copyable, because it lives in people who understand ecom.',
 num='06'),

slide(
 cell(1,13,1,3,'<div class="l mut">And what it does for you on Monday</div>'
   '<div class="t mt">This is not homework for <em>a promotion later.</em></div>')
 +cell(1,7,3,7,'<ul><li class="b">You stop being stuck on tickets you do not understand</li>'
   '<li class="b">You stop asking her to explain &mdash; you already know what she means</li>'
   '<li class="b">Your forwards get <b>actioned</b>, because &ldquo;I think&hellip;&rdquo; is filled in</li></ul>')
 +cell(7,13,3,7,'<ul><li class="b">Fewer angry follow-ups, because you solved <b>the real thing</b></li>'
   '<li class="b">Faster replies, because you are not decoding word by word</li>'
   '<li class="b">The copy-forward loop &mdash; the part that makes the job feel bad &mdash; <b>stops</b></li></ul>','lemon')
 +cell(1,13,7,9,'<div class="st">So today we do not open Joy. We start with <em>the business.</em></div>','ink'),
 'This is the slide that decides whether they do the reps. If they think it is a promotion track they will half-do it. If they believe it makes Monday easier, they will show up.',
 num='07'),
]

# ── SESSION 1: why we are here + how a shop makes money ──
_HALFDAYS = slide(
 cell(1,6,1,9,'<div class="l mut">Today&rsquo;s brand &middot; breakdown 1</div>'
   '<div class="t mt">Halfdays</div>'
   '<div>'+link('halfdays.com')+'</div>'
   '<div class="rule"></div>'
   '<div class="b">Outdoor apparel. Find the hero jacket and its price.</div>'
   '<div class="b mt2">Guess what it <b>costs them to make</b>, out loud, as a room.</div>'
   '<div class="bs mt2 mut">See the little tab on the left? That is the capture popup, waiting.</div>')
 +cell(6,13,1,9,img(HALFDAYS),'photo'),
 'You will be roughly right, and being roughly right is the whole skill. Then note the free-shipping threshold: $95. Ask why that number.',
 kicker='Open it live')

_POPUP = slide(
 cell(1,6,1,9,'<div class="l mut">A real one, right now</div>'
   '<div class="t mt">52% off &mdash; <em>for an email.</em></div>'
   '<div class="rule"></div>'
   '<div class="b">HexClad, today. The popup fires before you have seen a single pan.</div>'
   '<div class="b mt2">Ask the room: <b>what is actually being bought here?</b></div>'
   '<div class="bs mt2 mut">Not the sale. The email. And a very large discount handed to everyone who arrives.</div>')
 +cell(6,13,1,9,img(HEXPOPUP),'photo'),
 'This is the single best teaching image in the deck because it is live and enormous. Fifty-two percent, before she has looked at anything. Ask what that trains a customer to do — wait for the sale. Then go to the next slide.',
 kicker='Open it live')

SESS1 = INTRO + [S1[i] for i in (1,2,3,4,5,7)] + [_STORES[2], _HALFDAYS] + [S1[i] for i in (9,10,11,12,13)] + [_STORES[0]] + [S1[i] for i in (14,)] + [_STORES[1]] + [S1[16]] + _DRILL1 + [_SRC1]

# ── SESSION 2: how to read a shop ──
SESS2 = [TITLE('Goal: given a shop you have never seen, find what is actually wrong with it — and say which problem to fix first. Today we diagnose one together, then you diagnose another alone.',
  'Session Two','What is<br><em>wrong</em><br>with this shop?',
  ('Troubleshooting a real business.','Every merchant complaint is a symptom. Today you learn to find the cause.'),'Trouble-<br>shooting')] \
  + [_DIAGNOSE] + _WINNER + [S2[i] for i in (1,2,3)] + [_POPUP] + _DECODER + [_DD_AOV,_DD_ROAS,_DD_NORMAL] + _RTRAP + [S2[i] for i in (11,12,13)] + _STACKMAP + [_RANK] + [S2[14]] + _DRILL2 + [_SRC2]


S4.insert(4, slide(
 cell(1,13,1,3,'<div class="l mut">And here is how merchants actually decide</div>'
   '<div class="t mt">They do not buy features.<br>They buy <em>a number.</em></div>')
 +cell(1,7,3,6,'<div class="c3">Rivo &mdash; a loyalty competitor</div><div class="rule"></div>'
   '<div class="b"><b>19 case studies.</b> Each card: <b>one hero number</b> '
   '&mdash; &ldquo;$450K in 90 days&rdquo; &mdash; and <b>no feature list at all</b>.</div>')
 +cell(1,7,6,8,'<div class="bs mut">their category banner</div>'
   '<div class="c3 mt">55&times; ROI &middot; 3.1&times; repeat &middot; +4% revenue &middot; 9,000+ brands</div>','ink')
 +cell(7,13,3,6,'<div class="ch">We have the results too</div>'
   '<div class="b mt">1700% ROI. 450% ROI. $110K in 14 days. All real, all ours.</div>','lemon')
 +cell(7,13,6,8,'<div class="ch">And almost no public page saying so</div>'
   '<div class="bs mt">A <b>packaging</b> gap, not a results gap.</div>','ink')
 +cell(1,13,8,9,'<div class="c3">A CS person who can say <em>what result to expect, and by when</em> '
   'is worth more than one who configures faster.</div>'),
 'Real, and it happened: asked "what apps does Avada have?", the answer was "we have twenty apps." The other side stopped wanting to talk — not because twenty is too few, but because the answer read as "these people do not know what problem they solve." The right answer starts at the problem, never at the catalogue. That is exactly what we are training out of CS.',
 num='04a'))

S4.insert(5, slide(
 cell(1,13,1,3,'<div class="l mut">A test you can run on yourself, and on any pair reporting back</div>'
   '<div class="t mt">The <em>&ldquo;why&rdquo;</em> chain</div>')
 +cell(1,7,3,7,'<div class="b">&ldquo;They should run a subscription.&rdquo;</div>'
   '<div class="b mt"><b>What for?</b> &mdash; &ldquo;to increase LTV.&rdquo;</div>'
   '<div class="b mt"><b>Why does LTV need increasing?</b></div>'
   '<div class="b mt"><b>To what number? Why that number?</b></div>'
   '<div class="b mt"><b>What do they get there that they do not get now?</b></div>')
 +cell(7,13,3,7,'<div class="ch">Same for AOV</div>'
   '<div class="b mt2">&ldquo;They need higher AOV.&rdquo;</div>'
   '<div class="ch mt2">How much is <em>low?</em><br>How much is <em>enough?</em><br>Enough <em>for what?</em></div>','lemon')
 +cell(1,13,7,9,'<div class="st">If the chain breaks anywhere, the business was not understood &mdash; '
   'no matter how full the sheet is.</div>'
   '<div class="b mt mut">Three questions and you find out immediately whether somebody read the business '
   'or repeated a word they have heard on calls.</div>','ink'),
 'Use this as the report-out standard for the rep tonight. It is fast, it is fair, and it cannot be bluffed.',
 num='04b'))

# ═════════════════ THE TALK — 20-25 min, standalone ═════════════════
TALK=[
slide(
 cell(1,10,1,7,'<div class="l mut">Joy &middot; CS</div>'
   '<div class="d mt">From app support<br>to <em>retention<br>service</em></div>','ink')
 +cell(10,13,1,7,'<div class="l">20 minutes</div>'
   '<div class="ch mt2">Then we<br>start the<br>work.</div>','lemon')
 +cell(1,13,7,9,'<div class="st">Get the shop more customers coming back &mdash; in less time.</div>'
   '<div class="b mt mut">No slides about the app today. Nothing to configure. Just what the job is turning into, '
   'and why.</div>'),
 'Twenty minutes, then sit down. This is the heading, not the course. Do not let it drift into teaching.'),

slide(
 cell(1,13,1,4,'<div class="l mut">A ticket lands. Right now.</div>'
   '<div class="d mt">&ldquo;Rewards aren&rsquo;t working.&rdquo;</div>')
 +cell(1,13,4,9,'<div class="st">What do you write back?</div>'
   '<div class="b mt2 mut">Out loud. Take three answers before I go on.</div>','lemon'),
 'Somebody will say "could you explain more" or "can you send a screenshot". Let it sit. Do not correct it — the next slide does.',
 kicker='Ask the room'),

slide(
 cell(1,7,1,7,'<div class="l mut">What we write today</div>'
   '<div class="ch mt">&ldquo;Could you please provide more details?&rdquo;</div><div class="rule"></div>'
   '<div class="b mut">&rarr; she explains again</div>'
   '<div class="b mut">&rarr; we copy</div>'
   '<div class="b mut">&rarr; we forward</div>')
 +cell(7,13,1,7,'<div class="l">What the other job writes</div>'
   '<div class="ch mt">&ldquo;Members aren&rsquo;t using the reward, so it isn&rsquo;t creating a second order.&rdquo;</div>'
   '<div class="rule"></div>'
   '<div class="b">&ldquo;Do they <b>not see</b> the balance &mdash; or see it and it is <b>not worth</b> using?&rdquo;</div>','lemon')
 +cell(1,13,7,9,'<div class="st">Same number of minutes. Only one of them <em>did the thinking.</em></div>','ink'),
 'Say the loop without shame: merchant talks, I do not get it, can you explain more, they write the ticket for me, I copy, I forward. That is transcription — and it is not a character flaw. It is what happens when you have no picture of a shop for their words to land on.'),

slide(
 cell(1,13,1,2,'<div class="t">Two jobs</div>')
 +cell(1,13,2,7,'<table style="font-size:26px">'
   '<tr><th></th><th>CS</th><th>AM</th></tr>'
   '<tr><td class="mut">You are judged on</td><td>the <b>ticket</b></td><td>the <b>shop</b></td></tr>'
   '<tr><td class="mut">Who starts</td><td>they write to you</td><td><b>you</b> open it</td></tr>'
   '<tr><td class="mut">You must know</td><td>the <b>app</b></td><td>the <b>business</b></td></tr>'
   '<tr><td class="mut">Done means</td><td>ticket closed</td><td>the <b>result showed up</b></td></tr>'
   '<tr><td class="mut">You lose when</td><td>backlog, slow reply</td><td>churn you never saw coming</td></tr>'
   '</table>','flat')
 +cell(1,13,7,9,'<div class="d">You can close every ticket perfectly<br>and still <em>lose the account.</em></div>','ink'),
 'Not a complaint about CS. The two scoreboards barely overlap — every CS number can be green while every AM number is red. That gap is the whole reason for this talk.'),

slide(
 cell(1,13,1,3,'<div class="l mut">Why you freeze &mdash; and it is not what you think</div>'
   '<div class="t mt">It was never <em>the English.</em></div>')
 +cell(1,13,3,6,'<div class="b">Without a picture of how a real shop earns &mdash; get a customer, take the money, '
   'need them back &mdash; her words have <b>nowhere to land</b>. So every sentence is noise, '
   'and you ask her to keep talking until you can forward it.</div>')
 +cell(1,13,6,9,'<div class="st">Không phải vì tiếng Anh. Vì chưa biết shop chạy thế nào, '
   'nên câu của merchant <em>không ghim vào đâu được.</em></div>'
   '<div class="b mt mut">Học xong, em phải nói lại được vấn đề. '
   'Hỏi &ldquo;explain more&rdquo; là chưa hiểu &mdash; không phải là cách hiểu.</div>','ink'),
 'Say the Vietnamese line yourself, slowly. This is the moment the room stops feeling accused and starts feeling explained.'),

slide(
 cell(1,13,1,3,'<div class="l mut">Why now &middot; 1</div>'
   '<div class="t mt">The machine already answers<br>&ldquo;<em>where do I click?</em>&rdquo;</div>')
 +cell(1,7,3,7,'<div class="c3">Better than us</div><div class="rule"></div>'
   '<ul><li class="bs">instantly, 24/7, every language</li><li class="bs">perfect, polite English</li>'
   '<li class="bs">reads the docs, writes the reply</li><li class="bs">never tired, never annoyed</li></ul>')
 +cell(7,13,3,7,'<div class="c3">Cannot do at all</div><div class="rule"></div>'
   '<ul><li class="bs">decide if points suit <b>this</b> merchant</li>'
   '<li class="bs">own whether her customers came back</li>'
   '<li class="bs">be accountable across a quarter</li></ul>','lemon')
 +cell(1,13,7,9,'<div class="st">AI does not take the job. It takes <em>the execution.</em></div>'
   '<div class="b mt mut">And notice which half it is best at: <b>the English.</b> '
   'If your plan is to win on English, you picked the one race that is already lost.</div>','ink'),
 'Elevation, not threat. Nobody has automated being accountable for whether it worked. And this closes the English argument from the other end — the machine has perfect English and still cannot answer this merchant.'),

slide(
 cell(1,13,1,3,'<div class="l mut">Why now &middot; 2</div>'
   '<div class="t mt">Every loyalty app has<br>the <em>same features.</em></div>')
 +cell(1,7,3,7,'<div class="c3">Rivo &middot; Yotpo &middot; Smile &middot; LoyaltyLion &middot; Growave &middot; BON</div>'
   '<div class="rule"></div>'
   '<div class="b">Points. Tiers. Referrals. Widgets. Anything we ship, they ship within a quarter.</div>'
   '<div class="b mt2">So the app <b>cannot</b> be what a merchant chooses us for.</div>')
 +cell(7,13,3,7,'<div class="ch">What is left to compete on</div>'
   '<div class="st mt2">Whether the merchant actually <em>gets a result.</em></div>','lemon')
 +cell(1,13,7,9,'<div class="st">We are not selling software. We are selling <em>the outcome it produces.</em></div>'
   '<div class="b mt mut">Which makes the people who can produce that outcome not a support cost. '
   'They are the product.</div>','ink'),
 'The company-level version of the same argument. Features are commoditised in a quarter. Service is not copyable, because it lives in people who understand ecom.'),

slide(
 cell(1,13,1,3,'<div class="l mut">And merchants already decide this way</div>'
   '<div class="t mt">They do not buy features.<br>They buy <em>a number.</em></div>')
 +cell(1,7,3,7,'<div class="c3">A competitor&rsquo;s public page</div><div class="rule"></div>'
   '<div class="b">19 case studies. Each one <b>a single number</b> &mdash; &ldquo;$450K in 90 days&rdquo; '
   '&mdash; and <b>no feature list at all</b>.</div>'
   '<div class="bs mt2 mut">Features get explained only after the number has persuaded you.</div>')
 +cell(7,13,3,7,'<div class="ch">Asked what Avada does, we once said</div>'
   '<div class="st mt2">&ldquo;We have <em>twenty apps.</em>&rdquo;</div>'
   '<div class="bs mt2">They stopped wanting to talk.</div>','ink')
 +cell(1,13,7,9,'<div class="st">Not because twenty is too few. Because it reads as '
   '<em>&ldquo;these people do not know what problem they solve.&rdquo;</em></div>','lemon'),
 'Real, and it happened. The right answer starts at the problem — we help merchants do X, measured by Y — never at the catalogue. "Where do I click" is the catalogue answer. "Here is the result you should expect" is the other one.'),

slide(
 cell(1,13,1,3,'<div class="l mut">So where you are heading</div>'
   '<div class="t mt">Four questions you can answer about <em>any</em> merchant &mdash; before opening Joy.</div>')
 +cell(1,7,3,6,'<div class="b">1 &middot; What does this shop sell, and how does it make money on one order?</div>')
 +cell(7,13,3,6,'<div class="b">2 &middot; How do people arrive, and where do they quit?</div>')
 +cell(1,7,6,8,'<div class="b">3 &middot; Why would someone buy a <b>second</b> time &mdash; and what is the brand doing about it?</div>')
 +cell(7,13,6,8,'<div class="b">4 &middot; Is it ours, does it need us, and what is the one thing we would change?</div>','lemon')
 +cell(1,13,8,9,'<div class="c3">If you cannot answer 1&ndash;3, you are not allowed to open the app.</div>','ink'),
 'The app is the last mile, not the job. Say that plainly.'),

slide(
 cell(1,13,1,2,'<div class="l mut">There is a rung in between. Nobody jumps.</div>')
 +cell(1,13,2,4,'<div class="ch">CS <span class="mut">&mdash; answers the app</span></div>')
 +cell(1,13,4,5,'<div class="bs mut">gate &middot; restate the merchant&rsquo;s outcome before you reply</div>','plain')
 +cell(1,13,5,7,'<div class="ch">CS who reads <span class="mut">&mdash; answers the ticket behind the ticket</span></div>','lemon')
 +cell(1,13,7,8,'<div class="bs mut">gate &middot; read a brand cold &middot; launch your own store</div>','plain')
 +cell(1,13,8,9,'<div class="ch">AM <span class="mut">&mdash; answers for the account</span></div>','ink'),
 'The middle rung is a real job and a real raise. Aim there first. Not everyone will want rung three — owning revenue and renewals is a different appetite, not a better person.'),

slide(
 cell(1,13,1,3,'<div class="l mut">And what it does for you on Monday</div>'
   '<div class="t mt">This is not homework for <em>a promotion later.</em></div>')
 +cell(1,7,3,7,'<ul><li class="b">You stop being stuck on tickets you do not understand</li>'
   '<li class="b">You stop asking her to explain &mdash; you already know what she means</li>'
   '<li class="b">Your forwards get <b>actioned</b>, because &ldquo;I think&hellip;&rdquo; is filled in</li></ul>')
 +cell(7,13,3,7,'<ul><li class="b">Fewer angry follow-ups, because you solved <b>the real thing</b></li>'
   '<li class="b">Faster replies &mdash; you are not decoding word by word</li>'
   '<li class="b">The copy-forward loop &mdash; the part that makes the job feel bad &mdash; <b>stops</b></li></ul>','lemon')
 +cell(1,13,7,9,'<div class="st">It makes Monday easier. The rest follows from that.</div>','ink'),
 'This is the slide that decides whether they do the reps. If they hear "promotion track" they will half-do it. If they believe it makes Monday easier, they show up.'),

slide(
 cell(1,13,1,2,'<div class="l mut">How we will learn it &mdash; four sessions, two hours each</div>')
 +cell(1,4,2,7,'<div class="n-sm">01</div><div class="ch mt">How a shop makes money</div>'
   '<div class="rule"></div><div class="bs mut">price, margin, and why the second order is the business</div>')
 +cell(4,7,2,7,'<div class="n-sm">02</div><div class="ch mt">What is wrong with this shop?</div>'
   '<div class="rule"></div><div class="bs mut">find the real problem &mdash; and which one to fix first</div>','lemon')
 +cell(7,10,2,7,'<div class="n-sm">03</div><div class="ch mt">Why people come back</div>'
   '<div class="rule"></div><div class="bs mut">retention, and what actually makes someone return</div>')
 +cell(10,13,2,7,'<div class="n-sm">04</div><div class="ch mt">Bring it together</div>'
   '<div class="rule"></div><div class="bs mut">is it ours, does it need us, what do we say</div>','ink')
 +cell(1,13,7,9,'<div class="st">No lectures. Every session you break down <em>a real brand</em> &mdash; '
   'and you launch <em>a real store</em> of your own.</div>'),
 'Not a manual and not a product certification. Reps on real shops.'),

slide(
 cell(1,7,1,6,'<div class="l mut">And a real store &mdash; not a development store</div>'
   '<div class="t mt">You will be the <em>owner</em>, not the user.</div>'
   '<div class="b mt2">One product. Real checkout. <b>Max three apps</b>, and every one has to survive '
   '&ldquo;what job does this do?&rdquo;</div>')
 +cell(7,13,1,6,'<table style="font-size:23px">'
   '<tr><th>Dev store</th><th>Real store</th></tr>'
   '<tr><td>you click Admin</td><td>you are the <b>owner</b></td></tr>'
   '<tr><td>nothing is at stake</td><td>a wrong discount costs you</td></tr>'
   '<tr><td>&ldquo;set up the app&rdquo; feels like the work</td><td><b>order 1 &rarr; order 2</b> is the work</td></tr>'
   '<tr><td>you still think like CS</td><td>you think like the person on the call</td></tr></table>','flat')
 +cell(1,13,6,9,'<div class="st">Complete <em>order one</em>. Then try to make <em>order two</em> happen.</div>'
   '<div class="b mt mut">That is the whole simulation, and it is the part you will remember in a year.</div>','ink'),
 'Today CS stores are many apps, low quality, not to standard. That is the thing being fixed — and building one to standard is the cause, not a side exercise.'),

slide(
 cell(1,13,1,5,'<div class="d">We don&rsquo;t get paid because<br>they learned the app.</div>','ink')
 +cell(1,13,5,9,'<div class="d">They get paid when the same<br>customer <em>orders again.</em></div>'
   '<div class="st mt">Your job is that outcome &mdash; faster.</div>','lemon'),
 'Close here. Do not add anything. Sit down.'),
]

if __name__=='__main__':
    os.chdir(D)
    print('Building (Neo-Grid Bold):')
    build('00-talk.html','The Talk — from app support to retention service',TALK)
    build('session-1-money.html','Session 1 — How a shop makes money',SESS1)
    build('session-2-troubleshoot.html','Session 2 — What is wrong with this shop?',SESS2)
    build('session-3-retention.html','Session 3 — Why people come back',S3)
    build('session-4-together.html','Session 4 — Bring it together',S4[:-2] + _DRILL4 + [_SRC4, S4[-1]])
