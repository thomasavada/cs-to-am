# Session 2 — What is wrong with this shop?

**Goal:** given a shop you have never seen, find what is **actually** wrong with it — and say which problem to fix first.
**Deck:** `session-2-troubleshoot.html` · 24 slides · **Resources:** [`resources.md`](resources.md)
**Material:** [`shop vs online`](../material/journey/2-shop-vs-online.md) · [`stops 1–9`](../material/journey/3-stops-1-9.md) · [`problem decoder`](../material/journey/10-merchant-problem-decoder.md) · [`stack is a confession`](../material/journey/7-stack-confession.md) · [`full stack map`](../material/journey/9-stack-map.md) · [`what an app really solves`](../material/money/8-what-an-app-really-solves.md)

## Prep
- [ ] **Walk Halfdays yourself the night before** — know where its popup fires
- [ ] Brand site open, cart empty, **not logged in** · phone mirrored if possible
- [ ] **Practise the view-source demo once** — know the keystrokes cold
- [ ] Everyone brings a charged phone

## Run of show — 2 hours
| Time | Beat | Format |
|---|---|---|
| 0:00 | Checkpoint + homework on the table | round the room |
| 0:10 | **Every merchant message is a symptom, never a cause** | slides |
| 0:14 | Outside-in · a shop vs online · *someone who leaves is a list* | slides |
| 0:16 | **The funnel — 100 land, 3 pay** | slides |
| 0:20 | **The problem decoder** — what they say → what it means → where | slides |
| 0:24 | Deep dive · **low AOV** — packs, pairs, upsells, the $1-above threshold, the $35 floor | slides |
| 0:28 | Deep dive · **low ROAS with good clicks and CVR** — double AOV, double ROAS | slides |
| 0:31 | Deep dive · **low CVR with high AOV — normal, don't escalate** | slides |
| 0:34 | Deep dive · **flat sales with great ROAS** — the returning-rate trap | slides |
| 0:38 | Deep dive · **low returning rate** — three product types, three answers | slides |
| 0:42 | Deep dive · **low CVR** — the product-page fixes, *move everything upward* | slides |
| 0:46 | Deep dive · **8% ATC, 1% CVR** — the checkout killers, incl. our own widget | slides |
| 0:52 | "Conversion is down" is a symptom | slides |
| 0:37 | **View source, live** → the stack is a confession | ◉ live |
| 0:42 | The real board — 28 fields, one of them ours · the yotpo trap | slides |
| 0:47 | **Alia** and **Order Editing** — what an app really solves | slides |
| 0:53 | **Which problem do you fix first?** — ranking by people-lost and cost-to-fix | slides |
| 0:58 | **Brand beat** — what is this owner paying to fix? | ◉ live |
| 1:05 | **Rep: diagnose a brand, then rank the problems** | ▲ 45 min |
| 1:50 | Report out — three problems, ranked, with the cost of each | — |

## Every decoder row has a deep dive
The table is the index. Each row then gets its own slide with the actual diagnosis and fixes — the way
Chase works through them. Full reference and sources:
[`material/journey/10-merchant-problem-decoder.md`](../material/journey/10-merchant-problem-decoder.md).

The one to not skip is **"low CVR with high AOV is normal"** — it is the counterweight. A merchant
panicking about 0.4% conversion on a $1,700 machine needs reassurance, not a fix, and an AM who cannot
tell the difference sends people chasing ghosts.

## Running the 45 minutes

The deck timeboxes it on screen. **Write the times on the board too.**

| | |
|---|---|
| **3 min** | Get your brand — handed out. Phone, cart empty, not logged in. |
| **12 min** | Walk it as a customer. Where would *you* quit? |
| **10 min** | Read the stack — view source, then `/pages/rewards` |
| **12 min** | **List every problem. All of them. Do not rank yet.** |
| **5 min** | Rank your top three, with what each costs to fix |

**Separating "list everything" from "rank" is the whole design.** Rank as you go and they stop at the
first thing they recognise — usually the thing we sell.

### What you do while they work
Circulate. When a pair says "the site looks bad", make them say **which step and how many people**.
Vague is the enemy here, not wrong.

Watch for the pair whose top three includes loyalty at number one. Ask them what it would cost to fix,
and what the *free* fixes are. Usually that reorders it for them without you saying anything.

### Report out
Three problems, ranked, with the cost of each. **If loyalty is not in their top three, that is a correct
answer** — say so out loud so nobody thinks they got it wrong.

## The most senior beat in the session
**Which one do you fix first?** Anyone can list problems. Ranking them — by *how many people it loses*
and *what it costs to fix* — is judgement. And the honest order puts **us last**: a merchant with a
broken checkout button does not need a loyalty program, and if we sell them one it will not work.

> Recommending someone else's fix first is how you earn the conversation about ours.

## The two beats that carry it
**The view-source demo.** Sixty seconds and they know more than a discovery call would tell them.

**The loyalty-widget slide.** A loyalty widget covering the checkout button is a named conversion killer
— that is *our app*. Read the quote slowly, then land it. It turns an annoying ticket ("can you move the
widget?") into a real signal, and makes them the person who catches it.

**Live, not screenshots.** Walk the real site. Screenshots in `resources.md` are the wifi fallback.
**Stop before paying** — nobody buys anything on the projector.

## Homework
1. A full teardown on two more brands — **three ranked problems each**
2. Walk your own store on your phone and diagnose it. Be honest.
3. Three tickets — which step of the path is each really about?
