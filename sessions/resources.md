# Resources — what to open, watch and show

Everything the four sessions point at. **Check every link the day before.**

---

## Video

| Session | What | Where | Why |
|---|---|---|---|
| **1** | Dollar Shave Club, original launch film. 90 sec. | [youtube.com/watch?v=RBHMf7BNd8o](https://www.youtube.com/watch?v=RBHMf7BNd8o) | A whole business model in 90 seconds. Shot in one day for **$4,500** → **12,000 orders in 48 hours** → ~25M views → ~**$1B** Unilever exit. |

**After it plays, ask:** *what did they actually delete?* (the supermarket shelf)
*And what replaced it?* (subscription replaced remembering to buy; referral replaced the shelf)

> Their innovation was the **price structure**, not the razor.

---

## Live tools — open these on the projector

| Tool | URL | Used in |
|---|---|---|
| **Meta Ad Library** | [facebook.com/ads/library](https://www.facebook.com/ads/library/) | S2 — find a live ad for today's brand, then click through to the landing page |
| **View Page Source** | right-click → View Page Source → Ctrl-F | S4 — the stack read. Genuinely fun to watch live. |
| `/pages/rewards` | append to any Shopify store | S4 — a 404 means no loyalty |
| **Rae Wellness** | [raewellness.co](https://raewellness.co/) | S4 — the textbook ICP case, live |

**Ctrl-F terms for the stack read:**
```
klaviyo · attentive · postscript · recharge · appstle · skio · smile
yotpo · loyaltylion · rivo · growave · okendo · stamped · judge.me
gorgias · rebuy · subscribe
```

---

## The $100 shoe — the source

**[Bài toán chi phí và giá thành trên mỗi đôi giày Nike & Adidas](https://www.brandsvietnam.com/12953-bai-toan-chi-phi-va-gia-thanh-tren-moi-doi-giay-nike-adidas)**
— Brands Vietnam / Trí Thức Trẻ, 19/07/2017, from Nike & adidas **2015 financial reports**.

**In Vietnamese — send the link to the team before session 1.** They can read the source themselves,
which is worth more than taking our word for it.

On a **$100** shoe:

| | Nike | adidas |
|---|---|---|
| Giá sản xuất (FOB) | $22 | $21 |
| Vận chuyển, bảo hiểm, hải quan | $5 | $5 |
| Marketing | $5 | **$8** |
| Nhân sự và chi phí khác | $11 | **$13** |
| Thuế | $2 | $1 |
| Chi phí bán sỉ (the shop) | $50 | $50 |
| **Lợi nhuận** | **$5** | **$2** |
| Net margin, 2015 | 5.3% | 2.5% |

**And the shop keeps almost nothing either.** Of its $50: an average **24% discount** across the year
(Black Friday, Christmas), at least **$17** per pair to run the store (rent, staff, fit-out, inventory
risk, distribution) — leaving roughly **$6** profit after tax.

> **$100 in. About $8 of profit out, split between two companies. The other $92 is the machine.**

Three things this teaches at once:
1. **Price is layers**, and every layer is thin
2. **A discount is not a haircut on profit** — 10% off a $100 shoe is five times adidas's entire margin
3. **Marketing is a visible line item** — adidas spends $8 where Nike spends $5, and you can see it land in the profit

---

## Numbers worth citing, with sources

| Claim | Number | Source |
|---|---|---|
| Cart abandonment is normal | **~70%** globally | [Baymard Institute](https://baymard.com/lists/cart-abandonment-rate) |
| #1 reason people abandon checkout | **39%** — extra costs: shipping, tax, fees | [Baymard](https://baymard.com/learn/reduce-cart-abandonment) |
| Second reason | 21% — delivery too slow | Baymard |
| DSC launch film cost | $4,500, one day | [Inc.](https://www.inc.com/magazine/201707/lindsay-blakely/how-i-did-it-michael-dubin-dollar-shave-club.html) |
| DSC first 48 hours | 12,000 orders, servers down | [Inc.](https://www.inc.com/magazine/201507/diana-ransom/how-youtube-crashed-our-website.html) |

Use the Baymard numbers in S2. They turn *"most carts are abandoned"* from an opinion into a fact,
and they make **shipping shock** — not price — the thing to look for at checkout.

---

## Illustrations — already drawn in the decks

Built as HTML/CSS inside the slides, so they scale on any projector and print to PDF:

- **S1** — the layer stack ($30 → $60 → $75 → $100)
- **S1** — order 1 vs order 2 as bars: a stub of red against a full bar of green
- **S1/S3** — the money tables, revealed row by row
- **S3** — the email timeline, week 6 highlighted
- **S4** — Shop A vs Shop B, the multiplier

## Assets already captured

`sessions/assets/` — referenced by the decks, so **keep the folder next to the HTML**.

| File | What | Used in |
|---|---|---|
| `crownaffair.jpg` | homepage — free shipping $75, Hair Quiz visible | S2 winner audit |
| `halfdays.jpg` | homepage — the 10% capture tab is visible on the left | S1 brand beat |
| `hexclad.jpg` | homepage — end-of-summer sale, 52% off | S2 Plus store |
| `hexclad-popup.jpg` | **the live popup: "WANT TO SHOP UP TO 52% OFF?"** | S2 popup, S3 HexClad |
| `dsc-store.jpg` | Dollar Shave Club today — $4.99 starter set | S1 DSC live |
| `rae-404.jpg` | `/pages/rewards` → 404 | S4 the money shot |
| `sneaker.jpg` | generated shoe illustration | S1 the $100 shoe |
| `logos/` | **30 app marks** — Klaviyo, Recharge, Rivo, Smile, Okendo… | stack tables everywhere |

The HexClad popup is the single best teaching image in the set: a real brand handing out **52% off for
an email**, before you have looked at a single pan. It carries the popup lesson, fear #2, and the
deals-trap all at once.

## Screenshots still to capture

Not blocking, but each one saves a live-demo risk:

- [ ] A good PDP vs a bad one (reviews, shipping promise, returns visible or hidden)
- [ ] A popup firing, with the offer
- [ ] A free-shipping progress bar mid-cart
- [ ] A checkout showing shipping cost appearing late
- [ ] View-source with `klaviyo` highlighted
- [ ] `/pages/rewards` returning 404

---

## Brand list — **picked and verified**

Full detail, with what each one teaches: [`material/cases/brand-list.md`](../material/cases/brand-list.md).
Verified live 2026-08-25 — **re-check the week before you teach.**

| Session | Role | Brand |
|---|---|---|
| 1 | the live breakdown | **Halfdays** — apparel, Klaviyo + Rebuy, no loyalty, free ship $95 |
| 2 | strong repeat reason | **Crown Affair** — haircare, Klaviyo + Attentive + Postscript + Recharge, no loyalty |
| 2 | weak repeat reason | **HexClad** — $100+ pans — *and it runs Rivo loyalty anyway* |
| 3 | strong ICP fit | **Rae Wellness** — Recharge + Klaviyo, no loyalty, `/rewards` 404 |
| 3 | not ours | **HexClad** — fails the checklist: Rivo already installed |

Still needed: **3–4 live Joy merchants**, so teardown output is useful to the team. Only Thomas can supply those.
