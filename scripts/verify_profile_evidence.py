#!/usr/bin/env python3
"""Verify public profile structure and require packets for material public-claim edits."""
import json, os, re, subprocess, sys
from pathlib import Path

MATERIAL={"README.md","AGENTS.md","scripts/verify_profile_evidence.py","tests/test_profile_evidence.py",".github/workflows/public-profile-integrity.yml"}
HEADINGS=("## Claim and risk","## Scope and acceptance criteria","## Verification plan and results","## Validation plan and results","## Public claim sources, security and privacy","## Limitations and open items","## Recovery and rollback","## Evidence and tested revision")
STATUSES={"DRAFT","IN_PROGRESS","BLOCKED","FAILED","VERIFIED","VALIDATED","ACCEPTED","ACCEPTED_RISK","DEFERRED"}

def validate_packet(text,path="<packet>"):
 errors=[]; m=re.search(r"(?im)^Status:\s*([A-Z_]+)\s*$",text); status=m.group(1) if m else None
 if status not in STATUSES: errors.append(path+": missing/invalid Status")
 for f,p in (("Task ID",r"(?im)^Task ID:\s*\S+"),("Accountable owner",r"(?im)^Accountable owner:\s*\S+"),("Risk tier",r"(?im)^Risk tier:\s*(R0|R1|R2|R3)\b")):
  if not re.search(p,text): errors.append(path+": missing "+f)
 for h in HEADINGS:
  m=re.search(r"(?m)^"+re.escape(h)+r"\s*$",text)
  if not m: errors.append(path+": missing section "+h); continue
  n=re.search(r"(?m)^##\s+",text[m.end():]); end=m.end()+n.start() if n else len(text); body=text[m.end():end].strip()
  if len(re.sub(r"\s+|[>#*_\-\[\]]","",body))<18: errors.append(path+": empty section "+h)
  if re.search(r"(?i)\b(TODO|TBD|PLACEHOLDER|FILL\s+IN|WRITE\s+HERE)\b",body): errors.append(path+": unresolved placeholder in "+h)
 if status in {"VERIFIED","VALIDATED","ACCEPTED"}:
  for f in ("Verification status: PASS","Validation status: PASS","Independent read-back: PASS"):
   if not re.search(r"(?im)^"+re.escape(f)+r"\s*$",text): errors.append(path+": cannot be "+status+" without "+f)
  if not re.search(r"(?im)^Tested revision:\s*[0-9a-f]{7,40}\s*$",text): errors.append(path+": accepted status needs tested SHA")
  if not re.search(r"(?im)^Acceptance authority:\s*\S+",text): errors.append(path+": accepted status needs acceptance authority")
 return errors

def check_readme():
 p=Path("README.md")
 if not p.exists(): return ["README.md missing"]
 text=p.read_text(encoding="utf-8")
 errs=[]
 if not re.search(r"(?m)^#\s+Praful Jadhav\s*$",text): errs.append("profile title missing")
 if not re.search(r"(?m)^##\s+Proof of work\s*$",text): errs.append("Proof of work section missing")
 if re.search(r"(?i)\b(Lorem ipsum|TODO|TBD|PLACEHOLDER|YOUR_NAME|example\.com)\b",text): errs.append("placeholder/demo content detected in public profile")
 patterns=(r"ghp_[A-Za-z0-9]{30,}",r"AKIA[0-9A-Z]{16}",r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",r"sk-[A-Za-z0-9]{32,}")
 if any(re.search(p,text) for p in patterns): errs.append("high-risk credential pattern detected in profile")
 return errs

def changes(name,event):
 if name=="pull_request":
  base=event.get("pull_request",{}).get("base",{}).get("sha")
  if not base: raise ValueError("missing PR base SHA")
  exists=subprocess.run(["git","cat-file","-e",base+"^{commit}"],capture_output=True,text=True)
  if exists.returncode!=0: subprocess.run(["git","fetch","--quiet","--no-tags","origin",base],check=True,capture_output=True,text=True)
  cmd=["git","diff","--name-only",base+"...HEAD"]
 elif name=="push":
  before,after=event.get("before",""),event.get("after","HEAD")
  cmd=(["git","ls-tree","-r","--name-only",after] if not before or set(before)=={"0"} else ["git","diff","--name-only",before,after])
 else:return []
 r=subprocess.run(cmd,check=True,capture_output=True,text=True)
 return [x.strip() for x in r.stdout.splitlines() if x.strip()]

def main():
 errors=check_readme()
 name=os.environ.get("GITHUB_EVENT_NAME","")
 if name in {"pull_request","push"}:
  try:
   event=json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8")); paths=changes(name,event)
  except Exception as e: errors.append("cannot establish candidate diff: "+str(e)); paths=[]
  touched=[p for p in paths if p in MATERIAL]
  if touched:
   packets=[p for p in paths if p.startswith("docs/evidence/") and p.endswith(".md")]
   if not packets: errors.append("material profile/review change without docs/evidence/*.md packet")
   for p in packets:
    try: errors.extend(validate_packet(Path(p).read_text(encoding="utf-8"),p))
    except Exception as e: errors.append(p+": cannot read packet: "+str(e))
 if errors:
  print("FAIL: "+str(len(errors))+" issue(s)")
  for e in errors: print("- "+e)
  return 1
 print("PASS: profile structure and applicable evidence packet checks.")
 print("This does not prove every public claim or external link.")
 return 0
if __name__=="__main__": raise SystemExit(main())
