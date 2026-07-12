# Mobile architecture

## Default decision

Use Expo/React Native for a product expected to remain in the stores, use native capabilities, support polished navigation, or evolve independently. Use a Capacitor/web wrapper only when the application is fundamentally a responsive website and the wrapper still provides enough mobile value to satisfy users and current store review policy.

Do not put the desktop Python sidecar inside the mobile application by default. Mobile should call the hosted API. Device-local compute can be added as a deliberately designed native module when justified.

## Shareable assets

Share:

- OpenAPI schema and generated API models/client;
- validation schemas where language/runtime permits;
- design tokens (color, typography, spacing, radii);
- product terminology and analytics event names;
- test fixtures;
- entitlement semantics.

Do not force-share:

- DOM components;
- desktop filesystem assumptions;
- browser storage/session code;
- desktop keyboard/mouse interactions;
- server secrets or provider SDKs.

## Mobile requirements

- secure token storage and rotation;
- PKCE/deep-link handling for OAuth/passwordless auth;
- clear network/offline/retry states;
- idempotency for costly operations and uploads;
- cancellation and resume where practical;
- background/foreground lifecycle handling;
- push notifications only when they provide clear value;
- accessible labels, dynamic text, contrast, touch targets, and reduced-motion behavior;
- privacy disclosures and permission minimization;
- crash reporting with sensitive-data redaction;
- account deletion and subscription-management links/flows;
- current Apple/Google billing-policy review.

## Store billing

Do not assume Stripe Checkout can be used inside a mobile app for digital subscriptions. Before implementation, inspect current Apple App Store and Google Play policies for:

- required in-app purchase mechanisms;
- external purchase links and regional exceptions;
- reader-app or enterprise exceptions;
- account deletion;
- subscription restoration and management;
- pricing and trial disclosures.

Record the policy URLs, review date, selected approach, and residual risk in `dev/DECISIONS.txt`.

Keep the entitlement service provider-neutral so web Stripe subscriptions and store subscriptions can map into the same internal entitlement model.

## Release path

1. Expo development build on physical devices.
2. Automated unit/component checks.
3. End-to-end tests for critical flows where feasible.
4. Internal distribution.
5. TestFlight and Android closed test.
6. Production EAS build with controlled version numbers.
7. Store metadata, screenshots, privacy answers, support and policy URLs.
8. Review notes and test account.
9. Phased/staged rollout with crash and billing monitoring.
