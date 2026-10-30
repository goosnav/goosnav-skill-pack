# Images and performance

Source baseline: 2026-10-30. Optimize measured user experience, not a format checklist or a single synthetic score.

## Text alternatives and image meaning

Inspect the actual image and its role on the page. Supply short alternatives conveying the information, or the action/destination for an image used as a control. Preserve `alt=""` for purely decorative or redundant images; it is different from a missing attribute. Complex charts need equivalent information in surrounding content. Avoid filename guesses, generic “image of,” and keywords unrelated to meaning. CSS decoration does not require a fabricated description. Follow the [W3C image decision tree](https://www.w3.org/WAI/tutorials/images/decision-tree/).

Use descriptive contextual placement, crawlable image URLs and responsive `<img>`/`picture` output as appropriate. Ensure important visual content is not available only as an inaccessible background or blocked/ephemeral URL. Follow [Google's image guidance](https://developers.google.com/search/docs/appearance/google-images); descriptions do not compensate for an invisible or failed image.

## Formats, delivery and layout

Measure source dimensions, displayed size, transfer size, quality, animation/transparency requirements and browser/CMS support. Produce responsive raster sizes and compare WebP, AVIF or existing formats for actual benefit. Preserve appropriate SVG vectors rather than rasterizing small logos/icons blindly. Retain originals/recovery paths where needed, credits/licenses and accurate image meaning; do not use image-generation tools to replace documentary product screenshots. Update `srcset`, `sizes`, image URLs, preload references, caching and content types together. Verify generated files open and render before replacing references.

Reserve image/media/embed space with correct dimensions or aspect ratios. Lazy-load below-the-fold media where useful, but keep the likely LCP/hero image promptly discoverable; do not lazy-load it by default. Avoid indiscriminate preloads or high fetch priority on every asset. Check visual fidelity, responsive cropping, retina sizes, transparency and fallbacks. Detailed timing diagnosis: [Optimize LCP](https://web.dev/articles/optimize-lcp). Layout diagnosis: [Optimize CLS](https://web.dev/articles/optimize-cls).

## Metrics and honest budgets

The [Web Vitals guidance](https://web.dev/articles/vitals) lists good thresholds of LCP **at most 2.5 seconds**, INP **at most 200 milliseconds**, and CLS **at most 0.1**, assessed at the **75th percentile**, segmented by mobile and desktop. Verify current metrics at audit time. Do not substitute a load event, TTFB, Lighthouse score, TBT or a first-paint value for those metrics. Lighthouse TBT can help diagnose responsiveness but does not establish field INP.

Use Search Console/CrUX or authorized real-user measurements where available, and state URL versus origin scope, reporting window, device and sample availability. “Insufficient data” is unknown, not a pass. A single lab run does not establish sitewide real-user success, and field history will not update immediately after a deployment. Google's [Core Web Vitals report](https://support.google.com/webmasters/answer/9205520) explains the grouped real-user reporting.

Treat “every page loads in under two seconds” as a requested engineering budget that needs a named metric, test device, network, cache state and route coverage. Do not claim Google has a universal two-second requirement. Define the budget from the task, retain the conventional CWV thresholds separately, and report the actual observed distribution/coverage. If the requested budget is not met or cannot be measured, say so.

## Measurement and repairs

Capture representative landing, content, media-heavy and interactive routes plus any known slow routes. Save reproducible before/after measurements under comparable conditions; repeated controlled runs help avoid treating noise as improvement. Pair lab diagnostics with field evidence, retaining both scopes. Do not install a new monitoring platform or telemetry collector merely to close an audit without considering consent, data and authorization.

Investigate the bottleneck before changing architecture: response time/caching, content discovery and resource priority, render-blocking CSS/fonts, oversized assets, excessive JavaScript, long tasks, third-party work, font swaps, late inserted UI and missing reserved space. Choose targeted changes. Keep consent controls, ads/placeholders and meaningful UI behavior functional; do not hide content or remove necessary controls to manufacture a score. Exercise interactions, scrolling, navigation and late loading when checking CLS, rather than testing only the initial viewport.

Run available project checks and actual browser measurements after repairs; state what unavailable tooling leaves unverified. Reopen converted assets and inspect the page at relevant sizes. Report local improvements only at that boundary. A successful build, smaller file or fast local host is not proof of production CWV or ranking improvement.
