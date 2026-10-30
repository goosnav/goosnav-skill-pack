# Crawling and indexing

Source baseline: 2026-10-30. Reopen the relevant official references when applying the guidance. These checks establish technical behavior, not a guarantee that Google will index or rank a URL.

## Rendering: diagnose before switching to SSR

Compare initial response HTML, rendered DOM and Google's inspected version where accessible. Check meaningful content, status, links, metadata and canonical before and after hydration. Identify blocked resources, JavaScript errors, interaction-only content and app-shell responses. Use [Google's JavaScript SEO guide](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics).

Keep already complete static HTML. For deficient public routes, choose a supported static generation, prerendering or SSR approach in the current stack, with a reason and operating-cost implications. Do not convert the whole authenticated application merely to fix marketing pages. Avoid crawler-only content or architecture changes without an observed need. Verify content parity, direct/deep route loads, HTTP errors, hydration, navigation and metadata after the change. Initial `noindex` can prevent rendering; JavaScript removal may not rescue it.

## Robots and indexing directives

Check effective `robots.txt` for the correct scheme/host and user-agent group, route patterns, essential CSS/JS, sitemap declaration and deployed/CDN overrides. Fix unintended public blocks without indiscriminately allowing staging or crawl traps. See the [robots introduction](https://developers.google.com/search/docs/crawling-indexing/robots/intro).

Inspect HTML `robots`/`googlebot` meta directives and HTTP `X-Robots-Tag`, including response-header rules for non-HTML resources. Remove only accidental exclusions from intended public pages, preferably in the template/configuration emitting them. Keep deliberate exclusions, authentication and authorization. `robots.txt` controls crawling, not confidentiality or guaranteed deindexing; a blocked crawler cannot read a page's `noindex`. `noindex` is not a supported robots.txt directive. See [Google's noindex documentation](https://developers.google.com/search/docs/crawling-indexing/block-indexing).

Do not resolve the crawl/noindex interaction by exposing private content. For publicly reachable excluded pages, choose controls deliberately; for confidential content, retain access control. Check production and nonproduction configurations separately.

## Canonicals and redirects

Define the preferred origin and URL policy from deployment/business facts, including HTTPS, host, slash, case and meaningful parameters. Give distinct public pages appropriate absolute canonicals, usually self-referencing; consolidate genuine equivalents. Do not canonicalize the whole site to its homepage, drop meaningful locale/filter variants blindly, use fragments as canonical identities, or trust a user-controlled Host header as the configured public origin. Align HTML/HTTP canonical signals, redirects, internal links and sitemap. Check canonical targets resolve to appropriate indexable content. Canonicals are signals, not guaranteed Google selections. Use [Google's canonicalization guidance](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls).

Trace redirect hops, status, destination, query handling and loops through the actual server/CDN rules. Collapse avoidable chains to the final relevant destination; update internal references. Preserve intentional temporary redirects, authentication, locale routing and valid legacy migrations. Use the appropriate permanent/temporary status; avoid blanket redirects from missing URLs to the homepage and changes that break form/API method semantics. Return genuine 404/410 or meaningful errors for absent pages rather than soft-404 success. See [Google's redirect guidance](https://developers.google.com/search/docs/crawling-indexing/301-redirects).

## Sitemap and discovery

Use the existing CMS/framework generator when correct; avoid a second stale hand-maintained sitemap. Generate from the actual intended public inventory, not just reachable navigation, so useful orphans are considered. Include absolute preferred URLs that should be indexed and return successful content. Exclude private/unlisted/staging, redirects, errors, duplicates and `noindex` URLs. Use accurate `lastmod` only when a meaningful modification date is known; do not refresh every URL's date on every build. Parse XML, check escaping/namespace, final statuses and inventory coverage. Follow current [sitemap format and size limits](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap); split into an index when needed. A sitemap is a discovery hint, not a replacement for navigation.

Publish at the correct origin and declare the absolute location in robots.txt where useful. For authorized Search Console submission, verify the property and deployed sitemap, submit via the actual connected interface, and record acceptance/errors. Otherwise provide the verified URL and the [Sitemaps report](https://support.google.com/webmasters/answer/7451001) owner step. A local XML file or a robots declaration is not proof of submission. Do not use retired sitemap-ping endpoints or treat the [restricted Indexing API](https://developers.google.com/search/apis/indexing-api/v3/using-api) as a general website-submission API. For selective recrawl, follow the [official request-indexing guidance](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl); success does not guarantee indexing.

## Broken links and orphans

Resolve relative URLs against each page's base; check href targets, anchors, images and important resources, rendered links, redirects and destinations. Use a bounded GET when HEAD is unsupported or misleading. Retest suspected external failures: 403, 429, TLS problems and transient timeouts may be access/rate issues rather than a dead page. Do not mass-delete links on those observations. Fix confirmed internal 404s/invalid anchors and redirect sources; choose a relevant replacement, or remove a genuinely obsolete reference without inventing a page.

Build a public internal-link graph and reconcile source/CMS routes with navigation, sitemap, logs and Search Console evidence when supplied. Link useful indexable orphan pages contextually from relevant hubs with descriptive text; omit deliberate private, obsolete or unlisted routes. Prefer real `<a href>` links and useful hierarchy. See [Google's crawlable-link guidance](https://developers.google.com/search/docs/crawling-indexing/links-crawlable). For international or large faceted sites, investigate the existing locale/pagination/parameter strategy before changing canonicals or crawl scope; escalate that scope explicitly rather than applying a blanket rule.
