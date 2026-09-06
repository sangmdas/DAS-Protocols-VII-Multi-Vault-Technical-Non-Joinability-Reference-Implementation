from __future__ import annotations

import time

from .authorization import ProtectedAuthorizationDomain
from .canonical import sha256_hex
from .models import (
    CandidateOutput,
    OutputReleaseCapability,
    ProtectedOutputValidationReceipt,
    ReleaseDecision,
    SessionContext,
)
from .output_finality import OutputFinalityController


class OutputReleaseBoundary:
    def __init__(self, boundary_id: str, controller: OutputFinalityController, auth: ProtectedAuthorizationDomain):
        self.boundary_id = boundary_id
        self.controller = controller
        self.auth = auth

    def release(
        self,
        candidate: CandidateOutput,
        receipt: ProtectedOutputValidationReceipt,
        capability: OutputReleaseCapability,
        session: SessionContext,
        current_destination: str,
        current_recipient: str,
        current_policy_epoch: int,
        current_session_epoch: int,
    ) -> ReleaseDecision:
        try:
            self.auth.sessions.require_active(session)
            if capability.output_boundary_id != self.boundary_id or candidate.output_boundary_id != self.boundary_id:
                return ReleaseDecision(False, "MV_BOUNDARY_MISMATCH", "wrong Output Release Boundary")
            if time.time() > capability.expires_at:
                return ReleaseDecision(False, "MV_CAP_EXPIRED", "release capability expired")
            if not self.controller.verify_capability(capability):
                return ReleaseDecision(False, "MV_CAP_INVALID", "invalid release capability")
            if not self.controller.verify_receipt(receipt):
                return ReleaseDecision(False, "MV_RECEIPT_INVALID", "invalid POVR signature")
            if capability.candidate_output_digest != self.controller.candidate_digest(candidate):
                return ReleaseDecision(False, "MV_OUTPUT_MISMATCH", "candidate output changed")
            if receipt.candidate_output_digest != capability.candidate_output_digest:
                return ReleaseDecision(False, "MV_RECEIPT_OUTPUT_MISMATCH", "POVR does not bind this output")
            if capability.receipt_digest != sha256_hex(receipt):
                return ReleaseDecision(False, "MV_RECEIPT_DIGEST_MISMATCH", "capability/POVR mismatch")
            if not self.controller.receipts.contains_digest(receipt.receipt_id, capability.receipt_digest):
                return ReleaseDecision(False, "MV_RECEIPT_NOT_COMMITTED", "POVR not durably committed")
            if (current_destination, current_recipient) != (capability.destination, capability.recipient):
                return ReleaseDecision(False, "MV_DESTINATION_MISMATCH", "destination or recipient changed")
            if current_policy_epoch != capability.policy_epoch or current_session_epoch != capability.session_epoch:
                return ReleaseDecision(False, "MV_EPOCH_MISMATCH", "current protected epoch changed")
            if candidate.session_id != session.session_id or capability.session_id != session.session_id:
                return ReleaseDecision(False, "MV_SESSION_MISMATCH", "cross-session use")
            if not self.controller.receipts.consume_once(capability.capability_id, time.time()):
                return ReleaseDecision(False, "MV_REPLAY", "release capability already consumed")
            payload = self.controller.decrypt_candidate(candidate)
            return ReleaseDecision(
                True,
                "MV_ALLOW",
                "verified output released exactly once",
                released_payload=payload,
                receipt_id=receipt.receipt_id,
                capability_id=capability.capability_id,
            )
        except Exception as exc:
            return ReleaseDecision(False, "MV_FAIL_CLOSED", str(exc))
