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

/* ── illustration components ── */
.viz{margin:1em 0}
.cap{font-size:clamp(12px,1.3vw,17px);color:var(--dim);letter-spacing:.1em;text-transform:uppercase;font-weight:700;margin-bottom:.5em}
.stack{display:flex;border-radius:12px;overflow:hidden;box-shadow:0 10px 30px rgba(0,0,0,.45)}
.stack>div{padding:1.1em .5em .9em;text-align:center;min-width:0}
.stack .v{font-size:clamp(17px,2.4vw,32px);font-weight:800;line-height:1;color:#0d1117}
.stack .k{font-size:clamp(10px,1.15vw,15px);margin-top:.45em;color:rgba(13,17,23,.72);font-weight:700;letter-spacing:.04em}
.scale{display:flex;justify-content:space-between;margin-top:.5em;font-size:clamp(12px,1.4vw,19px);color:var(--dim);font-weight:700}
.rail{position:relative;height:clamp(38px,5vw,62px);border-radius:10px;background:var(--card);box-shadow:inset 0 0 0 1px var(--line)}
.fill{position:absolute;inset:0 auto 0 0;border-radius:10px;display:flex;align-items:center;padding:0 1em;
  font-weight:800;font-size:clamp(15px,2.1vw,29px);color:#0d1117;white-space:nowrap}
.row{display:grid;grid-template-columns:clamp(72px,9vw,132px) 1fr;align-items:center;gap:1em;margin:.7em 0}
.row .lbl{font-size:clamp(12px,1.4vw,19px);color:var(--dim);text-align:right;font-weight:700;letter-spacing:.06em}
.over{display:flex;gap:2px}
.over>div{padding:.75em .3em;text-align:center;font-size:clamp(10px,1.15vw,15px);font-weight:800;color:#0d1117;
  border-radius:4px;overflow:hidden;white-space:nowrap}
.mark{position:absolute;top:-8px;bottom:-8px;width:0;border-left:2px dashed var(--fg)}
.fun{display:flex;align-items:flex-end;gap:clamp(3px,.6vw,8px);height:clamp(120px,17vw,220px)}
.fun>div{flex:1;border-radius:6px 6px 0 0;position:relative;
  background:linear-gradient(180deg,#2f6fb0,#1b3a5c)}
.fun span{position:absolute;bottom:-1.9em;left:50%;transform:translateX(-50%);font-size:clamp(9px,1.05vw,14px);color:var(--dim);white-space:nowrap}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:clamp(12px,2vw,28px)}
.tile{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:clamp(14px,1.8vw,26px)}
.tile.hot{border-color:var(--acc)}
.tile h4{font-size:clamp(14px,1.7vw,23px);font-weight:800;margin-bottom:.45em}
.tile p,.tile li{font-size:clamp(12px,1.45vw,20px);line-height:1.45}
.tile ul{margin-top:.4em}.tile li{padding-left:1em;margin:.28em 0}
.tile li:before{width:.34em;height:.34em;top:.6em}
.dots{display:grid;gap:2px}
.tl{position:relative;height:clamp(78px,10vw,120px);margin-top:1.6em}
.tl:before{content:"";position:absolute;left:0;right:0;top:50%;height:3px;background:var(--line);border-radius:2px}
.tl i{position:absolute;top:50%;transform:translate(-50%,-50%);width:14px;height:14px;border-radius:50%;background:var(--dim)}
.tl i.big{width:22px;height:22px;box-shadow:0 0 0 6px rgba(240,180,41,.16)}
.tl b{position:absolute;transform:translateX(-50%);font-size:clamp(11px,1.3vw,17px);white-space:nowrap;font-weight:700}
.tl s{position:absolute;transform:translateX(-50%);font-size:clamp(10px,1.15vw,15px);color:var(--dim);text-decoration:none}
.pill{display:inline-block;padding:.3em .9em;border-radius:99px;font-size:clamp(11px,1.3vw,17px);font-weight:800}
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

# ─────────────────────────── ILLUSTRATIONS (HTML/CSS) ───────────────────────────
GR = {'gold':'linear-gradient(160deg,#ffd166,#e0a020)','amber':'linear-gradient(160deg,#e0a020,#a8761a)',
      'bronze':'linear-gradient(160deg,#a8761a,#6b4a12)','deep':'linear-gradient(160deg,#6b4a12,#3d2a09)',
      'green':'linear-gradient(160deg,#5ddb7a,#2f9946)','red':'linear-gradient(160deg,#ff7b72,#c9382f)',
      'slate':'linear-gradient(160deg,#6b7280,#3f4650)','steel':'linear-gradient(160deg,#4a5560,#2b323b)'}

def viz_shoe():
    """The $100 sneaker. Real numbers, and the punchline."""
    segs=[(28,'$28','made in the factory','gold'),(22,'$22','the brand','amber'),(50,'$50','the shop that sells it','bronze')]
    bar=''.join(f'<div style="flex:{w};background:{GR[g]}"><div class="v">{v}</div><div class="k">{k}</div></div>'
                for w,v,k,g in segs)
    return ('<div class="viz"><div class="cap">what you pay for a $100 shoe</div>'
            f'<div class="stack">{bar}</div>'
            '<div class="scale"><span>$0</span><span>$50 &nbsp;·&nbsp; what the shop paid</span><span>$100</span></div>'
            '<div style="margin-top:1.1em;display:flex;align-items:center;gap:.9em;flex-wrap:wrap">'
            '<span class="pill" style="background:var(--line);color:var(--dim)">then take out marketing, R&amp;D, admin, tax</span>'
            '<span style="font-size:clamp(15px,2vw,28px)">&rarr;</span>'
            '<span class="pill" style="background:var(--bad);color:#fff">adidas keeps about <b>$2</b></span>'
            '</div></div>')

def viz_layers():
    segs=[(30,'$30','factory','gold'),(30,'+$30','brand','amber'),(15,'+$15','distributor','bronze'),(25,'+$25','retail shop','deep')]
    bar=''.join(f'<div style="flex:{w};background:{GR[g]}"><div class="v">{v}</div><div class="k">{k}</div></div>'
                for w,v,k,g in segs)
    return ('<div class="viz"><div class="cap">a $30 shirt on its way to you</div>'
            f'<div class="stack">{bar}</div>'
            '<div class="scale"><span>cost to make</span><span>$100 to you</span></div></div>')

def viz_eaten():
    costs=[(15,'ads','red'),(30,'the shirt','steel'),(9,'discount','amber'),(6,'shipping','slate'),(1.78,'fee','slate')]
    tot=sum(c[0] for c in costs)
    inner=''.join(f'<div style="flex:{w};background:{GR[g]}">{n if w>5 else "&nbsp;"}</div>' for w,n,g in costs)
    return ('<div class="viz"><div class="cap">what she pays</div>'
            '<div class="rail"><div class="fill" style="width:100%;background:'+GR['green']+'">$60.00</div></div>'
            '<div class="cap" style="margin-top:1.2em">what it costs her shop</div>'
            f'<div style="position:relative"><div class="over" style="width:{tot/60*100:.1f}%">{inner}</div>'
            f'<div class="mark" style="left:{60/tot*100:.1f}%"></div></div>'
            '<div style="margin-top:1.1em;font-size:clamp(15px,2.1vw,29px);font-weight:800;color:var(--bad)">'
            'the costs run past the end of the money &nbsp;&rarr;&nbsp; &minus;$1.78</div></div>')

def viz_bars(rows, unit='$'):
    """rows = [(label, value, text, color)] — value drives width."""
    mx=max(abs(v) for _,v,_,_ in rows) or 1
    out=''
    for lbl,v,txt,col in rows:
        w=max(abs(v)/mx*100,7)
        out+=(f'<div class="row"><div class="lbl">{lbl}</div>'
              f'<div class="rail"><div class="fill" style="width:{w:.1f}%;background:{GR[col]}">{txt}</div></div></div>')
    return f'<div class="viz">{out}</div>'

def viz_funnel():
    stops=[('the ad',100),('lands',78),('popup',70),('product',52),('offer',44),('cart',34),('leaves',20),('checkout',15),('paid',11)]
    out=''
    for i,(t,h) in enumerate(stops):
        bg = GR['gold'] if i==0 else (GR['red'] if i==6 else (GR['green'] if i==8 else None))
        st=f'height:{h}%;'+(f'background:{bg}' if bg else '')
        out+=f'<div style="{st}"><span>{t}</span></div>'
    return ('<div class="viz"><div class="cap">everyone who saw the ad &nbsp;&rarr;&nbsp; who actually paid</div>'
            f'<div class="fun">{out}</div>'
            '<div style="margin-top:2.6em;color:var(--bad);font-weight:800;font-size:clamp(13px,1.6vw,21px)">'
            '~70% of carts end at that red step. That is normal, not failure.</div></div>')

def viz_shop_online():
    return ('<div class="viz grid2">'
            '<div class="tile"><h4 class="dim">A SHOP</h4>'
            '<p style="font-size:clamp(28px,4vw,56px);line-height:1;margin:.3em 0">&#128100;&nbsp;&rarr;&nbsp;&#10067;</p>'
            '<p class="dim">She walks in. She browses. She leaves.</p>'
            '<p style="margin-top:.5em"><span class="pill" style="background:var(--bad);color:#fff">gone &mdash; no name, no record</span></p></div>'
            '<div class="tile hot"><h4 class="acc">ONLINE</h4>'
            '<p style="font-size:clamp(28px,4vw,56px);line-height:1;margin:.3em 0">&#128100;&nbsp;&rarr;&nbsp;&#128231;</p>'
            '<p class="dim">Came from that ad. Viewed it three times. Left at shipping.</p>'
            '<p style="margin-top:.5em"><span class="pill" style="background:var(--acc);color:#0d1117">on a list &mdash; you can talk to her tomorrow</span></p></div>'
            '</div>')

def viz_timeline():
    pts=[(0,'order','',0),(9,'ships','',0),(20,'arrives','',0),(33,'how to use it','week 1',0),
         (50,'review','week 2',0),(75,'&#8220;running low?&#8221;','week 6',1),(96,'REORDERS','week 8',2)]
    out=''
    for x,lab,sub,big in pts:
        col='var(--acc)' if big==1 else ('var(--good)' if big==2 else 'var(--dim)')
        out+=f'<i class="{"big" if big else ""}" style="left:{x}%;background:{col}"></i>'
        out+=f'<b style="left:{x}%;top:{-8 if big else 4}px;color:{col};font-size:{"1.15em" if big else "1em"}">{lab}</b>'
        if sub: out+=f'<s style="left:{x}%;bottom:2px">{sub}</s>'
    return ('<div class="viz"><div class="cap">the eight weeks after she pays</div>'
            f'<div class="tl">{out}</div>'
            '<div style="margin-top:.4em;color:var(--acc);font-weight:800;font-size:clamp(13px,1.7vw,22px);text-align:right">'
            'week 6 is worth more than the ad that found her</div></div>')

def viz_dots():
    a=''.join('<i style="background:var(--acc)"></i>' for _ in range(100))
    b=''.join(f'<i style="background:{"var(--acc)" if i%20==0 else "#252b33"}"></i>' for i in range(600))
    css='<style>.dots i{display:block;width:100%;aspect-ratio:1;border-radius:1px}</style>'
    return (css+'<div class="viz grid2">'
            '<div class="tile"><h4 class="dim">SHOP A &mdash; 100 customers, <b class="acc">100%</b> loyal</h4>'
            f'<div class="dots" style="grid-template-columns:repeat(20,1fr);max-width:60%;margin:.8em 0">{a}</div>'
            '<p style="color:var(--bad);font-weight:800">&asymp;100 extra orders &mdash; still dead</p></div>'
            '<div class="tile hot"><h4 class="dim">SHOP B &mdash; 20,000 customers, <b class="acc">5%</b> loyal</h4>'
            f'<div class="dots" style="grid-template-columns:repeat(40,1fr);margin:.8em 0">{b}</div>'
            '<p style="color:var(--good);font-weight:800">&asymp;3,000&ndash;4,000 extra orders &mdash; real money</p></div>'
            '</div>')

def viz_grow_keep():
    return ('<div class="viz grid2">'
            '<div class="tile"><h4 style="color:var(--good)">REFERRAL &nbsp;&rarr;&nbsp; grows it</h4>'
            '<p style="font-size:clamp(30px,4.4vw,60px);line-height:1;margin:.25em 0">&#8594;&#11044;&#8592;</p>'
            '<p class="dim">New people arrive with trust already loaded. You pay only when it works.</p></div>'
            '<div class="tile hot"><h4 class="acc">LOYALTY &nbsp;&rarr;&nbsp; monetises it</h4>'
            '<p style="font-size:clamp(30px,4.4vw,60px);line-height:1;margin:.25em 0">&#8635;&#11044;&#8594;$</p>'
            '<p class="dim">The same people, chosen again. Nothing new arrives.</p></div>'
            '</div>')

def viz_once_again():
    once='<i style="background:var(--acc);left:2%"></i>'
    again=''.join(f'<i style="background:{"var(--acc)" if i==0 else "var(--good)"};left:{2+i*15}%"></i>' for i in range(7))
    return ('<div class="viz"><div class="cap">bought once &mdash; mattress, cookware, luggage</div>'
            f'<div class="tl" style="height:52px">{once}<s style="left:12%;bottom:0">then nothing for years</s></div>'
            '<div class="cap" style="margin-top:.8em">bought again &mdash; soap, shampoo, razors, skincare</div>'
            f'<div class="tl" style="height:52px">{again}<s style="left:80%;bottom:0">this is where we live</s></div></div>')

def viz_confession():
    rows=[('Klaviyo','I cannot reach my visitors again'),('Rebuy','my orders are too thin'),
          ('Recharge','customers buy once and vanish'),('Gorgias','I am drowning in <i>where is my order</i>'),
          ('a loyalty app','I have a base and nothing brings them back')]
    out=''.join('<div class="row" style="grid-template-columns:clamp(110px,15vw,210px) 1fr">'
                f'<div><span class="pill" style="background:var(--acc);color:#0d1117">{a}</span></div>'
                f'<div style="font-size:clamp(14px,1.8vw,25px)">&ldquo;{f}&rdquo;</div></div>' for a,f in rows)
    return ('<div class="viz"><div class="cap">what they bought &nbsp;&rarr;&nbsp; what they were afraid of</div>'+out+'</div>')

def viz_points_credit():
    def t(title,sub,items,cls,col):
        li=''.join(f'<li>{i}</li>' for i in items)
        return (f'<div class="tile {cls}"><h4 style="color:{col}">{title}</h4>'
                f'<p style="font-weight:700;margin-bottom:.3em">{sub}</p><ul>{li}</ul></div>')
    return ('<div class="viz grid2">'
            +t('POINTS','the brand&rsquo;s currency',['abstract &mdash; needs explaining','feels like belonging, progress',
               'you name it, you theme it','some are never redeemed'],'hot','var(--acc)')
            +t('STORE CREDIT','money with your logo on it',['understood instantly','feels like a transaction',
               'looks like money, not like you','spent fast &mdash; you hold their cash'],'','var(--good)')
            +'</div>')

def viz_boxes():
    bx=[('GET PEOPLE IN','ads, email, they remember you',0),('ON THE SITE','home, product, cart, popup',0),
        ('PAY','checkout, discount, shipping',0),('AFTER THE ORDER','email, where is my order, refund',0),
        ('COME BACK','refill, drop, membership',1),('MONEY','order 1 cost them. order 2 is the win',1)]
    out=''.join(f'<div class="tile {"hot" if h else ""}"><h4 style="color:{"var(--acc)" if h else "var(--fg)"}">{t}</h4>'
                f'<p class="dim">{s}</p></div>' for t,s,h in bx)
    return f'<div class="viz" style="display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(10px,1.4vw,20px)">{out}</div>'

def viz_stage():
    rows=[('no real base yet','expand the base &mdash; <b>REFERRAL</b>','var(--good)'),
          ('a base, but they buy once','a reason to return &mdash; <b>POINTS</b>','var(--acc)'),
          ('a base, discounting everyone','stop the blanket discount &mdash; <b>TIERS</b>','var(--acc)')]
    out=''.join('<div class="row" style="grid-template-columns:1fr auto 1fr;gap:1.2em">'
                f'<div class="tile" style="padding:.7em 1em;font-size:clamp(13px,1.6vw,22px)">{l}</div>'
                f'<div style="color:{c};font-size:clamp(16px,2vw,28px)">&rarr;</div>'
                f'<div style="color:{c};font-size:clamp(13px,1.7vw,23px);font-weight:700">{r}</div></div>' for l,r,c in rows)
    return f'<div class="viz">{out}</div>'

def viz_dtc():
    boxes=[('factory',1),('brand',1),('distributor',0),('shop',0),('you',1)]
    out=''
    for i,(t,on) in enumerate(boxes):
        if on: st=f'background:{GR["gold"]};color:#0d1117'
        else:  st='background:var(--card);color:var(--dim);text-decoration:line-through;opacity:.55;border:1px solid var(--line)'
        out+=f'<div style="{st};padding:.75em 1em;border-radius:10px;font-weight:800;font-size:clamp(13px,1.7vw,24px)">{t}</div>'
        if i<4: out+='<div style="color:var(--dim);font-size:clamp(14px,1.8vw,26px)">&rarr;</div>'
    return ('<div class="viz"><div style="display:flex;align-items:center;gap:.6em;flex-wrap:wrap">'+out+'</div>'
            '<p style="margin-top:1.1em;color:var(--bad);font-weight:800;font-size:clamp(14px,1.9vw,26px)">'
            'they deleted the shop &mdash; and bought an ad instead, for every single customer</p></div>')

def WHYNOT(q, yes_t, yes_b, no_t, no_b, note, kind='slide'):
    """question -> real case both ways. why it works, why it does not."""
    return {'k':kind,'h':f'<h2>{q}</h2>'
        '<div class="viz grid2">'
        f'<div class="tile hot"><h4 class="acc">WHY &mdash; {yes_t}</h4><p>{yes_b}</p></div>'
        f'<div class="tile" style="border-color:var(--bad)"><h4 style="color:var(--bad)">WHY NOT &mdash; {no_t}</h4><p>{no_b}</p></div>'
        '</div>','n':note}

def BRAND(n, q, note):
    """The recurring beat: stop, go to tonight's real brand, answer one question."""
    return {'k':'look','h':f'<div class="cap">tonight&rsquo;s brand &nbsp;·&nbsp; breakdown {n}</div>'
            f'<h2 style="margin-top:.2em">On the screen. Together.</h2>'
            f'<p class="punch" style="margin-top:.8em">{q}</p>'
            f'<p class="dim" style="margin-top:1.2em">Fill it on the sheet as we go. This is the same sheet you use alone in 40 minutes.</p>','n':note}

# ═══════════════ SESSION 1 — THE BASICS ═══════════════
S1=[
{'h':'<h1>How a shop<br>makes money</h1><p class="dim" style="margin-top:1em">Session 1 · the basics · no website, no app, no Joy</p>'
 ,'n':'Goal: a shop is a business, not a website. Tonight is arithmetic on real things. We break down one real brand together as we go, and you break down another one at the end.'},

{'k':'ask','h':'<h2>You can buy this shirt for <span class="acc">$30</span>.</h2><p class="punch">What do you sell it for?</p>'
 '<p class="dim" style="margin-top:1.4em">Everyone answers. No wrong answers yet.</p>'
 ,'n':'Write every answer up. Someone will say sixty. Keep them all on the board — you come back to them at the end.'},

{'h':'<h2>Start with something you have held</h2>'+viz_shoe()+
 '<p class="dim" style="margin-top:.3em">Sources: WearTesters, Solereview, adidas &amp; Nike annual reports</p>'
 ,'n':'A hundred dollar shoe costs about twenty-eight to make. The brand sells it to the shop for fifty. The shop sells it to you for a hundred. And after marketing, R&D, admin and tax, adidas keeps about two dollars. Two. Let that number sit — nobody in the room expects it.'},

{'h':'<h2>So price is <span class="acc">layers</span>, not cost</h2>'+viz_layers()+
 '<p style="margin-top:.4em">Every layer is somebody who <b class="acc">has to eat</b> — rent, staff, a shelf, a warehouse.</p>'
 ,'n':'The shop is not greedy. The shop has rent. Point at the gap between thirty and a hundred: none of that is shirt.'},

{'h':'<p class="punch">The further a product travels from the factory, the <em>more mouths</em> it has to feed.</p>'
 '<p class="punch" style="margin-top:1.1em">A discount does not eat the profit. It eats <em>the layer that was paying for everything else.</em></p>'
 ,'n':'Remember the second one. Every time a merchant flinches at a discount, this is why. If adidas keeps two dollars, a ten percent discount does not cut their profit — it erases it four times over.'},

{'h':'<h2>Which is why DTC exists</h2>'+viz_dtc()
 ,'n':'Sell straight to the person, keep the layers. That is why a DTC brand can charge less and still keep more. But nothing is free — and unlike a shop, you pay the ad again for every single customer. The shop was a fixed cost. The ad is a per-customer cost. That is the whole game.'},

{'k':'watch','h':'<h2>The clearest example ever filmed</h2>'
 '<p><b>Dollar Shave Club</b>, March 2012. 90 seconds.</p>'
 '<ul><li>Shot in one day for <b class="acc">$4,500</b></li>'
 '<li><b class="acc">12,000 orders</b> in 48 hours — the servers fell over</li>'
 '<li>~25M views · sold to Unilever for <b class="acc">~$1B</b></li></ul>'
 '<div class="res">youtube.com/watch?v=RBHMf7BNd8o</div>'
 ,'n':'Watch it, then ask: what did they delete? The supermarket shelf. And what replaced it — subscription replaced remembering to buy, referral replaced the shelf. Their innovation was the price structure, not the razor.'},

BRAND(1,'What does tonight&rsquo;s brand sell &mdash; and what do you think it costs them to make?',
 'Open the real site. Find the hero product and its price. Guess the cost to make it out loud, as a room. You will be roughly right, and being roughly right is the whole skill.'),

{'k':'board','h':'<h2>Now back to your shirt</h2><p class="punch">$30 &rarr; you said <em>$60</em>.</p>'
 '<p style="margin-top:1em">Let us find out what actually stays in your pocket.</p>'
 ,'n':'Whiteboard from here. Build it line by line with the room. Do NOT show them the picture.'},

{'h':'<h2>Order one</h2>'+viz_eaten()
 ,'n':'You sold a shirt and you are down one dollar seventy-eight. The costs literally overflow past the money she paid — that is the point of the picture.'},

{'h':'<h2>And nothing else is paid yet</h2>'
 '<p class="mono dim" style="font-size:clamp(16px,2.2vw,30px)">Shopify plan &middot; apps &middot; salary &middot; rent &middot; tax</p>'
 '<p class="punch" style="margin-top:1em">The honest number is closer to <em class="neg">&minus;$8</em>.</p>'
 '<p class="dim" style="margin-top:1em">The app stack alone is often ~10% of revenue at this size.</p>'
 ,'n':'Stop here. Let it sit. Do not rescue them.'},

{'k':'ask','h':'<p class="punch">So why would anybody <em>run this business?</em></p>'
 ,'n':'Say nothing. Wait. Somebody will get close.'},

{'h':'<h2>Because of the second one</h2>'+
 viz_bars([('ORDER 1',-2,'&minus;$2 &nbsp; paid for the ad, nothing else','red'),
           ('ORDER 2',22,'+$22 &nbsp; no ad. no first-order discount.','green')])+
 '<p class="punch" style="margin-top:.5em">The business is not the shirt.<br>It is the <em>second shirt.</em></p>'
 ,'n':'Same shirt, same price. The only difference is nobody had to pay to find her. Write this down — everything for the next four weeks comes back to it.'},

BRAND(2,'Would anybody buy tonight&rsquo;s product <em>twice</em>? How soon?',
 'Look at the product again. Does it run out? Wear out? Is there a next size, next drop, next flavour? If the honest answer is no, say so — that is a real finding, not a failure.'),

{'h':'<h2>So how much are you <em class="acc">allowed</em> to spend?</h2>'+
 viz_bars([('1 order',13.22,'$13.22 &nbsp; your ceiling if she never returns','slate'),
           ('3 orders',57,'$57 &nbsp; now you can spend $30&ndash;40 and still win','gold')])+
 '<p style="margin-top:.5em">How long she stays decides <b class="acc">what you are allowed to pay</b> to get her.</p>'
 ,'n':'Same product, same ad, same market — the brand that gets a second order can outspend the brand that does not. Retention is not a nice-to-have. It is how you afford to compete at all.'},

{'h':'<h2>Not every product is the same business</h2>'+viz_once_again()
 ,'n':'One question — bought once or bought again — predicts most of what a merchant does, including whether they need us at all. Session four is built on this.'},

{'h':'<h2>And every shop is these six boxes</h2>'+viz_boxes()+
 '<p style="margin-top:.5em">Every merchant message you will ever read is about <b class="acc">one box</b>.</p>'
 ,'n':'Your map for next week. We live in COME BACK — but you cannot help someone there if you do not know the other five exist.'},

{'h':'<h2>Your two fears, as arithmetic</h2>'
 '<div class="grid2"><div class="tile"><h4>1 &middot; They vanish</h4>'
 '<p class="dim">I keep buying new people who never come back &mdash; only ever booking the first table.</p></div>'
 '<div class="tile"><h4>2 &middot; I discount the wrong people</h4>'
 '<p class="dim">The $9 handed to someone who was already buying. And adidas only keeps $2.</p></div></div>'
 ,'n':'These are not feelings. They are the two pictures you just built. When a merchant sounds scared, it is one of these two.'},

{'k':'drill','h':'<h2>Now you &mdash; your own brand</h2>'
 '<ul><li>Pairs. A brand you have <b>not</b> seen tonight</li>'
 '<li>Teardown sheet <b>&sect;0&ndash;1</b> &mdash; same questions we just did together</li></ul>'
 '<p class="punch" style="margin-top:1em">At that margin, <em>how many orders</em> before they are ahead?</p>'
 ,'n':'Homework: sections 0-1 on two more brands. Classify each bought-once or bought-again. And: what does one order cost YOUR store?'},
]

S1.insert(5, WHYNOT('So should a shop ever discount?',
 'yes &mdash; to win a stranger','She has never heard of you. $9 buys a first order you would not otherwise get, '
 'and her email, which is worth more than the $9.',
 'no &mdash; to someone already buying','That same $9 goes to people who were coming anyway. '
 'On a $100 shoe adidas keeps $2 &mdash; a 10% discount does not shrink that profit, it <b>erases it four times over</b>.',
 'This is fear number two, and it is why merchants agonise over discounts that look small to us. Ask the room which one the popup on most sites is doing. Answer: both, at the same time, and nobody measures the split.'))

# ═══════════════ SESSION 2 — BREAK DOWN A BRAND ═══════════════
S2=[
{'h':'<h1>Break down<br>a brand</h1><p class="dim" style="margin-top:1em">Session 2 · the method · phones out</p>'
 ,'n':'Goal: open a brand you have never seen and say what it is doing and where it loses people. Tonight we do one together, slowly, then you do one alone.'},

{'h':'<h2>One sheet. Any brand. No login.</h2>'
 '<p class="punch"><em>Outside-in:</em> if you cannot see it on the public site, it is not on the sheet.</p>'
 '<p style="margin-top:1.2em">No ad account. No merchant interview. No Joy admin.</p>'
 '<p class="dim" style="margin-top:.6em">First time ~45 min. By next month, 15.</p>'
 ,'n':'This is the skill the whole course exists to give you. Everything else is context for this.'},

{'h':'<h2>Why you can do this at all</h2>'+viz_shop_online()+
 '<p class="punch" style="margin-top:.6em">In a shop, someone who leaves is <em>gone.</em><br>Online, someone who leaves is <em>a list.</em></p>'
 ,'n':'That is why the popup exists, why retargeting exists, why abandoned-cart email is the most profitable email in ecom. And it is why loyalty works at all — loyalty is identity applied over time. In a shop you need a plastic card for that. Online it is just an account.'},

{'h':'<h2>The path you are looking for</h2>'+viz_funnel()
 ,'n':'Nine steps from stranger to paid. Walking a brand means finding where people fall out. Not fixing it — finding it.'},

BRAND(1,'Where does tonight&rsquo;s brand get its people from?',
 'Ad Library first — are they running ads, and what do the ads promise? Then check: Instagram linked? A blog? A quiz? A popup? Name the main door out loud before moving on.'),

{'k':'look','h':'<h2>Click the ad. Land on the page.</h2>'
 '<div class="res">facebook.com/ads/library</div>'
 '<p class="punch" style="margin-top:1.2em">Does the page <em>repeat the promise</em> the ad just made?</p>'
 '<p class="dim" style="margin-top:1em">Same photo? Same claim? Same price? Same offer?</p>'
 ,'n':'The most common way to waste thirty dollars in this business: the ad promises one thing and the page says another. She assumes she misread it, and leaves. Do this live with tonight brand.'},

WHYNOT('Should a shop run a popup?',
 'yes &mdash; it buys her identity','Not the sale &mdash; the <b>email</b>. Without it you cannot recover a cart, '
 'send a refill reminder, or retarget. Everything after this depends on it.',
 'no &mdash; not like that','Fires instantly, on mobile, before she has seen anything &mdash; she bounces. '
 'And the 10% goes to people who would have paid full price. <b>Fear #2 in the first thirty seconds.</b>',
 'A popup is not good or bad. Timing and offer decide which of the two columns it lands in. Trigger tonight brand popup live and let the room judge which one it is.', 'look'),

{'h':'<h2>The product page answers three silent questions</h2>'
 '<p class="punch">Will this work for me?<br>Can I trust you?<br>What if I hate it?</p>'
 '<p style="margin-top:1.2em">Reviews answer all three &mdash; cheaper than any copy you could write.</p>'
 '<p class="dim" style="margin-top:.8em">A hidden returns policy kills the sale. A stranger will not risk $42 on a shop that will not say what happens if it fails.</p>'
 ,'n':'On tonight brand: are there reviews? With faces? Is the returns policy findable in one click?'},

WHYNOT('Subscribe &amp; save, or a bundle?',
 'subscription &mdash; buys <b>LTV</b>','The next order is already agreed. Predictable revenue, and she stops shopping around. '
 'Costs ~15% margin, forever.',
 'bundle &mdash; buys <b>AOV</b>','A fatter order today. Right when there may never be a second order. '
 'Less margin per unit, but the cash is now.',
 'Different problems, opposite answers. A shop with a repeat problem needs the first. A shop with thin orders needs the second. Do not let anyone say them in the same breath. And note the trap: a sub discount so deep the shop loses money on its most loyal customers — fear two again.'),

{'k':'look','h':'<h2>The cart, and the strongest lever in ecom</h2>'
 '<p class="punch">"You are <em>$12 away</em> from free shipping."</p>'
 '<p style="margin-top:1.2em">She would rather add $12 of product than pay $7 of shipping for nothing.</p>'
 '<p class="dim" style="margin-top:1em">Set it too high and it stops being a nudge and becomes a wall.</p>'
 ,'n':'Add to cart live so they watch the bar move. Free shipping thresholds move AOV more than almost anything else — but the threshold has to sit above the point where the maths works, or the merchant is just paying postage.'},

{'h':'<h2>Checkout &mdash; where intent goes to die</h2>'
 '<div class="viz grid2"><div class="tile" style="border-color:var(--bad)"><h4 style="color:var(--bad)">39%</h4>'
 '<p>abandon over <b>extra costs</b> &mdash; shipping, tax, fees. The number one reason.</p></div>'
 '<div class="tile"><h4 class="dim">~70%</h4><p>of all carts are abandoned. That is <b>normal</b>, not failure.</p></div></div>'
 '<ul style="margin-top:.4em"><li>The discount code box is a <b>leak</b> &mdash; they leave to hunt a code</li>'
 '<li>Express wallets: five fields &rarr; one thumbprint</li>'
 '<li>Guest checkout &mdash; do not force an account on a stranger</li></ul>'
 '<div class="res">baymard.com/lists/cart-abandonment-rate</div>'
 ,'n':'A seven dollar fee on a forty-two dollar order reads as a seventeen percent price rise. It is the surprise, not the price.'},

{'h':'<p class="punch">"Conversion is down" is <em>not a problem.</em></p>'
 '<p style="margin-top:1em">It is a symptom of a leak at one specific step.</p>'
 '<p class="punch" style="margin-top:1.2em">An AM finds the step.<br><span class="dim">CS forwards the sentence.</span></p>'
 ,'n':'That sentence is the difference between the two jobs. That is all it is.'},

{'k':'look','h':'<h2>Now read what they installed</h2>'
 '<p class="mono dim">right-click &rarr; View Page Source &rarr; Ctrl-F</p>'
 '<div class="res mono">klaviyo &middot; attentive &middot; recharge &middot; appstle &middot; skio &middot; smile<br>'
 'yotpo &middot; loyaltylion &middot; rivo &middot; growave &middot; okendo &middot; judge.me<br>gorgias &middot; rebuy &middot; subscribe</div>'
 '<p style="margin-top:1em">Then the footer &middot; <span class="mono">/account</span> &middot; <span class="mono acc">/pages/rewards</span></p>'
 ,'n':'Do it live on tonight brand. Sixty seconds and you know more than a discovery call would tell you.'},

{'h':'<h2>The stack is a confession</h2>'+viz_confession()
 ,'n':'Nobody installs a bundle app for fun. They installed it at 11pm after looking at a number that scared them. The stack tells you what the owner is afraid of before they say a word.'},

BRAND(2,'What is tonight&rsquo;s owner <em>paying to fix</em> &mdash; and is it their real leak?',
 'This is the whole session landing. Read their stack, name the fear, then ask whether that fear matches where you actually watched people fall out on the path. Often it does not — and that gap is the job.'),

{'k':'drill','h':'<h2>Now you &mdash; a brand you have not seen</h2>'
 '<ul><li>Pairs, <b>phones out</b>, real money in the cart</li>'
 '<li>Walk it as a customer. Fill <b>&sect;0&ndash;6</b> &mdash; same questions we just did together</li>'
 '<li>Every step: what you saw &middot; what they wanted &middot; <b>what would make you quit</b></li></ul>'
 '<p class="punch" style="margin-top:1em">The main door, the place you would quit, and <em>what this owner is paying to fix.</em></p>'
 ,'n':'Homework: a full teardown on two more brands. Walk your own store and mark where you would quit. Three tickets — which step is each really about?'},
]

# ═══════════════ SESSION 3 — WHY PEOPLE COME BACK ═══════════════
S3=[
{'h':'<h1>Why people<br>come back</h1><p class="dim" style="margin-top:1em">Session 3 · retention and loyalty · our own subject</p>'
 ,'n':'Goal: why a person buys a second time, and what actually makes them. Tonight we break down TWO brands — one with a strong reason to return, one with none.'},

{'h':'<h2 class="dim">Last week ended the moment she paid.</h2>'
 '<p class="punch">Every business thinks that is the finish line.</p>'
 '<p class="punch" style="margin-top:.6em">It is <em>the start.</em></p>'
 ,'n':'Everything tonight is after the money changed hands.'},

{'h':'<h2>The wait</h2>'
 '<p class="mono dim" style="font-size:clamp(16px,2.4vw,32px)">paid &mdash;&mdash;&mdash;&mdash;&mdash; ? &mdash;&mdash;&mdash;&mdash;&mdash; arrived</p>'
 '<p style="margin-top:1.2em">Nothing happens here. That <b>is</b> the problem.</p>'
 '<p style="margin-top:.8em">This gap is where every <b class="acc">"where is my order"</b> ticket is born &mdash; '
 'usually the biggest ticket category in ecom.</p>'
 ,'n':'You already live in this one. A late parcel someone warned you about is fine. A late parcel nobody mentioned is a refund and a one-star review. Ask the room how many WISMO tickets they closed last week.'},

{'h':'<h2>The eight weeks after she pays</h2>'+viz_timeline()+
 '<p class="dim" style="margin-top:.4em">The review is asked when she has <b>used</b> it &mdash; not when it arrived. A day-one review is a review of the packaging.</p>'
 ,'n':'Week six: you arrive before she runs out and before she thinks about alternatives. One automated email, sent to somebody who already likes them, beats thirty dollars of advertising.'},

BRAND(1,'What does tonight&rsquo;s brand send you <em>after</em> you buy?',
 'Use their own inbox — they placed real orders in the build track. Put a real confirmation, shipping note and review request on the screen. Then ask: did anyone get a "running low" email? Almost nobody will have. That absence is the finding.'),

{'k':'ask','h':'<p class="punch">Why would a human buy <em>this</em> twice?</p>'
 '<p class="dim" style="margin-top:1.4em">Ask it about both brands on the table tonight.</p>'
 ,'n':'Let the room struggle on the weak one. Do not rescue them. The struggle is the lesson.'},

WHYNOT('Does a loyalty program help this shop?',
 'Lumi &mdash; a refill brand','$42 moisturizer, runs out every 8 weeks. She has to rebuy <b>something</b> &mdash; '
 'points decide it is Lumi, and decide it is <b>now</b> rather than in three weeks.',
 'HexClad &mdash; premium cookware','A pan is a five-year decision. Give her 400 points and they <b>expire before they are worth anything</b>. '
 'You added a widget, a cost and a promise, and produced no second order.',
 'Some very good brands should not run a points program. If you cannot say that out loud you are selling, not advising. HexClad answer is referral and range — sell them a lid, a knife, another size, or get them to bring someone new.'),

{'h':'<h2>Sometimes there is genuinely no reason</h2>'+viz_once_again()+
 '<p style="margin-top:.4em">That is not a failure of the shop. It is a <b class="acc">fact about the product</b> &mdash; and it decides everything they need.</p>'
 ,'n':'This is the uncomfortable one, and it is the whole setup for next week.'},

{'h':'<h2>Lumi, all the way through</h2>'+
 viz_bars([('ORDER 1',2.13,'+$2.13 &nbsp; she spent $61.20','slate'),
           ('ORDER 2',17.28,'+$17.28 &nbsp; she spent $42, no ad attached','green')])+
 '<p class="punch" style="margin-top:.5em">One order with no ad attached is worth <em>eight</em> of the first one.</p>'
 ,'n':'Same shop, same product, same customer. The first order paid for the ad and almost nothing else.'},

{'h':'<h2>Order 1 &mdash; where it all went</h2><table>'
 '<tr><td>Ad to reach Mai</td><td class="n neg">&minus;$30.00</td></tr>'
 '<tr><td>Cart: moisturizer + travel size</td><td class="n">+$68.00</td></tr>'
 '<tr><td>Popup 10%</td><td class="n neg">&minus;$6.80</td></tr>'
 '<tr><td>Free shipping, Lumi pays it</td><td class="n neg">&minus;$7.00</td></tr>'
 '<tr><td>Processing</td><td class="n neg">&minus;$2.07</td></tr>'
 '<tr><td>Products</td><td class="n neg">&minus;$20.00</td></tr>'
 '<tr class="tot"><td>Lumi keeps</td><td class="n acc">+$2.13</td></tr></table>'
 ,'n':'Mai spent sixty-one twenty. The shop kept two thirteen. Stop talking for a second.'},

{'h':'<h2 class="dim">So what did the points actually do?</h2>'
 '<p class="punch">They did not make Mai <em>like</em> Lumi.</p>'
 '<p style="margin-top:1.2em">They gave her a reason to choose Lumi <b>instead of the alternative</b>, in that moment '
 '&mdash; and a nudge to do it <b>now</b> rather than in three weeks.</p>'
 '<p class="punch" style="margin-top:1.2em">Loyalty does not buy affection.<br>It buys <em>timing and preference.</em></p>'
 ,'n':'If you remember one sentence about our product, make it that one.'},

{'h':'<h2>Three things, not one thing</h2>'
 '<div class="viz" style="display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(10px,1.5vw,22px)">'
 '<div class="tile"><h4>SUBSCRIPTION</h4><p class="dim">the next box is already agreed</p></div>'
 '<div class="tile hot"><h4 class="acc">LOYALTY</h4><p class="dim">a reason to choose <b>you</b> next time</p></div>'
 '<div class="tile"><h4>DISCOUNT</h4><p class="dim">this order is cheaper</p></div></div>'
 '<p class="punch" style="margin-top:.6em">A standing order does not mean she <em>chose</em> you.<br>'
 '<span class="dim" style="font-size:.7em">It means she has not cancelled yet.</span></p>'
 ,'n':'Merchants mix these up constantly. If you mix them up too, you cannot help them. And that gap — between not-cancelled and chosen — is exactly what we sell.'},

{'h':'<h2>Two machines, opposite jobs</h2>'+viz_grow_keep()
 ,'n':'A referred person arrives with trust already loaded, and you pay only when it works — unlike an ad, which you pay on hope. Remember this: next week it decides what you recommend to a real merchant.'},

WHYNOT('They ask for store credit. Do you just switch it on?',
 'credit fits &mdash; considered, rare, returns','Expensive one-off purchases, or a shop with lots of returns. '
 'Credit is understood instantly and <b>keeps the money in the shop</b> instead of refunding it out.',
 'points fit &mdash; refill, habit, membership','Credit is money with your logo on it &mdash; transactional, no attachment, '
 'and <b>you are holding their cash</b>. Points are the brand&rsquo;s currency, and they build a habit.',
 'Neither is the default. Ask stage, product, repurchase cycle, return rate — then recommend, and be able to say what the other option loses. That last part is the job.'),

{'h':'<h2>Points or credit &mdash; the whole trade</h2>'+viz_points_credit()+
 '<p class="punch" style="margin-top:.4em">Points are the brand&rsquo;s <em>currency</em>.<br>Store credit is just <em>money with your logo on it.</em></p>'
 ,'n':'Which is also why on-brand is not decoration. If the widget looks like a generic app bolted on, it is not brand currency any more — it is a coupon machine, and you threw away the only reason you chose points.'},

{'k':'ask','h':'<h2>VIP tiers &mdash; spend $500 to reach Gold.</h2><p class="punch">Why <em>$500?</em></p>'
 ,'n':'Let them flounder. Nobody can defend it, because today the number is guessed. That is the problem.'},

{'h':'<h2>Where the number actually comes from</h2>'
 '<ul><li>Pull customers with total spend, last 12 months</li><li>Sort, highest first</li>'
 '<li>Decide the share per tier &mdash; commonly <b class="acc">~5% top, ~20% middle</b></li>'
 '<li>The spend at that cut line <b>is</b> your threshold</li></ul>'
 '<div class="viz grid2" style="margin-top:1em">'
 '<div class="tile" style="border-color:var(--bad)"><h4 style="color:var(--bad)">too high</h4>'
 '<p class="dim">nobody reaches it &mdash; decoration</p></div>'
 '<div class="tile" style="border-color:var(--bad)"><h4 style="color:var(--bad)">too low</h4>'
 '<p class="dim">everybody clears it &mdash; a discount for everyone. <b>Fear #2 with extra steps.</b></p></div></div>'
 '<p class="punch" style="margin-top:.6em">If you cannot say <em>why the number is that number</em>, do not set it.</p>'
 ,'n':'And the reason tiers exist at all is fear two: otherwise you hand the same coupon to a first-time buyer and to someone who spends two thousand a year.'},

{'k':'drill','h':'<h2>Now you &mdash; two brands, and a recommendation</h2>'
 '<ul><li>Pairs. One brand with a strong repeat reason, one with a weak one</li>'
 '<li>Teardown <b>&sect;4&ndash;5</b>, then <b>prescribe</b></li></ul>'
 '<p class="punch" style="margin-top:1em">Points, credit, tiers or referral &mdash; and <em>what does the option you rejected lose?</em></p>'
 ,'n':'The rejected option is the grading criterion. Anyone can pick something. Only someone who understands it can say what the alternative costs.'},
]

# ═══════════════ SESSION 4 — BRING IT TOGETHER ═══════════════
S4=[
{'h':'<h1>Bring it<br>together</h1><p class="dim" style="margin-top:1em">Session 4 · a real merchant, a real call</p>'
 ,'n':'Goal: given a real merchant, say whether it is ours, whether it needs us, and what to do. Tonight: two brands side by side, one of which we should turn down.'},

{'h':'<h2>Three weeks ago you could not do any of this</h2>'
 '<ul><li>How does this shop make money on one order?</li>'
 '<li>How do people arrive, and where do they quit?</li>'
 '<li>Why would someone buy twice &mdash; and what is the brand doing about it?</li></ul>'
 '<p class="punch" style="margin-top:1.2em">Tonight we add the last one: <em>so what do we tell them?</em></p>'
 ,'n':'And you still have not opened Joy once.'},

{'k':'ask','h':'<p class="punch">Is Recharge a <em>subscription app?</em></p>'
 ,'n':'Let them say yes. Then say no — it is a solution for increasing lifetime value. Klaviyo is not an email app, it is a cheap way to talk to everyone at scale plus a CRM. We do not sell an app. We sell the solution the app is made of.'},

{'h':'<h2>Is it ours? Run the checklist</h2><table>'
 '<tr><td>Shopify or Plus</td><td class="n dim">&#9744;</td></tr>'
 '<tr><td>Category that repurchases <span class="dim">&mdash; beauty, apparel, wellness, kids, outdoor, pet, home</span></td><td class="n dim">&#9744;</td></tr>'
 '<tr><td>Roughly $5&ndash;40M</td><td class="n dim">&#9744;</td></tr>'
 '<tr><td><b>Klaviyo or Attentive</b> installed</td><td class="n dim">&#9744;</td></tr>'
 '<tr><td>Growing &mdash; raise, press, retail, viral</td><td class="n dim">&#9744;</td></tr>'
 '<tr><td><b>No</b> Rivo / Yotpo / Smile / LoyaltyLion / Growave</td><td class="n dim">&#9744;</td></tr></table>'
 '<p class="acc" style="margin-top:1em">Every line is visible from the public site. You never ask them.</p>'
 ,'n':'Joy real ICP, not something invented for class. And you already know how to check every line — that was last week.'},

BRAND(1,'Run the checklist on both brands. Out loud, line by line.',
 'One should pass and one should fail. Do not tell them which. Let the checklist do it, and let them notice that they never had to ask the merchant anything.'),

{'h':'<h2>The easiest win to recognise</h2>'
 '<p class="punch">Recharge or Appstle <em>+</em> Klaviyo <em>+</em> no loyalty app</p>'
 '<p style="margin-top:1.4em">They already pay for repeat revenue. They have nothing that gives a reason to <b>return</b>.</p>'
 '<p class="dim" style="margin-top:1em">Subscription is not loyalty &mdash; not-cancelled is not the same as chosen.</p>'
 ,'n':'And it is not a rip-and-replace. Joy sits on top of the sub stack. That is why this one is easy.'},

{'k':'look','h':'<h2>The textbook case</h2><p class="punch">raewellness.co</p>'
 '<ul><li>Recharge, heavily used</li><li>Klaviyo</li><li>Wellness &mdash; natural repurchase</li>'
 '<li><b class="acc">/pages/rewards &rarr; 404</b></li></ul>'
 ,'n':'Do it live. Thirty seconds. Ctrl-F recharge and klaviyo — both hit. Ctrl-F smile, loyaltylion, yotpo — nothing. Then slash pages slash rewards. 404. That is the entire pitch, and they found it themselves.'},

{'k':'ask','h':'<p class="punch">But does this shop need a loyalty program <em>at all?</em></p>'
 ,'n':'This is the question that separates you from a salesperson. Let it hang.'},

{'h':'<h2>A loyalty program is a multiplier</h2>'+viz_dots()+
 '<p class="punch" style="margin-top:.4em">Multiply a small number &mdash; <em>it is still small.</em></p>'
 ,'n':'Shop A has a perfect loyalty program and is going out of business. You cannot multiply your way out of a base of a hundred.'},

WHYNOT('A shop with 100 customers wants points. Do you sell it?',
 'no &mdash; they need a bigger base','Perfect retention on 100 people is still 100 people. '
 'They need <b>referral and acquisition</b> first. Points multiply a base that is not there yet.',
 'and if you sell it anyway','It will not produce a result. They will churn in six months &mdash; '
 '<b>correctly</b> &mdash; and blame us. You did not win an account, you borrowed one.',
 'Telling a survival-stage shop to launch points is not service. It is selling them the wrong thing. And "not ready" is never a dead end — it is a different recommendation.'),

{'h':'<h2>So the first question is stage</h2>'+viz_stage()+
 '<p style="margin-top:.4em">Referral <b>grows</b> the base. Loyalty <b>monetises</b> it. Never confuse the two.</p>'
 ,'n':'The shop that must NOT be sold points is often exactly the shop that should run referral.'},

{'h':'<h2 class="dim">The hardest thing you will have to say</h2>'
 '<p>They installed a bundle app. Their real leak is that <b>nobody comes back.</b></p>'
 '<p class="punch" style="margin:1.2em 0">They are fixing <em>the cart</em> while bleeding at <em>the second order.</em></p>'
 '<p class="punch">Do you <em>tell them?</em></p>'
 ,'n':'Yes. That is the service. That is the whole difference between answering the app and owning the outcome — and it costs something, because you are telling a paying merchant that the thing they bought is not their problem.'},

{'h':'<h2>The conversation, replaced</h2>'
 '<p class="dim">Never: <span class="mono">"Points or store credit? OK, I&rsquo;ll show you where to turn it on."</span></p>'
 '<ul style="margin-top:1em"><li><b>1 Stage</b> &mdash; is there a base to sell back to?</li>'
 '<li><b>2 Base</b> &mdash; how many, how many return, typical basket</li>'
 '<li><b>3 Fear</b> &mdash; losing new people, or over-discounting?</li>'
 '<li><b>4 Mechanism</b> &mdash; referral, points, credit, tiers</li>'
 '<li><b>5 Numbers</b> &mdash; thresholds from their data, defended</li>'
 '<li><b>6 Placement</b> &mdash; from their journey, not the demo store</li></ul>'
 '<p class="punch" style="margin-top:1em">Only step 6 is <em>a screen.</em></p>'
 ,'n':'Steps one to five are the service. That is what we are actually paid for. Call back to the talk — AI took the execution. What is left for people is the outcome.'},

{'h':'<h2>The gate</h2>'
 '<div class="viz grid2"><div class="tile"><h4>1 &middot; A cold teardown</h4>'
 '<p class="dim">a brand you have never seen &middot; 15 minutes &middot; a lead accepts it</p></div>'
 '<div class="tile"><h4>2 &middot; 8 of 12 restatements</h4><p class="dim">timed, from your own queue</p></div></div>'
 '<div class="tile" style="margin-top:clamp(12px,2vw,28px)"><h4>3 &middot; Your store, launched, to standard</h4>'
 '<p class="dim">max three apps, every one defensible</p></div>'
 ,'n':'"Not yet" is a normal outcome here too. It means another stack of reps, not another lecture.'},

{'k':'drill','h':'<h2>Now you &mdash; two brands, one verdict each</h2>'
 '<ul><li><b>Two</b> brands side by side. One strong fit, one deliberately not ours</li>'
 '<li>Full teardown, then a <b>verdict out loud</b> with the reason</li>'
 '<li>Fit is learned by contrast &mdash; never one brand alone</li></ul>'
 '<p class="punch" style="margin-top:1em">Is it ours &middot; does it need this &middot; <em>what is the one thing we would change?</em></p>'
 ,'n':'A checklist memorised is trivia. A checklist run against a brand that fails it is judgement. That is what we grade.'},

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
    print('Done. ← → move · S notes · Cmd-P to PDF.')
