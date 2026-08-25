# What an app really solves — two worked examples

**Used in:** Session 1, the stack read.
**Source:** `~/avada-know-the-drill/training.md` (Thomas's talk to Avada tech leads) + `data/graph.json`.

The talk to the tech leads and this course are the **same argument aimed at two teams**. Engineers were
told: AI does execution, so stop competing on features and move to service. CS is being told the same
thing about tickets. Worth saying out loud in the room — this is not a CS-only re-training.

---

## Why two examples beat a list

CS can already recite app names. What they cannot do is say **what problem an app was built to kill**.
So take two apps and go all the way down. One is a popup. One fixes an address. Both look trivial and
neither is.

---

## 1 · Alia — a popup, taken to 10/10

**Field:** capture. **The one job:** email/SMS capture for DTC.

Everyone ships a popup. Alia's whole company rests on noticing what a *normal* popup actually does:

> Blanket discount popups **buy signups that never convert** and **train shoppers to wait for 15% off.**

Read that against session 1. That is **owner fear #2** — discounting people who would have paid — and
the deals-trap from session 2, where a predictable sale teaches people the real price is lower.
Alia did not build a better popup. They noticed the popup was **causing** the merchant's problem.

**So they changed the mechanism:** the coupon is **earned**, not given. She does something — answers,
engages, plays — and the discount becomes a reward instead of a toll the shop pays on every visitor.

And then they went *deep* rather than wide: Prism AI, Smart Triggering, Smart Testing, twelve researched
popup formats. One job, taken to nine or ten out of ten.

**What CS should take from it**
- An app is not a feature. It is **a position on what the merchant's real problem is.**
- The interesting question is never *what does this app do* — it is **what does this app believe?**
- Alia believes a blanket discount is a leak. Rivo believes retention is a proof problem.
  Joy has to be able to say what it believes too.

---

## 2 · Order Editing — an app that exists because of one ticket

**Field:** order_edit. **The one job, verbatim:** *let the shopper or merchant fix an unfulfilled order.*

> A wrong address, size, variant, or forgotten item becomes a support ticket — and can turn into a
> **mis-shipment** if the warehouse acts before anyone fixes it.

This is the example to use with **our** team, because they have lived it. Every person in the room has
worked that ticket. Somebody built a company around it.

**Walk the room through the chain:**

| Step | What happens |
|---|---|
| She mistypes her address | thirty seconds of her time |
| She emails support | a ticket in your queue |
| The warehouse ships first | a parcel in the wrong place |
| Refund or reship | the whole order's margin is gone |
| She tells someone | and a review |

**The lesson:** a ticket is never just a ticket. It has a **cost downstream**, and that cost is why an
app exists. When you can see that chain, you stop seeing tickets as work to clear and start seeing them
as **evidence about the business** — which is the entire difference between the two jobs.

---

## 3 · The "why" chain — steal this test

From the training talk, as a way of checking whether anyone has actually understood a product:

> Build a subscription app. **What for?** — "to increase LTV."
> Fine. **Why does LTV need increasing?** Is that a real question, or a slogan everyone repeats?
>
> Same for AOV. **How much is low? How much is enough? Enough for what?**

If the chain cannot be answered with concrete business reasoning, the problem is not understood — no
matter how much research sits on paper.

**Use it as the report-out standard.** When a pair says *"they should raise AOV"*, ask:

1. Raise it to what number?
2. Why that number?
3. What does the merchant get at that number that they do not get today?

Three questions, and you find out immediately whether they read the business or repeated a word.

---

## 4 · What merchants actually buy

The training talk names this as a gap at Avada, and it is the sharpest argument for the whole course.

**Rivo** — a loyalty competitor — publishes 19 case studies. Each card carries **one hero number**
("$450K in 90 days", "3.2× repeat rate") and **no feature list at all**. Features are only explained
*after* the number has already persuaded you. Above them sits a category-level proof banner:
**55× ROI · 3.1× repeat purchase rate · +4% revenue lift · 9,000+ brands.**

And the painful half: internal research found Avada products with results just as good — *1700% ROI,
450% ROI, $110K in 14 days* — with **no public case study presenting them that way**. The vault calls
it **"a packaging gap, not a results gap."**

> **Merchants do not buy features. They buy a number, proven by somebody like them.**

Which is why a CS person who can say *what result this merchant should expect, and by when* is worth
more than one who can configure the app faster.

**And the story to tell in the room** — real, and it happened:

> Asked "what apps does Avada have?", the answer given was *"we have twenty apps."*
> The other side stopped wanting to talk. Not because twenty is too few — because the answer read as
> **"these people do not know what problem they solve."**
>
> The right answer starts at the problem: *we help merchants [do X, measured by Y]* — never a catalogue.

That is exactly what we are training out of CS. *"Where do I click"* is the catalogue answer.
*"Here is the result you should expect"* is the other one.
