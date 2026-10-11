import unittest
from scripts.verify_profile_evidence import check_readme, validate_packet

PACKET = """# Profile Evidence Packet

Task ID: PROFILE-ZTG-001
Status: IN_PROGRESS
Accountable owner: Profile maintainer
Risk tier: R1

## Claim and risk
Introduce evidence rules for public professional claims.

## Scope and acceptance criteria
Material README, policy, script and workflow changes require an evidence packet documenting claim provenance and limitations.

## Verification plan and results
CI runs profile structure checks and evidence-packet validation against the candidate revision.

## Validation plan and results
A human review must inspect linked repositories and verify each substantive claim against actual work products.

## Public claim sources, security and privacy
Claims point to public work products; private client information, credentials and internal operating details are excluded.

## Limitations and open items
Static checks cannot prove the truth of every professional claim or whether all external links currently resolve.

## Recovery and rollback
Revert the gate if it falsely flags a valid profile or fails to detect a known unfinished-copy/secret pattern.

## Evidence and tested revision
Read the exact candidate SHA and CI result after completion. No claim is accepted by this checker alone.
"""

class ProfileEvidenceTests(unittest.TestCase):
 def test_current_readme_structure(self):
  self.assertEqual(check_readme(),[])
 def test_packet_passes_in_progress(self):
  self.assertEqual(validate_packet(PACKET),[])
 def test_missing_sources_section_fails(self):
  text=PACKET.replace("## Public claim sources, security and privacy\nClaims point to public work products; private client information, credentials and internal operating details are excluded.\n","")
  self.assertTrue(any("missing section" in e for e in validate_packet(text)))
 def test_accepted_without_readback_fails(self):
  text=PACKET.replace("Status: IN_PROGRESS","Status: ACCEPTED")
  self.assertTrue(any("Independent read-back: PASS" in e for e in validate_packet(text)))
if __name__=="__main__": unittest.main()
