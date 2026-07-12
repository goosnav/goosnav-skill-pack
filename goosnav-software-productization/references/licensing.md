# Licensing and public distribution

## Terminology

- **Proprietary / all rights reserved:** source may be private or visible, but no broad permission is granted.
- **Source-available:** source is visible under restrictions such as noncommercial or delayed-open terms. This is not open source under the standard OSI meaning.
- **Open source:** an OSI-compatible license permits use, modification, and redistribution under its terms.
- **Dual license:** the same code is offered under two licensing paths, often open-source plus commercial.

Do not tell users a repository is open source if its license forbids commercial use, redistribution, or modification.

## Default Goosnav posture

Unless the user selects another model:

1. core commercial application: proprietary, all rights reserved;
2. public CLI/client libraries: evaluate a separate permissive license only when community adoption materially benefits the business;
3. templates/examples: license explicitly;
4. third-party dependencies/assets/fonts/icons: track their licenses and attribution requirements;
5. public repository with proprietary source: include an explicit license notice; absence of a license creates ambiguity, not a useful community grant.

## Separation strategies

When open community automation is valuable but the product must remain protected:

- publish a thin CLI/API client under MIT or Apache-2.0 while keeping service implementation proprietary;
- publish provider adapters or SDKs separately;
- use an open-core model with a clearly separated commercial module;
- use a source-available license only after reviewing whether its restrictions and ecosystem consequences are acceptable;
- use trademark policy and service operation as protection rather than pretending copyright can prevent all imitation.

## Required project action

At M0, select and record:

- owner/copyright entity;
- private, proprietary-visible, source-available, open-source, or dual-license model;
- license file;
- contributor policy;
- third-party attribution process;
- whether user-generated content has separate terms.

For material commercial distribution, have the selected license and terms reviewed by qualified counsel.
