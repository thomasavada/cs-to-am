# The full stack map — every app is a confession, filed by funnel step

**Used in:** Session 1, the stack read.
**Source:** `~/avada-know-the-drill` (`data/graph.json`, 627 nodes / 130 fielded apps · `data/detection-patterns.json`).

The short table in the deck lists seven apps. The real board is **~28 fields**. This is the reference —
so when a merchant names something nobody has heard of, you can still place it on the path.

---

## GET PEOPLE IN

| Field | Who plays | What the owner is afraid of |
|---|---|---|
| **Creator / affiliate** | GOAFFPRO · Refersion · Superfiliate | "I need other people to bring me people" |
| **Attribution** | Northbeam · Triple Whale | "Ad platforms double-count. I do not know what actually works" |
| **Server-side events (CAPI)** | Elevar | "Ad blockers and consent broke my tracking, so my ads optimise on bad data" |
| **Post-purchase survey** | Fairing | "Attribution misses word of mouth — so I ask the customer directly" |

## ON THE SITE

| Field | Who plays | What the owner is afraid of |
|---|---|---|
| **Capture** | Alia · Privy · Dotdigital | "Too many people leave anonymous" |
| **Quiz** | Octane AI | "She cannot ask a shop assistant which one is for her" |
| **Reviews** | Okendo · Judge.me · Fera · **Yotpo Reviews** | "Strangers do not trust me yet" |
| **On-site video** | Tolstoy · VideoWise | "I have great video and it is not selling anything" |
| **Search** | Algolia · Nosto · Shopify Search & Discovery | "They cannot find the thing they came for" |
| **Landing pages** | PageFly · Replo · Weaverse | "My theme cannot do what the campaign needs" |

## PAY

| Field | Who plays | What the owner is afraid of |
|---|---|---|
| **Subscriptions** | Recharge · Skio · Appstle | "They buy once and vanish" — **LTV** |
| **Bundles / upsell** | Rebuy | "My orders are too thin" — **AOV** |
| **Discount logic** | Discount Kit | "My promotions are too complicated for native rules" |
| **Price / offer testing** | Intelligems | "I do not actually know what to charge" |
| **Buy now, pay later** | Klarna · Afterpay | "The basket is too big to pay in one go" |
| **Checkout** | Checkout Blocks · Checkout Buddy · Shop Pay | "Checkout is where I lose people" |
| **Tax · Cross-border** | Avalara · Global-e | "Selling abroad is a compliance minefield" |

## AFTER THE ORDER

| Field | Who plays | What the owner is afraid of |
|---|---|---|
| **Tracking** | AfterShip | "**WISMO tickets** are eating my team" |
| **Order editing** | Order Editing | "A wrong address becomes a mis-shipment and a refund" |
| **Returns** | Loop · Happy Returns · Redo · ReturnGO | "Returns cost me money, stock and goodwill" |
| **Support** | Gorgias | "My team is drowning and answering the same question all day" |

## COME BACK — *our field*

| Field | Who plays | What the owner is afraid of |
|---|---|---|
| **Lifecycle / email** | Klaviyo · Drip · Bloomreach | "I have no way to reach them again" |
| **SMS** | Attentive · Postscript | "Email is not enough for the urgent moments" |
| **Mobile app** | Tapcart · Fuego · MageNative | "I want a channel nobody can take away from me" |
| **Loyalty** | **Joy** · Smile.io · Rivo · LoyaltyLion · Yotpo Loyalty · BON | "I have a base and nothing brings them back" |

---

## Three things this map teaches that the short table cannot

**1. Joy plays one field out of twenty-eight.**
Not a criticism — a scale check. A merchant's day is spent on twenty-seven other worries. If we walk in
talking only about points, we are talking about ~4% of their board. **The AM read is the whole board.**

**2. The loyalty field is crowded and the features are identical.**
Six named competitors, all shipping points, tiers and referrals. That is the argument from session 1
made concrete: **the app cannot be the reason they choose us.**

**3. A name is a signal, not a verdict.**
`yotpo` in page source could be Yotpo **Reviews** (on-site trust) or Yotpo **Loyalty** (a competitor).
Different field, opposite conclusion. Rae Wellness runs Yotpo Reviews and has **no** loyalty.
Confirm which before you tell anyone a brand "already has loyalty."

---

## Detecting properly

`avada-know-the-drill/data/detection-patterns.json` holds confirm-strings and known false positives.
Two worth knowing, because both would embarrass you on a call:

| App | Decisive marker | Known false positive |
|---|---|---|
| **Rivo** | `window.Rivo.global_config`, `loyalty.rivo.io` | dead theme CSS (`--rivo-aw-`, `.RivoMultiplier`) — four false hits observed |
| **Alia** | `backend.alia-prod.com`, `window.ALIA_SHOPIFY_EXTENSION_INFO` | `window.SHOW_ALIA = false` — installed but **switched off** |

> An app in the source is not always an app in use. A disabled flag is not a live install.

---

## One line worth stealing

Alia's own positioning, on why a blanket popup is a bad trade:

> Blanket discount popups **buy signups that never convert** and **train shoppers to wait for 15% off.**

That is owner fear #2 and the deals-trap from session 2, written by a company that sells against it.
Use it — it is more persuasive coming from the market than from us.
