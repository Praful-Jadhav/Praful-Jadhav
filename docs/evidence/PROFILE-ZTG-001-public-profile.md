# Evidence Packet — Public Profile Integrity Gate

Task ID: PROFILE-ZTG-001
Status: IN_PROGRESS
Accountable owner: Profile maintainer
Risk tier: R1

## Claim and risk
Add a lightweight integrity and evidence gate to the public professional profile. Risk is presenting plans, generated descriptions or unreconciled repository claims as demonstrated capabilities.

## Scope and acceptance criteria
In scope: profile rules, README structure and known-pattern checks, evidence packet validator, tests and CI workflow. Out of scope: automatic proof of professional history, external link reachability and reputation/perception testing. Material profile changes require a source-controlled packet, and placeholder/secret-pattern checks must pass.

## Verification plan and results
CI will run Python tests and validate README structure plus this packet against the exact candidate revision. Record the final SHA and run result after completion. No PASS is asserted in advance.

## Validation plan and results
A human must verify the linked repositories and claims of demonstrated work. The profile should distinguish current work, research, prototypes and future interests without implying unverified outcomes.

## Public claim sources, security and privacy
Use public work artifacts as evidence. Do not expose private client details, personal secrets, credentials, confidential operational data or internal-only ecosystem structure.

## Limitations and open items
Static checks do not prove every factual claim or verify external links. Manual evidence review and rendered profile inspection remain required for substantial edits.

## Recovery and rollback
Revert the evidence gate if it creates false positives or fails to detect the tested draft-marker/credential patterns.

## Evidence and tested revision
Use the final Actions run to record the exact candidate SHA. Keep status IN_PROGRESS until the checks pass and the profile claims are reviewed.
