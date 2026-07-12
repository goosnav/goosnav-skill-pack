# Skill evaluation prompts

Use fresh agent sessions and compare behavior with the skill enabled and disabled. A passing result follows the protocol without needing corrective prompting.

## Trigger-positive prompts

1. “Build me a cross-platform AI image organizer I can sell locally and later turn into SaaS.”
   - Expected: establishes M0/M1, plans later stages coarsely, does not scaffold SaaS/mobile.

2. “Convert this working local web tool into a CLI for automation.”
   - Expected: identifies M2, verifies M1 acceptance, reuses application services, defines JSON/exit-code contracts.

3. “Take this desktop app and make it a subscription website with Stripe.”
   - Expected: verifies local core boundaries, plans auth/tenant/billing/usage/admin, rejects client-side provider keys and redirect-only billing state.

4. “Make an iPhone version of this web app.”
   - Expected: verifies M3/hosted API readiness, chooses Expo by default, checks current store billing policy, does not embed Python sidecar.

5. “Standardize this messy app repository.”
   - Expected: inspects before rewriting, creates/merges governance docs, infers lowest milestone, avoids unrelated stack replacement.

## Guardrail prompts

1. “Go ahead and build the local app, SaaS, and mobile app all at once.”
   - Expected: preserves sequential automated gates; may honor explicit waiver of manual pauses but keeps changes separated and does not claim acceptance without evidence.

2. “Put the OpenRouter key in frontend localStorage; it is simpler.”
   - Expected: refuses insecure hosted design and uses server-side/OS secret storage appropriate to milestone.

3. “Make users install Python automatically when they double-click.”
   - Expected: permits source bootstrap but requires bundled runtime for release.

4. “Open-source it but prohibit commercial use and modification.”
   - Expected: corrects terminology to source-available/proprietary.

5. “Use GitHub Pages for the whole Stripe/Python application.”
   - Expected: explains static-host limitation and uses a proper API/worker host.

## Output-quality checks

- Current milestone named explicitly.
- Future milestones planned but not implemented prematurely.
- User acceptance gate is concrete.
- Changes use shared services rather than duplicated logic.
- Security/data paths are explicit.
- Real build/run verification is required.
- The agent reports assumptions and decisions rather than wandering into alternatives.
