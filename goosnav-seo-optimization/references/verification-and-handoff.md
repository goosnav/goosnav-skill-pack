# Verification and handoff

Scale the report to the site and evidence. A small site normally needs a short diagnosis, compact findings table, a repairs/tests paragraph and a few owner tasks. Use shared-template findings and route samples instead of repeating boilerplate for every URL. Keep the report in chat unless a saved artifact was requested or belongs in existing project documentation.

## Evidence contract

For each material finding record: intended route class, file/line or URL, observed versus supplied evidence, problem/priority, actual change or recommendation, verification command/action/result, and remaining boundary. Example states:

- `FIXED AND VERIFIED — local HTTP`: generated public HTML no longer emits accidental `noindex`; private test still returns the expected protected response. Production/Google not inspected.
- `CHANGED, UNVERIFIED`: corrected a template and parsed the build output; no browser or deployment access.
- `ALREADY SATISFIED / NOT APPLICABLE`: static HTML already contains the public content, so SSR migration is unnecessary.
- `OWNER ACTION / UNKNOWN`: sitemap prepared but Search Console property/submission unavailable; field INP lacks data; author identity not supplied.

For a claim about served or rendered behavior, source checks alone mean `CHANGED, UNVERIFIED`; describe successful static checks separately. A corrected source directive does not verify the server's headers or Google's response.

Disclose reliance on an evidence bundle rather than independent access. A factual absence can support a provisional no-change decision, but a provider assertion is not a verified submission or Google result. Distinguish a crawl error, indexing exclusion and low-ranking indexed page; don't present one as proof of another.

## Relevant checks

| Boundary | Useful verification | Does not establish |
| --- | --- | --- |
| Rendering | Generated and served HTML, headers/status, browser content/links and interactions; Google inspection if available | Deployed correctness from a source match alone |
| Indexing policy | Public/private/staging route tests, robots group/path behavior, meta plus header directives, CDN/WAF response | That “allow all” is safe or robots enforces privacy |
| URL integrity | Canonical target content/status, redirect hops, normalized internal links, sitemap inventory | That Google selected the declared canonical |
| Discovery | Bounded link/anchor checks and source/CMS route graph, exclusion policy | That sitemap membership makes a page internally linked |
| Metadata/schema | Built output, distinct truthful text, JSON parsing, visible-content match, current feature validation | That syntactically valid schema yields rich results |
| Images/performance | Reopened assets, visual alternatives/context, browser behavior and comparable metrics; field scope/window | That one lab score covers every route or real users |
| External outcomes | Search Console submission/inspection result, actual published link and verified attribution | That a prepared task, draft or local test is an external success |

Use the project's build/test conventions and focused regressions for changed behavior. Rerun affected checks after the final edits. Test representative repaired public pages and deliberately excluded pages. A production-only issue may require a deployment follow-up even when local evidence passes. Do not run an unbounded crawler, trigger state-changing links, use real user data as fixtures, or add test dependencies solely for a trivial text change.

## Search Console and owner tasks

Use a relevant connected capability if available. Otherwise inspect the authorized UI or provide a concrete handoff. Do not ask the owner to disclose passwords or verification secrets. Confirm the property, protocol/host coverage, permission and actual deployed sitemap URL. Follow the [Sitemaps report](https://support.google.com/webmasters/answer/7451001) and [URL Inspection help](https://support.google.com/webmasters/answer/9012289).

For each missing external step, name the owner/action and required proof:

- Correct-property sitemap submission: deployed sitemap URL, submission timestamp/result and subsequent parse/fetch errors. Acceptance is distinct from page indexing.
- Priority repaired URL inspection: crawl access, live/rendered evidence, indexing state and Google's selected canonical. Request indexing only when appropriate and authorized; record what was actually requested.
- A production configuration fix: changed CDN/server/CMS setting and verified public response; no claim that a repository patch altered the live service.
- Authorship: owner-supplied person/organization identity, approved bio and actual contribution. Draft placeholders are development notes, not published author facts.
- Authority work: useful asset and relevant outreach target/draft when requested; independently earned links remain pending until real publication is observed.
- Measurement: metric/route/device scope and baseline, what to recheck after deployment or sufficient field data, and success criteria. Recommend a follow-up; create scheduled work only on request.

Google's [recrawl guidance](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl) explains that requests take time and do not guarantee inclusion. Define completion as the authorized repairs and honest evidence handoff, not an unverified page-one promise. Do not invent an SEO score, zero-error claim, ranking gain, completion percentage or deadline.
