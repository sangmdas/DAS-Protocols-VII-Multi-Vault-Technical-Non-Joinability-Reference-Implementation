from __future__ import annotations

from .authorization import ProtectedAuthorizationDomain, SessionRegistry
from .boundary import OutputReleaseBoundary
from .legacy import LegacyGateway, LegacyRecordAdapter
from .models import SessionContext
from .output_finality import OutputFinalityController
from .receipt_store import ProtectedReceiptStore
from .reconstruction import ProtectedReconstructionDomain
from .vaults import ProtectedVault, VaultCoordinator


def build_demo():
    joined = {
        "name": "Alice Example",
        "email": "alice@example.test",
        "case_summary": "Device battery overheated during evaluation",
        "future_program": "Project Aurora",
    }
    adapter = LegacyRecordAdapter()
    ids, identity, content, relationship = adapter.split_record(
        "case-77", joined, ("name", "email"), ("case_summary", "future_program")
    )

    sessions = SessionRegistry()
    session = SessionContext(
        session_id="sess-demo-001",
        tenant_id="tenant-demo",
        workload_id="ai-assistant-demo",
        workload_measurement="sha256:demo-workload-measurement",
        session_epoch=7,
        policy_epoch=12,
    )
    sessions.register(session)
    auth = ProtectedAuthorizationDomain(b"demo-auth-secret", sessions)

    identity_vault = ProtectedVault("vault-identity", "identity", b"identity-vault-secret", {ids.identity_id: identity})
    content_vault = ProtectedVault("vault-content", "content", b"content-vault-secret", {ids.content_id: content})
    relationship_vault = ProtectedVault(
        "vault-relationship", "relationship", b"relationship-vault-secret", {ids.relationship_id: relationship}
    )
    coordinator = VaultCoordinator(identity_vault, content_vault, relationship_vault)
    prd = ProtectedReconstructionDomain(coordinator, auth)

    gateway = LegacyGateway()
    request = gateway.make_request(
        ids,
        purpose="customer-support",
        destination="internal-case-ui",
        recipient="support-analyst",
        permitted_fields=("identity.name", "content.case_summary"),
        boundary_id="boundary-support-ui",
    )
    rao = auth.issue(request, session)
    components = coordinator.release_required(rao, session, auth, parallel=True)
    view = prd.reconstruct(rao, session, components)

    receipts = ProtectedReceiptStore()
    controller = OutputFinalityController(b"output-authority-secret", b"output-seal-secret", receipts, auth)
    boundary = OutputReleaseBoundary("boundary-support-ui", controller, auth)
    return session, auth, rao, view, controller, boundary


def main() -> None:
    session, auth, rao, view, controller, boundary = build_demo()

    payload = f"Support summary for {view.fields['identity.name']}: {view.fields['content.case_summary']}"
    candidate = controller.form_candidate(
        payload,
        used_fields=("identity.name", "content.case_summary"),
        used_associations=view.associations,
        view=view,
        rao=rao,
        session=session,
    )
    receipt, cap = controller.verify_and_authorize(
        candidate,
        view,
        rao,
        session,
        current_destination="internal-case-ui",
        current_recipient="support-analyst",
        current_policy_epoch=session.policy_epoch,
        current_session_epoch=session.session_epoch,
    )
    decision = boundary.release(
        candidate,
        receipt,
        cap,
        session,
        current_destination="internal-case-ui",
        current_recipient="support-analyst",
        current_policy_epoch=session.policy_epoch,
        current_session_epoch=session.session_epoch,
    )
    print(decision)


if __name__ == "__main__":
    main()
