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

# ─────────────────────────────── SESSION 1 ───────────────────────────────
S1=[
{'h':'<h1>Money on<br>one unit</h1><p class="dim" style="margin-top:1em">Session 1 · 2 hours · no Joy, no app, no screens</p>'
 ,'n':'Goal: you can say how a shop makes money on one order, and why the second order is the business.'},

{'k':'ask','h':'<h2>You can buy this shirt for <span class="acc">$30</span>.</h2><p class="punch">What do you sell it for?</p>'
 ,'n':'Shout it out. Take every answer, write them all up, judge none of them. Someone will say sixty.'},

{'h':'<h2>Same shirt. Three prices.</h2><div class="two"><div class="card"><h3 class="dim">Retail shop</h3><p class="punch">$100</p></div>'
 '<div class="card"><h3 class="dim">Outlet, next season</h3><p class="punch">$60</p></div></div>'
 '<p style="margin-top:1.2em">Why? It is not brand. It is not quality.</p>'
 ,'n':'Let them guess. They will say brand and quality. Both mostly wrong.'},

{'h':'<h2>Price is layers</h2><table>'
 '<tr><td>Factory</td><td class="dim">fabric, labour</td><td class="n acc">$30</td></tr>'
 '<tr><td>Brand</td><td class="dim">design, marketing, warehouse</td><td class="n">$60</td></tr>'
 '<tr><td>Distributor</td><td class="dim">moving it, holding stock</td><td class="n">$75</td></tr>'
 '<tr class="tot"><td>Retail shop</td><td class="dim">rent, staff, the shelf</td><td class="n">$100</td></tr></table>'
 ,'n':'Price is not the cost of the thing. Price is a stack of layers, and every layer is somebody who has to eat. The shop is not greedy. The shop has rent.'},

{'h':'<p class="punch">The further a product travels from the factory, the <em>more mouths</em> it has to feed.</p>'
 '<p class="punch" style="margin-top:1em">A discount does not eat the profit. It eats <em>the layer that was paying for everything else.</em></p>'
 ,'n':'Remember the second one. Every time a merchant flinches at a discount, this is why.'},

{'h':'<h2>So DTC deletes the layers</h2>'
 '<p class="mono" style="font-size:clamp(17px,2.4vw,34px)">factory → brand → <s class="dim">distributor</s> → <s class="dim">shop</s> → you</p>'
 '<p style="margin-top:1.2em">Sell straight to the person. Keep the layers.</p>'
 '<p class="punch" style="margin-top:.7em">But they deleted the shop and bought <em>an ad</em> instead.</p>'
 ,'n':'Nothing is free. And unlike a shop, you pay the ad again for every single customer. That is the whole game.'},

{'k':'watch','h':'<h2>The clearest example ever filmed</h2><p><b>Dollar Shave Club</b>, March 2012. 90 seconds.</p>'
 '<ul><li>Shot in one day for <b class="acc">$4,500</b></li><li><b class="acc">12,000 orders</b> in 48 hours — the servers fell over</li>'
 '<li>~25 million views · sold to Unilever for <b class="acc">~$1B</b></li></ul>'
 '<div class="res">youtube.com/watch?v=RBHMf7BNd8o</div>'
 ,'n':'Watch it. Then ask: what did they actually delete? The supermarket shelf. And what replaced it — subscription replaced remembering to buy, referral replaced the shelf. Their innovation was the price structure, not the razor.'},

{'k':'board','h':'<h2>Back to your shirt</h2><p class="punch">$30 → you said <em>$60</em>.</p><p style="margin-top:1em">Let us find out what actually stays in your pocket.</p>'
 ,'n':'Whiteboard from here. Build it live, one line at a time. Do NOT show them the finished table.'},

{'h':'<h2>Order one</h2><table>'
 '<tr><td>Sticker price</td><td class="n">$60.00</td></tr>'
 '<tr><td>15% off <span class="dim">— a stranger needs a reason</span></td><td class="n neg">−$9.00</td></tr>'
 '<tr><td class="dim">Collected</td><td class="n dim">$51.00</td></tr>'
 '<tr><td>The shirt</td><td class="n neg">−$30.00</td></tr>'
 '<tr><td>Shipping</td><td class="n neg">−$6.00</td></tr>'
 '<tr><td>Processing</td><td class="n neg">−$1.78</td></tr>'
 '<tr><td>Ads, to make this person show up</td><td class="n neg">−$15.00</td></tr>'
 '<tr class="tot"><td>Kept</td><td class="n neg">−$1.78</td></tr></table>'
 ,'n':'You sold a shirt and you are down one dollar seventy-eight.'},

{'h':'<h2>And nothing else is paid yet</h2><p class="mono dim" style="font-size:clamp(16px,2.2vw,30px)">Shopify plan · apps · salary · rent · tax</p>'
 '<p class="punch" style="margin-top:1em">The honest number is closer to <em class="neg">−$8</em>.</p>'
 ,'n':'The app stack alone is around ten percent of revenue at this size. Stop here. Let it sit.'},

{'k':'ask','h':'<p class="punch">So why would anybody <em>run this business?</em></p>'
 ,'n':'Say nothing. Wait. Let them answer. Somebody will get close.'},

{'h':'<h2>Because of this one</h2><p class="dim">Order 2 — same customer, eight weeks later</p><table>'
 '<tr><td>Sticker price</td><td class="n">$60.00</td></tr>'
 '<tr><td>First-order discount</td><td class="n dim">none — she is not a stranger</td></tr>'
 '<tr><td>The shirt</td><td class="n neg">−$30.00</td></tr>'
 '<tr><td>Shipping</td><td class="n neg">−$6.00</td></tr>'
 '<tr><td>Processing</td><td class="n neg">−$2.04</td></tr>'
 '<tr><td><b>Ads</b></td><td class="n pos">$0.00 — she came back on her own</td></tr>'
 '<tr class="tot"><td>Kept</td><td class="n pos">+$21.96</td></tr></table>'
 ,'n':'Same shirt. Same price. Twenty-two dollars instead of minus two. The only difference is nobody had to pay to find her.'},

{'h':'<h2 class="dim">The whole business</h2>'
 '<div style="margin:1.4em 0"><p class="dim" style="font-size:.8em">ORDER 1</p>'
 '<div class="bar" style="width:12%;background:var(--bad)">−$2</div></div>'
 '<div><p class="dim" style="font-size:.8em">ORDER 2</p>'
 '<div class="bar" style="width:100%;background:var(--good)">+$22</div></div>'
 '<p class="punch" style="margin-top:1.4em">The business is not the shirt.<br>It is the <em>second shirt.</em></p>'
 ,'n':'Write this down. Everything we do for the next four weeks comes back to this.'},

{'h':'<h2>So how much are you <em class="acc">allowed</em> to spend?</h2><table>'
 '<tr><td>Order 1 keeps, before ads</td><td class="n acc">$13.22</td></tr>'
 '<tr><td>If she only ever buys once, your ceiling is</td><td class="n">$13.22</td></tr>'
 '<tr><td>If she buys three times</td><td class="n acc">≈ $57</td></tr>'
 '<tr class="tot"><td>Now you can spend</td><td class="n pos">$30–40 and still win</td></tr></table>'
 ,'n':'How long a customer stays decides how much you are allowed to pay for her. Same product, same ad, same market — the brand that gets a second order can outspend the brand that does not. That is why retention is not a nice-to-have. It is how you afford to compete at all.'},

{'h':'<h2>Not every product is the same business</h2><table>'
 '<tr><th></th><th>Bought once</th><th>Bought again</th></tr>'
 '<tr><td class="dim"></td><td>mattress, cookware, luggage</td><td>soap, shampoo, razors, skincare</td></tr>'
 '<tr><td class="dim">Shots you get</td><td class="bad"><b>one</b></td><td><b>many</b></td></tr>'
 '<tr><td class="dim">So order 1 must</td><td><b>be squeezed</b></td><td>only cover itself</td></tr>'
 '<tr><td class="dim">They install</td><td>bundle / upsell</td><td>subscription, email, <b class="acc">loyalty</b></td></tr>'
 '<tr><td class="dim">Grows by</td><td>referral, new products</td><td><b>repeat</b></td></tr></table>'
 ,'n':'One question — bought once, or bought again — predicts most of what a merchant does. Including whether they need us at all. Hold onto this. Session four is built on it.'},

{'h':'<h2>Your two fears, as arithmetic</h2>'
 '<div class="card" style="margin-bottom:1em"><h3>1 · I keep buying new people who vanish</h3><p class="dim">only ever booking the first table</p></div>'
 '<div class="card"><h3>2 · I keep discounting people who would have paid anyway</h3><p class="dim">the $9, handed to someone already buying</p></div>'
 ,'n':'These are not feelings. They are the two tables you just built. When a merchant sounds scared, they are scared of one of these two things.'},

{'k':'drill','h':'<h2>Now you</h2><ul><li>Pairs. A real brand. Teardown sheet <b>§0–1</b></li>'
 '<li>50 minutes, then every pair reports</li></ul>'
 '<p class="punch" style="margin-top:1em">At that margin, <em>how many orders</em> before they are ahead?</p>'
 ,'n':'Homework: sections 0-1 on two more brands. Classify each bought-once or bought-again, then predict the stack BEFORE you look. Then look, and score yourself.'},
]

# ─────────────────────────────── SESSION 2 ───────────────────────────────
S2=[
{'h':'<h1>How the order<br>happens</h1><p class="dim" style="margin-top:1em">Session 2 · stops 1–9 · phones out</p>'
 ,'n':'Goal: you can walk any shop as a customer and name where people quit.'},

{'h':'<h2>Today we follow one person</h2><div class="card"><h3>Mai</h3>'
 '<p><b>Lumi</b> — one moisturizer, <b class="acc">$42</b>, refill every <b class="acc">8 weeks</b>.<br>'
 'Lumi paid about <b class="acc">$30</b> in ads to reach her.</p></div>'
 '<p style="margin-top:1em">Last week we did the money. Today we watch it happen to a human being.</p>'
 ,'n':'Keep asking through the session: what is Mai doing right now? Never let it become abstract.'},

{'h':'<p class="punch">Every stop is a place where <em>money leaks out.</em></p>'
 '<p style="margin-top:1.2em">Every leak has a name, a number, and a fix.</p>'
 '<p class="punch" style="margin-top:1em">You cannot find the opportunity if you cannot <em>see the journey.</em></p>'
 ,'n':'No merchant will ever write in saying "I have a leak at stop six." They say "conversion is down." Your job is to know which stop they are standing on.'},

{'h':'<h2>The thing that makes all of this possible</h2><table>'
 '<tr><th></th><th>A shop</th><th>Online</th></tr>'
 '<tr><td class="dim">Someone walks in</td><td>you see a body</td><td>you know they came from that ad</td></tr>'
 '<tr><td class="dim">They browse</td><td>no record</td><td>you know they viewed it 3×</td></tr>'
 '<tr><td class="dim">They leave</td><td class="neg"><b>gone forever</b></td><td class="pos">they are on a list</td></tr>'
 '<tr><td class="dim">You learn who they are</td><td>only at the till</td><td><b>at the popup</b></td></tr></table>'
 ,'n':'This is the difference between a shop and a website, and nearly every app in ecom exists because of it.'},

{'h':'<p class="punch">In a shop, someone who leaves is <em>gone.</em></p>'
 '<p class="punch" style="margin-top:.8em">Online, someone who leaves is <em>a list.</em></p>'
 ,'n':'That is why the popup exists. Why retargeting exists. Why abandoned cart email is the most profitable email in ecom. And it is why loyalty works at all — a loyalty program is just identity, applied over time.'},

{'k':'look','h':'<h2>Stops 1–2 · The ad, and where she lands</h2>'
 '<p>Open the Ad Library. Find a live ad for tonight\'s brand. Then click through.</p>'
 '<div class="res">facebook.com/ads/library</div>'
 '<p style="margin-top:1em">Does the page repeat the promise the ad just made?</p>'
 ,'n':'An ad is not a picture of a product. It is an argument aimed at one person: name her problem, prove it, make it urgent. And the most common way to waste thirty dollars in this business is the ad promising one thing and the page saying another. She assumes she misread it and leaves.'},

{'k':'look','h':'<h2>Stop 3 · The popup</h2><p class="punch">"10% off your first order"</p>'
 '<p style="margin-top:1em">What is actually being bought here?</p>'
 '<p style="margin-top:.6em">Not the sale. <b class="acc">The email.</b> Lumi cannot email a stranger.</p>'
 '<p class="dim" style="margin-top:1em">And the 10% is real: −$6.80. Some who take it would have paid full price.</p>'
 ,'n':'That is owner fear number two, live, in the first thirty seconds. Trigger the popup on the projector so they see it fire.'},

{'h':'<h2>Stop 4 · The product page</h2>'
 '<p class="punch">Will this work for me?<br>Can I trust you?<br>What if I hate it?</p>'
 '<p style="margin-top:1.2em">Reviews answer all three, cheaper than any copy you could write.</p>'
 ,'n':'A hidden returns policy kills the sale. A stranger will not risk forty-two dollars on a shop that will not say what happens if it fails.'},

{'h':'<h2>Stop 5 · Subscribe or bundle — not the same thing</h2><table>'
 '<tr><th></th><th>Buys the owner</th><th>Costs</th></tr>'
 '<tr><td><b>Subscription</b></td><td class="acc"><b>LTV</b> — next order agreed</td><td>15% margin, forever</td></tr>'
 '<tr><td><b>Bundle</b></td><td class="acc"><b>AOV</b> — fatter order today</td><td>less per unit, more cash now</td></tr></table>'
 ,'n':'Subscription raises lifetime value. Bundle raises order value. Different problems. A shop with a repeat problem needs the first. A shop with thin orders needs the second. Do not let anyone say them in the same breath.'},

{'k':'look','h':'<h2>Stop 6 · The strongest lever in ecom</h2>'
 '<p class="punch">"You are <em>$12 away</em> from free shipping."</p>'
 '<p style="margin-top:1.2em">She would rather add $12 of product than pay $7 of shipping for nothing.</p>'
 ,'n':'Free shipping thresholds move average order value more than almost anything else. And the threshold has to sit above the point where the maths works, or the merchant is just paying postage. Add to cart live so they see the bar move.'},

{'h':'<h2>Stop 7 · She leaves</h2><p>Puts the phone down. Dinner. She was never angry.</p>'
 '<p class="punch" style="margin:1em 0"><em>70%</em> of carts are abandoned.</p>'
 '<p>Three exits, three emails: <span class="dim">browse · cart · checkout</span></p>'
 '<p class="punch" style="margin-top:1em">No email captured → no recovery → the <em>$30 is gone.</em></p>'
 ,'n':'This is the whole reason stop three existed. Point back at it. Global cart abandonment is about 70 percent per Baymard — this is normal, not a failure.'},

{'h':'<h2>Stop 8 · Where intent goes to die</h2>'
 '<ul><li><b class="acc">Extra costs are the #1 abandon reason</b> — 39% of people</li>'
 '<li>The discount code box is a <b>leak</b> — they leave to hunt for a code</li>'
 '<li>Express wallets: five fields become one thumbprint</li>'
 '<li>Guest checkout — do not force an account on a stranger</li></ul>'
 '<div class="res">baymard.com/lists/cart-abandonment-rate</div>'
 ,'n':'A seven dollar shipping fee on a forty-two dollar order reads as a seventeen percent price rise. That is why it is the number one reason. Not the price of the product — the surprise.'},

{'h':'<h2>Stop 9 · The best real estate in the shop</h2>'
 '<p class="mono dim">"Order confirmed."</p><p class="punch">→ "Add the night cream, $18. <em>One click.</em>"</p>'
 '<p style="margin-top:1.2em">She already trusts them. Her card is already charged.</p>'
 ,'n':'A post-purchase offer cannot lose the sale, because the sale is done. This is also where loyalty enrolment belongs, and where most shops waste it.'},

{'h':'<h2>Every leak has a name</h2><table>'
 '<tr><th>The number</th><th>Stop</th><th>Low means</th></tr>'
 '<tr><td>Site speed</td><td class="dim">2</td><td>she left before it loaded</td></tr>'
 '<tr><td>Email capture</td><td class="dim">3</td><td>you do not know who is visiting</td></tr>'
 '<tr><td><b>Add-to-cart rate</b></td><td class="dim">4</td><td>the page did not convince her</td></tr>'
 '<tr><td><b>AOV</b></td><td class="dim">5–6</td><td>orders are too thin</td></tr>'
 '<tr><td><b>Checkout rate</b></td><td class="dim">8</td><td>shipping shock, friction</td></tr></table>'
 ,'n':'These numbers are not abstract. Each one is a stop on the path you just walked.'},

{'h':'<p class="punch">"Conversion is down" is <em>not a problem.</em></p>'
 '<p style="margin-top:1em">It is a symptom of a leak at one specific stop.</p>'
 '<p class="punch" style="margin-top:1.2em">An AM finds the stop.<br><span class="dim">CS forwards the sentence.</span></p>'
 ,'n':'That sentence is the difference between the two jobs. That is all it is.'},

{'k':'drill','h':'<h2>Now you</h2><ul><li>Pairs, <b>phones out</b>, real brand, real money in the cart</li>'
 '<li>Walk stops 1–9. Teardown <b>§2–3</b></li>'
 '<li>Every stop: what you saw · what they wanted · <b>what would make you quit</b></li></ul>'
 '<p class="punch" style="margin-top:1em">The main door — and the <em>one place you would quit.</em></p>'
 ,'n':'Homework: sections 2-3 on two more brands. Walk your own store and mark where you would quit. Three tickets from your queue — which STOP is each one really about?'},
]

# ─────────────────────────────── SESSION 3 ───────────────────────────────
S3=[
{'h':'<h1>After the order,<br>and the second one</h1><p class="dim" style="margin-top:1em">Session 3 · stops 10–14 · where the money is</p>'
 ,'n':'Goal: you can say why someone would buy twice, and what the shop is doing about it.'},

{'h':'<h2 class="dim">Last week ended the moment she paid.</h2>'
 '<p class="punch">Every business thinks that is the finish line.</p>'
 '<p class="punch" style="margin-top:.6em">It is <em>the start.</em></p>'
 ,'n':'Stops one to nine are greyed out now. Everything from here is where the money actually is.'},

{'h':'<h2>Stop 10 · The wait</h2>'
 '<p class="mono dim" style="font-size:clamp(16px,2.4vw,32px)">paid —————— ? —————— arrived</p>'
 '<p style="margin-top:1.2em">Nothing happens here. That is the problem.</p>'
 '<p style="margin-top:.8em">This gap is where every <b class="acc">"where is my order"</b> ticket is born.</p>'
 ,'n':'Usually the single biggest ticket category in ecom. You already know this one — you live in it. A late parcel someone warned you about is fine. A late parcel nobody mentioned is a refund and a one-star review.'},

{'h':'<h2>Stop 11 · The emails after</h2><table>'
 '<tr><th>When</th><th>Email</th><th>Job</th></tr>'
 '<tr><td class="dim">Immediately</td><td>confirmation</td><td>reassurance</td></tr>'
 '<tr><td class="dim">Ships</td><td>tracking</td><td>kill the WISMO ticket</td></tr>'
 '<tr><td class="dim">Delivered</td><td>how to use it</td><td><b>make sure she uses it</b></td></tr>'
 '<tr><td class="dim">~Week 2</td><td>review request</td><td>proof for the next stranger</td></tr>'
 '<tr class="tot"><td class="acc">~Week 6</td><td class="acc">"running low?"</td><td class="acc">the money email</td></tr></table>'
 ,'n':'The review comes when she has actually used it, not when it arrived. A review on day one is a review of the packaging.'},

{'h':'<h2>Week six is the one that pays</h2>'
 '<p>Refill window is 8 weeks. You arrive at <b class="acc">week 6</b> — before she runs out, before she thinks about alternatives.</p>'
 '<p class="punch" style="margin-top:1.2em">This email is worth more than <em>the ad from stop 1.</em></p>'
 ,'n':'Say it again in your head. One automated email, sent to someone who already likes them, beats thirty dollars of advertising.'},

{'k':'look','h':'<h2>Stop 12 · She is everywhere now</h2>'
 '<ul><li><b>Retargeting</b> — they have her email, so they can find her cheaply</li>'
 '<li><b>Creators / TikTok</b> — an army of small posts, sometimes its own checkout</li>'
 '<li><b>Amazon</b> — discovered on TikTok, bought on Amazon out of habit</li></ul>'
 ,'n':'Retargeting is far cheaper than stop one, because they are no longer paying to find a stranger. They are paying to remind a customer. Open a brand on two channels side by side if you have time.'},

{'h':'<h2 class="dim">Which is why attribution is a swamp</h2>'
 '<p class="mono" style="font-size:clamp(15px,2vw,28px)">saw the ad → got the email → watched a creator → <b class="acc">bought on Amazon</b></p>'
 '<p class="punch" style="margin-top:1.2em">Four arrows. <em>One sale.</em> Who gets the credit?</p>'
 ,'n':'You do not have to solve this. You just have to stop being surprised when a merchant says their numbers do not match. They never match.'},

{'h':'<h2>Stop 13 · Referral is a different machine</h2>'
 '<div class="two"><div class="card"><h3 class="acc">Referral</h3><p><b>grows</b> the base</p></div>'
 '<div class="card"><h3 class="acc">Loyalty</h3><p><b>monetises</b> the base</p></div></div>'
 '<p style="margin-top:1.2em">A referred person arrives with trust already loaded. And you pay only when it works —<br>unlike an ad, which you pay <b>on hope</b>.</p>'
 ,'n':'Remember this difference. Next week it decides what you recommend to a real merchant.'},

{'h':'<h2>Stop 14 · Week eight</h2>'
 '<p>She is nearly out. The refill email arrives.</p>'
 '<p class="punch" style="margin-top:1em">She opens her account. <em>420 points — worth $4.20.</em></p>'
 '<p style="margin-top:1em">She reorders.</p>'
 ,'n':'This is the only thing that ever made this business work.'},

{'h':'<p class="dim" style="font-size:clamp(20px,3vw,40px)">Look where we are.</p>'
 '<p class="punch" style="margin-top:.6em">Stop <em>14 of 14.</em></p>'
 '<p style="margin-top:1.4em">Loyalty is not the engine of a shop. It is the <b>last mile of a long system</b>, and it only pays if the thirteen stops before it exist.</p>'
 ,'n':'That is why we have not opened Joy once in three sessions.'},

{'h':'<h2>The money — order 1</h2><table>'
 '<tr><td>Ad to reach Mai</td><td class="n neg">−$30.00</td></tr>'
 '<tr><td>Cart: moisturizer + travel size</td><td class="n">+$68.00</td></tr>'
 '<tr><td>Popup 10%</td><td class="n neg">−$6.80</td></tr>'
 '<tr><td>Free shipping, Lumi pays it</td><td class="n neg">−$7.00</td></tr>'
 '<tr><td>Processing</td><td class="n neg">−$2.07</td></tr>'
 '<tr><td>Products</td><td class="n neg">−$20.00</td></tr>'
 '<tr class="tot"><td>Lumi keeps</td><td class="n acc">+$2.13</td></tr></table>'
 ,'n':'Mai spent sixty-one dollars twenty. The shop kept two dollars thirteen. Stop talking for a second.'},

{'h':'<h2>Order 2 — eight weeks later</h2><table>'
 '<tr><td><b>Ad spend</b></td><td class="n pos">$0.00</td></tr>'
 '<tr><td>Refill</td><td class="n">+$42.00</td></tr>'
 '<tr><td>Points redeemed</td><td class="n neg">−$4.20</td></tr>'
 '<tr><td>Shipping</td><td class="n neg">−$7.00</td></tr>'
 '<tr><td>Processing</td><td class="n neg">−$1.52</td></tr>'
 '<tr><td>Product</td><td class="n neg">−$12.00</td></tr>'
 '<tr class="tot"><td>Lumi keeps</td><td class="n pos">+$17.28</td></tr></table>'
 ,'n':'One order with no ad attached is worth eight of the first one. Same shop, same product, same customer.'},

{'h':'<h2 class="dim">So what did the points actually do?</h2>'
 '<p class="punch">They did not make Mai <em>like</em> Lumi.</p>'
 '<p style="margin-top:1.2em">They gave her a reason to choose Lumi <b>instead of the alternative</b>, in that moment — and a nudge to do it <b>now</b> rather than in three weeks.</p>'
 '<p class="punch" style="margin-top:1.2em">Loyalty does not buy affection.<br>It buys <em>timing and preference.</em></p>'
 ,'n':'If you remember one sentence about our product, make it that one.'},

{'h':'<h2>Three things, not one thing</h2><table>'
 '<tr><th>Subscription</th><th>Loyalty</th><th>Discount</th></tr>'
 '<tr><td>the next box is already agreed</td><td>a reason to choose <b>you</b> next time</td><td>this order is cheaper</td></tr></table>'
 '<p style="margin-top:1.4em">Merchants mix these up constantly.</p>'
 '<p class="punch" style="margin-top:.6em">If you mix them up too, <em>you cannot help them.</em></p>'
 ,'n':'This distinction comes back in session four as the easiest sale we have — Recharge plus Klaviyo plus no loyalty.'},

{'k':'ask','h':'<p class="punch">Why would a human buy <em>this</em> twice?</p>'
 '<p style="margin-top:1.4em">Sometimes there is no reason. A mattress. A set of pans.</p>'
 '<p style="margin-top:1em">That is not a failure of the shop. It is a fact about the product —<br>and it tells you everything about what that merchant actually needs.</p>'
 ,'n':'We come back to this next week. It is the whole of session four.'},

{'k':'drill','h':'<h2>Now you</h2><ul><li>Pairs. <b>Two</b> brands, chosen deliberately</li>'
 '<li>One with a strong repeat reason — refill, consumable</li><li>One with a weak one — bought once</li>'
 '<li>Teardown <b>§4–5</b></li></ul>'
 '<p class="punch" style="margin-top:1em">Why would a human buy this twice — and <em>what is the brand doing about it?</em></p>'
 ,'n':'Homework: sections 4-5 on two brands. What is the real reason someone reorders from YOUR store? Five tickets restated in two sentences each, own words, Vietnamese fine, no questions to the merchant.'},
]

# ─────────────────────────────── SESSION 4 ───────────────────────────────
S4=[
{'h':'<h1>The stack,<br>and is it ours</h1><p class="dim" style="margin-top:1em">Session 4 · the AM read · still no Joy admin</p>'
 ,'n':'Goal: you can read a shop\'s stack and say whether it is ours and whether it even needs us.'},

{'k':'ask','h':'<p class="punch">Is Recharge a <em>subscription app?</em></p>'
 ,'n':'Let them say yes. Then say no. It is a solution for increasing lifetime value. Klaviyo is not an email app — it is a cheap way to talk to everyone at scale, far cheaper than SMS, plus a CRM that remembers birthdays and order history.'},

{'h':'<p class="punch">We do not sell an app.</p><p class="punch" style="margin-top:.6em">We sell <em>the solution the app is made of.</em></p>'
 ,'n':'Which means every app on a merchant\'s site is a clue about what they are afraid of.'},

{'h':'<h2>The stack is a confession</h2>'
 '<p>Every app a merchant installed is money they spent because <b class="acc">they were worried about something.</b></p>'
 '<p class="dim" style="margin-top:1.2em">Nobody installs a bundle app for fun. They installed it at 11pm after looking at a number that scared them.</p>'
 ,'n':'This is the AM read. It is the single most useful thing in this whole course.'},

{'h':'<h2>Read it out</h2><table>'
 '<tr><th>They installed</th><th>So they believe their problem is</th></tr>'
 '<tr><td>Klaviyo / Attentive</td><td>"I cannot reach my visitors again"</td></tr>'
 '<tr><td>A popup tool</td><td>"too many people leave anonymous"</td></tr>'
 '<tr><td>Okendo / Judge.me</td><td>"strangers do not trust me yet"</td></tr>'
 '<tr><td><b>Rebuy / bundle</b></td><td>"my orders are too thin" — <b>AOV</b></td></tr>'
 '<tr><td><b>Recharge / Skio</b></td><td>"customers buy once" — <b>LTV</b></td></tr>'
 '<tr><td>Gorgias / Wonderment</td><td>"I am drowning in <i>where is my order</i>"</td></tr>'
 '<tr><td><b class="acc">A loyalty app</b></td><td>"I have a base and nothing brings them back"</td></tr>'
 '<tr><td class="dim">Nothing at all</td><td class="dim">very early — or nobody is minding the shop</td></tr></table>'
 ,'n':'The stack tells you what the owner is afraid of before they say a word.'},

{'k':'look','h':'<h2>How to check — no login, 60 seconds</h2>'
 '<p class="mono dim">right-click → View Page Source → Ctrl-F</p>'
 '<div class="res mono">klaviyo · attentive · recharge · appstle · skio · smile<br>'
 'yotpo · loyaltylion · rivo · growave · okendo · judge.me<br>gorgias · rebuy · subscribe</div>'
 '<p style="margin-top:1em">Then: the footer · <span class="mono">/account</span> · try <span class="mono acc">/pages/rewards</span></p>'
 ,'n':'Do this live on the projector. It is genuinely fun to watch. If /pages/rewards 404s, they have no loyalty — and that is a sixty second job that tells you more than a discovery call.'},

{'h':'<h2 class="dim">Now the sharp question</h2>'
 '<p>They installed a bundle app. But their real leak is that <b>nobody comes back.</b></p>'
 '<p class="punch" style="margin:1.2em 0">They are fixing <em>stop 6</em> while bleeding at <em>stop 11.</em></p>'
 '<p class="punch">Do you <em>tell them?</em></p>'
 ,'n':'Yes. That is the service. That is the entire difference between answering the app and owning the outcome. And it costs something — you are telling a paying merchant that the thing they bought is not their problem.'},

{'h':'<h2>Is it ours? Run the checklist</h2><table>'
 '<tr><td>Shopify or Plus</td><td class="n dim">□</td></tr>'
 '<tr><td>Category that repurchases <span class="dim">— beauty, apparel, wellness, kids, outdoor, pet, home</span></td><td class="n dim">□</td></tr>'
 '<tr><td>Roughly $5–40M</td><td class="n dim">□</td></tr>'
 '<tr><td><b>Klaviyo or Attentive</b> installed</td><td class="n dim">□</td></tr>'
 '<tr><td>Growing — raise, press, retail, viral</td><td class="n dim">□</td></tr>'
 '<tr><td><b>No</b> Rivo / Yotpo / Smile / LoyaltyLion / Growave</td><td class="n dim">□</td></tr></table>'
 '<p class="acc" style="margin-top:1em">Every line is visible from the public website. You never ask them.</p>'
 ,'n':'This is Joy\'s real ICP, not something I made up for class.'},

{'h':'<h2>The easiest win to recognise</h2>'
 '<p class="punch">Recharge or Appstle <em>+</em> Klaviyo <em>+</em> no loyalty app</p>'
 '<p style="margin-top:1.4em">They already pay for repeat revenue. They have nothing that gives a reason to return.</p>'
 '<p class="punch" style="margin-top:1em">Subscription is <em>not</em> loyalty.</p>'
 ,'n':'The next box being agreed is not the same as the customer choosing you. It means they have not yet cancelled. Those are different things, and the gap is exactly what we sell.'},

{'k':'look','h':'<h2>The textbook case</h2><p class="punch">raewellness.co</p>'
 '<ul><li>Recharge, heavily used</li><li>Klaviyo</li><li>Wellness — natural repurchase</li>'
 '<li><b class="acc">/pages/rewards → 404</b></li></ul>'
 ,'n':'Do it live. Thirty seconds. View source, Ctrl-F recharge, Ctrl-F klaviyo — both hit. Ctrl-F smile, loyaltylion, yotpo — nothing. Then type slash pages slash rewards. That 404 is the whole pitch, and they found it themselves without asking the merchant anything.'},

{'k':'ask','h':'<p class="punch">Does this shop need a loyalty program <em>at all?</em></p>'
 ,'n':'This is the question that separates you from a salesperson. Let it hang.'},

{'h':'<h2>A loyalty program is a multiplier</h2><table>'
 '<tr><th></th><th>Shop A</th><th>Shop B</th></tr>'
 '<tr><td class="dim">Customers</td><td>100</td><td>20,000</td></tr>'
 '<tr><td class="dim">Loyal share</td><td class="acc"><b>100%</b></td><td class="acc"><b>5%</b></td></tr>'
 '<tr><td class="dim">Extra orders</td><td>~100</td><td>~3,000–4,000</td></tr>'
 '<tr class="tot"><td>Verdict</td><td class="neg">still dead</td><td class="pos">real money</td></tr></table>'
 '<p class="punch" style="margin-top:1.2em">Multiply a small number — <em>it is still small.</em></p>'
 ,'n':'Shop A has a perfect loyalty program and is going out of business. A loyalty program is a multiplier on a base you already have. It is not a growth engine.'},

{'h':'<h2>So the first question is stage</h2><table>'
 '<tr><th>Their stage</th><th>What they actually need</th></tr>'
 '<tr><td>Ads to survive, no real base</td><td><b class="acc">expand the base</b> — referral. Not points.</td></tr>'
 '<tr><td>Base exists, people buy once</td><td>a <b>reason to return</b> — points, tiers</td></tr>'
 '<tr><td>Base exists, discounting everyone</td><td><b>stop the blanket discount</b> — VIP tiers</td></tr></table>'
 '<p style="margin-top:1.2em">Remember referral from last week — it <b>grows</b> the base where loyalty <b>monetises</b> it.</p>'
 ,'n':'The shop that must NOT be sold points is often exactly the shop that should run referral. So "not ready" is never a dead end. It is a different recommendation.'},

{'h':'<p class="punch">"Not yet" is a <em>correct answer.</em></p>'
 '<p style="margin-top:1.4em">Telling a survival-stage shop to launch points is not service. It is selling them the wrong thing. It will not produce a result.</p>'
 '<p class="punch" style="margin-top:1em">And they will churn — <em>correctly.</em></p>'
 ,'n':'If you cannot say "not yet" out loud, you are selling, not advising. And you lose the account anyway, six months later, with worse feelings.'},

{'h':'<h2>What you can do now — no app</h2><ul>'
 '<li>What does this shop sell, and how does it make money on one order?</li>'
 '<li>How do people arrive, and where do they quit?</li>'
 '<li>Why would someone buy twice — and what is the brand doing about it?</li>'
 '<li>Is it ours, does it need this, and what is the one thing we would change?</li></ul>'
 '<p class="punch" style="margin-top:1.2em">Four weeks ago none of you could answer these.<br><span class="dim">You have not opened Joy once.</span></p>'
 ,'n':'Let that land. This is the moment the course pays off.'},

{'h':'<h2>The gate</h2>'
 '<div class="card" style="margin-bottom:.8em"><h3>1 · A cold teardown</h3><p class="dim">a brand you have never seen, 15 minutes, a lead accepts it</p></div>'
 '<div class="card" style="margin-bottom:.8em"><h3>2 · 8 of 12 restatements</h3><p class="dim">timed, from your own queue</p></div>'
 '<div class="card"><h3>3 · Your store, launched, to standard</h3><p class="dim">max three apps, every one defensible</p></div>'
 '<p class="punch" style="margin-top:1.2em">Then: <em>Joy.</em></p>'
 ,'n':'"Not yet" is a normal outcome here too. It means another stack of reps — not another lecture.'},
]

# ─────────────────────────────── BUILD ───────────────────────────────
if __name__=='__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print('Building decks:')
    build('session-1-money.html','Session 1 — Money on one unit','Session 1 · Money on one unit',S1)
    build('session-2-first-order.html','Session 2 — How the order happens','Session 2 · How the order happens',S2)
    build('session-3-second-order.html','Session 3 — After the order','Session 3 · After the order, and the second one',S3)
    build('session-4-stack.html','Session 4 — The stack, and is it ours','Session 4 · The stack, and is it ours',S4)
    print('Done. Open any .html in a browser. ← → to move, S for speaker notes, Cmd-P to PDF.')
