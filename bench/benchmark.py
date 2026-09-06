from __future__ import annotations

import os
import statistics
import sys
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from das_vii_multivault.authorization import ProtectedAuthorizationDomain, SessionRegistry
from das_vii_multivault.boundary import OutputReleaseBoundary
from das_vii_multivault.legacy import LegacyGateway, LegacyRecordAdapter
from das_vii_multivault.models import SessionContext
from das_vii_multivault.output_finality import OutputFinalityController
from das_vii_multivault.receipt_store import ProtectedReceiptStore
from das_vii_multivault.reconstruction import ProtectedReconstructionDomain
from das_vii_multivault.vaults import ProtectedVault, VaultCoordinator


def pct(values, p):
    values = sorted(values)
    idx = min(len(values) - 1, int(round((p / 100) * (len(values) - 1))))
    return values[idx]


def stats(label, ns):
    us = [v / 1000 for v in ns]
    print(f"{label:34s} median={statistics.median(us):8.2f} us  p95={pct(us,95):8.2f} us  p99={pct(us,99):8.2f} us")


def build():
    joined = {"name":"Alice","email":"a@example.test","case_summary":"battery event","future_program":"Aurora"}
    adapter = LegacyRecordAdapter()
    ids, identity, content, relationship = adapter.split_record("77", joined, ("name","email"), ("case_summary","future_program"))
    sessions = SessionRegistry()
    session = SessionContext("bench", "tenant", "ai", "sha256:bench", 1, 1)
    sessions.register(session)
    auth = ProtectedAuthorizationDomain(b"auth", sessions)
    coordinator = VaultCoordinator(
        ProtectedVault("i","identity",b"i",{ids.identity_id:identity}),
        ProtectedVault("c","content",b"c",{ids.content_id:content}),
        ProtectedVault("r","relationship",b"r",{ids.relationship_id:relationship}),
    )
    request = LegacyGateway().make_request(ids,"support","internal","analyst",("identity.name","content.case_summary"),"b")
    prd = ProtectedReconstructionDomain(coordinator, auth)
    store = ProtectedReceiptStore()
    ctl = OutputFinalityController(b"out",b"seal",store,auth)
    boundary = OutputReleaseBoundary("b",ctl,auth)
    return session, auth, coordinator, request, prd, ctl, boundary


def main(iterations=500):
    session, auth, coordinator, request, prd, ctl, boundary = build()
    auth_ns=[]; vault_ns=[]; recon_ns=[]; output_ns=[]; total_ns=[]
    for _ in range(iterations):
        t0=time.perf_counter_ns()
        rao=auth.issue(request,session)
        t1=time.perf_counter_ns()
        comps=coordinator.release_required(rao,session,auth,parallel=False)
        t2=time.perf_counter_ns()
        view=prd.reconstruct(rao,session,comps)
        t3=time.perf_counter_ns()
        candidate=ctl.form_candidate("safe summary",("identity.name","content.case_summary"),view.associations,view,rao,session)
        receipt,cap=ctl.verify_and_authorize(candidate,view,rao,session,"internal","analyst",1,1)
        decision=boundary.release(candidate,receipt,cap,session,"internal","analyst",1,1)
        if not decision.allow:
            raise RuntimeError(decision)
        t4=time.perf_counter_ns()
        auth_ns.append(t1-t0); vault_ns.append(t2-t1); recon_ns.append(t3-t2); output_ns.append(t4-t3); total_ns.append(t4-t0)
    print(f"iterations={iterations}; local single-process benchmark; warm components; sequential local vault calls")
    stats("RAO issue",auth_ns)
    stats("3 vault-local releases",vault_ns)
    stats("protected reconstruction",recon_ns)
    stats("seal+POVR+cap+boundary release",output_ns)
    stats("end-to-end protected path",total_ns)
    print("\nEXCLUDES: AI inference, network/RPC, remote vault latency, remote attestation, HSM/KMS, distributed commit, human approval, production logging.")
    print("Parallel vault fan-out exists in the implementation, but local CPU-only timing is not a proxy for remote parallel-RPC benefit.")


if __name__ == "__main__":
    main()
