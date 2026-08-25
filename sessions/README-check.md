# Checking the decks for clipped text

Cards use `overflow:hidden`, so content taller than its grid rows would silently lose text.
`autofit()` in each deck shrinks an overflowing card (down to 0.6×) instead of clipping it.

**If a card is still clipped at 0.6× it needs more grid rows, not more shrinking.**

To sweep all three decks, serve the folder and run this in the browser console:

```bash
cd sessions && python3 -m http.server 8899
```

```js
for (const d of ['session-1-basics.html','session-2-retention.html','session-3-together.html']) {
  const html = await fetch('/'+d).then(r=>r.text());
  const f = Object.assign(document.createElement('iframe'),
            {style:'position:fixed;left:-9999px;width:1600px;height:900px'});
  document.body.appendChild(f); f.srcdoc = html;
  await new Promise(r => f.onload = r);
  try { await f.contentWindow.document.fonts.ready } catch(e){}
  await new Promise(r => setTimeout(r, 900));
  const bad = [];
  [...f.contentDocument.querySelectorAll('.slide')].forEach((s,i) => {
    s.classList.add('active');
    s.querySelectorAll('.card').forEach(c => {
      const o = c.scrollHeight - c.clientHeight;
      if (o > 4) bad.push(`s${i+1} +${o}px zoom=${c.style.zoom||1}`);
    });
    s.classList.remove('active');
  });
  console.log(d, bad.length ? bad : 'CLEAN');
  f.remove();
}
```

Run it after any content edit. `build.py` also validates section counts and catches swallowed
markup (unclosed attributes) on every build — that guard exists because a stray edit once
collapsed every slide in session 1 on top of each other.
