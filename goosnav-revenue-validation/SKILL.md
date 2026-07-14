---
name: goosnav-revenue-validation
description: Convert useful software into a specific productized offer and run a truthful validation loop with a proof artifact, qualified target list, personalized outreach drafts, explicit owner approval before sends, send/reply tracking, predefined positive-signal criteria, and evidence-based iteration. Use when a founder wants to test willingness to engage or pay without inventing traction.
version: 1.0.0
author: Goosnav LLC
license: Proprietary; internal use permitted
metadata:
  hermes:
    tags:
      - revenue-validation
      - productized-offer
      - outreach
      - founder-operations
      - evidence
    related_skills:
      - goosnav-mvp-delivery
      - goosnav-local-first-workbench
      - goosnav-software-productization
---

# Overview

Validation is a measured attempt to reduce commercial uncertainty, not a performance of momentum. Turn the working capability into one bounded offer for one reachable buyer, create proof that the capability exists, define what response would count before outreach, and keep an auditable ledger of actual sends and replies.

Separate four evidence levels:

```text
product proof -> buyer exposure -> response -> commitment/payment
```

Do not collapse them. A working demo is not demand. A drafted email is not outreach. A polite reply is not willingness to pay. A verbal “interesting” is not a paid pilot. Report the strongest level actually observed and preserve the denominator.

External actions require owner gates. Drafting, research from authorized sources, segmentation, and ledger preparation are reversible. Sending messages, publishing a page, spending on ads, changing prices for live customers, signing terms, or using personal data in new ways requires explicit authority.

## When to Use

Use when a founder has useful software or a credible working slice and needs to decide whom it is for, package a service/pilot/license, prepare outreach, track market responses, or choose the next product change from evidence. It works for founder-led sales, small paid pilots, design partnerships, digital downloads, and service-assisted software offers.

Do not use it to fabricate testimonials, customer counts, revenue, waitlists, case studies, or conversations. Do not automate bulk outreach or scrape prohibited/personal data. If the software cannot yet demonstrate its promised outcome, return to MVP Delivery and create a proof artifact first.

## Workflow

1. **State the commercial hypothesis.** Write one falsifiable sentence: “[Specific buyer] will [pay/commit time/provide data] for [bounded outcome] because [costly current problem], observed through [signal] within [time/volume window].” Record the highest-risk assumption and what evidence would change the decision.

2. **Verify product truth.** Run the product’s canonical verifier and complete the promised workflow. Record what is live, fixture-backed, manual, or unavailable. Never offer an automated outcome that currently requires hidden founder labor without disclosing the service component.

3. **Create a proof artifact.** Prefer a short artifact the buyer can judge: before/after sample, annotated output, replayable demo project, two-minute walkthrough script/video plan, benchmark with methodology, or sanitized report. Use fictional/synthetic inputs unless real-data use is authorized. Label fixtures and limitations directly in the artifact.

4. **Design one productized offer.** Specify target, trigger, included inputs, delivered output, turnaround, interaction model, exclusions, price or pilot terms, capacity, data handling, and call to action. Constrain custom work. State whether the buyer receives software, a service-assisted result, access, or a license. Avoid tier grids before one offer is understood.

5. **Choose signal thresholds in advance.** Define `positive`, `neutral`, and `negative` events before seeing replies. Strong signals include payment, signed pilot, scheduled evaluation with the right buyer, authorized sample data, or explicit procurement next step. Weak signals include opens, likes, compliments, generic curiosity, and replies from non-buyers. Set denominator and review date.

6. **Build a qualified target list.** Use only lawful, authorized sources and collect the minimum business contact data. For each target record organization, person/role, public source, problem evidence, qualification reason, personalization note, channel, status, and next permitted action. Prefer 10 well-matched targets over 1,000 generic addresses. Do not infer sensitive traits.

7. **Draft a narrow message sequence.** Lead with an observed problem and concrete proof, not broad product claims. Ask one low-friction question or offer one bounded next step. Personalization must be factually sourced. Prepare initial message and at most two respectful follow-ups with stop conditions. Do not use fake forwarding, fake scarcity, or deceptive subject lines.

8. **Run the owner send gate.** Present the exact recipient list, channel, final text/template, personalization fields, send schedule, data source, tracking method, and stop rule. Ask for explicit approval. Approval for a draft is not approval to send; approval for five named recipients is not approval for a larger batch. Never send through an available connector by inference.

9. **Send only the approved scope.** If authorized, send the exact approved messages and immediately record timestamp, channel, recipient, message/version, and external message identifier when available. On any mismatch, rate limit, bounce pattern, consent concern, or tool ambiguity, stop. Do not silently substitute recipients or copy.

10. **Track replies as observed events.** Preserve the reply’s meaning without exaggeration. Classify using the predetermined rubric, note objections/questions, and link to source. Distinguish no response, bounce, auto-response, opt-out, referral, curiosity, qualified conversation, requested trial, and commercial commitment. Respect opt-outs immediately.

11. **Review the denominator and quality.** Report sent, delivered if known, replies, qualified replies, positive signals, commitments, and payments. Small samples use counts plus context, not misleading percentages. Analyze by target qualification and message hypothesis, not vanity metrics.

12. **Update one variable at a time.** Choose target, problem framing, proof, offer, price/terms, or call to action. Do not simultaneously rewrite all dimensions because learning becomes uninterpretable. Record why the next batch differs and what result would support the change.

13. **Apply owner gates to the next step.** Meetings, custom work, data receipt, contract terms, discounts, refunds, paid ads, publication, and production access may create obligations. Present the decision and obtain authority before acting. Keep irreversible commitments outside autonomous iteration.

14. **Close the loop honestly.** End with `VALIDATED`, `PROMISING`, `INCONCLUSIVE`, or `NOT SUPPORTED` for the defined hypothesis and window. Cite proof, exposure, response, and commitment separately. Recommend continue, modify, or stop. Never backfill invented traction to make the project appear successful.

## Evidence Ledger

Use a local CSV, JSON, or spreadsheet with stable IDs and these logical records:

- `hypothesis`: version, buyer, problem, offer, threshold, window;
- `target`: source URL/reference, qualification fact, role, minimal contact data, consent/usage notes;
- `message`: version, exact body/template, proof artifact, approved scope;
- `send`: target ID, actual timestamp, channel, external ID, delivery state;
- `reply`: source, timestamp, observed content summary, rubric class, next step;
- `commitment`: type, owner, due date, financial/contract status;
- `decision`: counts, evidence level, interpretation, next variable.

Keep drafts separate from sends so the ledger cannot imply exposure. Store sensitive contact data outside public repositories. Redact it from screenshots, fixtures, and support artifacts. Retain only what the operating/legal context requires.

## Positive-Signal Rubric

Define product-specific criteria, but use this strength order:

1. payment received or binding purchase/pilot agreement;
2. explicit budget/process and dated procurement or pilot step;
3. qualified buyer provides authorized input/data and schedules evaluation;
4. qualified buyer schedules a discovery/evaluation conversation tied to the problem;
5. specific reply confirming the problem and asking a substantive question;
6. referral to the actual owner, generic interest, compliment, open, click, or social engagement.

Only levels selected in advance count as positive for the experiment. Lower levels may guide copy or targeting but do not prove revenue demand.

## Pitfalls

- **Proof-demand confusion:** treating a polished demo or test pass as buyer evidence.
- **Draft-send confusion:** counting prepared messages as contacted prospects.
- **Vanity promotion:** reporting opens, likes, or generic praise as purchase intent.
- **Denominator hiding:** citing two positive replies without saying 200 messages were sent.
- **Synthetic testimonial:** turning fixture output or an internal quote into a customer story.
- **Target drift:** messaging anyone reachable after the intended buyer does not respond.
- **Multi-variable thrash:** changing buyer, offer, price, and proof together.
- **Authority creep:** using a signed-in mailbox or browser session as permission to send.
- **Data sprawl:** committing personal contact lists or reply content to source control.
- **Overpromising automation:** hiding manual service work or unverified integrations.

## Verification Checklist

- [ ] The hypothesis names buyer, costly problem, bounded offer, signal, and window.
- [ ] The promised product workflow was actually run; fixture/manual/live parts are explicit.
- [ ] A reviewable proof artifact exists and contains no invented customer evidence.
- [ ] Offer scope, output, turnaround, exclusions, price/terms, and CTA are concrete.
- [ ] Positive-signal criteria and denominator were set before replies.
- [ ] Every target has a lawful source and a factual qualification reason.
- [ ] Messages contain sourced personalization and no deceptive claims.
- [ ] Explicit owner approval covers recipients, copy, channel, schedule, and scope before send.
- [ ] Drafts, sends, delivery states, replies, commitments, and payments remain distinct.
- [ ] Opt-outs and data-minimization rules are respected.
- [ ] Results report counts and evidence levels without inflated interpretation.
- [ ] The next iteration changes one named variable and has a new decision rule.

## Exact Recipe

Recipe: validate a local report-quality workbench as a paid pilot.

1. Hypothesis: “Boutique research agencies will pay for a five-report pilot that catches citation and consistency problems before client delivery; a positive signal is a qualified agency owner sharing one authorized sample report and scheduling a priced pilot review within 21 days.”
2. Run the workbench verifier. Create a synthetic report with deliberate issues, export the before/after findings bundle, and label it “synthetic demonstration.” Record that analysis is automated but founder review is included in the pilot.
3. Define offer: five reports, up to a stated page limit, local/private processing, findings bundle within two business days, one review call, fixed pilot price, no legal/factual guarantee, and deletion schedule.
4. Build 15 targets from public agency websites. Record role, source, an observed quality-sensitive service, and one factual personalization note. Store contact details in a private operations ledger, not the product repository.
5. Draft an initial email that links/attaches the synthetic proof and asks whether pre-delivery QA is a current bottleneck. Prepare one value follow-up and one close-the-loop follow-up.
6. Present all 15 recipients, the exact template and personalization, schedule, tracking columns, and a stop rule of any opt-out concern or three delivery failures. Wait for explicit owner approval before any send.
7. After approved sends, record actual message IDs and timestamps. Classify replies against the preset criterion; a compliment without sample/report step is neutral, not positive.
8. At day 21, report exposure, replies, qualified conversations, authorized samples, priced pilots, and payments. Mark the hypothesis `PROMISING` only if the preset qualified step occurred; otherwise `INCONCLUSIVE` or `NOT SUPPORTED`. Change only the selected next variable—such as agency specialization—before another gated batch.
