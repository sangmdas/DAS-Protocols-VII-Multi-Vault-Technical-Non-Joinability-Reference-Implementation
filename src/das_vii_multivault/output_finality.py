from __future__ import annotations

import hashlib
import secrets
import time
import uuid
from dataclasses import replace

from .authorization import ProtectedAuthorizationDomain
from .canonical import canonical_bytes, sha256_hex
from .crypto import AeadBox, hmac_sign, hmac_verify, without_signature
from .models import (
    CandidateOutput,
    EphemeralDataView,
    OutputReleaseCapability,
    ProtectedOutputValidationReceipt,
    ReconstructionAuthorizationObject,
    SessionContext,
)
from .receipt_store import ProtectedReceiptStore


class OutputDenied(RuntimeError):
    pass


class OutputFinalityController:
    def __init__(
        self,
        authority_secret: bytes,
        output_seal_secret: bytes,
        receipt_store: ProtectedReceiptStore,
        auth: ProtectedAuthorizationDomain,
    ):
        self._authority_secret = authority_secret
        self._box = AeadBox(output_seal_secret)
        self.receipts = receipt_store
        self.auth = auth

    @staticmethod
    def _aad(candidate_stub: dict) -> bytes:
        return canonical_bytes(candidate_stub)

    def form_candidate(
        self,
        payload: str,
        used_fields: tuple[str, ...],
        used_associations,
        view: EphemeralDataView,
        rao: ReconstructionAuthorizationObject,
        session: SessionContext,
    ) -> CandidateOutput:
        self.auth.verify(rao, session)
        if view.rao_digest != self.auth.digest(rao) or view.session_id != session.session_id:
            raise OutputDenied("view not bound to current RAO/session")
        if not set(used_fields).issubset(view.fields):
            raise OutputDenied("candidate uses field outside reconstructed view")
        if not set(used_associations).issubset(set(view.associations)):
            raise OutputDenied("candidate uses unauthorized semantic association")

        candidate_id = str(uuid.uuid4())
        plaintext_digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        stub = {
            "candidate_output_id": candidate_id,
            "rao_digest": view.rao_digest,
            "view_id": view.view_id,
            "session_id": session.session_id,
            "session_epoch": session.session_epoch,
            "policy_epoch": session.policy_epoch,
            "destination": rao.destination,
            "recipient": rao.recipient,
            "output_boundary_id": rao.output_boundary_id,
            "used_fields": tuple(sorted(used_fields)),
            "used_associations": tuple(used_associations),
            "provenance_digest": view.provenance_digest,
            "plaintext_digest": plaintext_digest,
        }
        nonce_b64, ciphertext_b64 = self._box.seal(payload.encode("utf-8"), self._aad(stub))
        return CandidateOutput(**stub, nonce_b64=nonce_b64, ciphertext_b64=ciphertext_b64)

    @staticmethod
    def candidate_digest(candidate: CandidateOutput) -> str:
        return sha256_hex(candidate)

    def verify_and_authorize(
        self,
        candidate: CandidateOutput,
        view: EphemeralDataView,
        rao: ReconstructionAuthorizationObject,
        session: SessionContext,
        current_destination: str,
        current_recipient: str,
        current_policy_epoch: int,
        current_session_epoch: int,
        ttl_seconds: int = 30,
    ) -> tuple[ProtectedOutputValidationReceipt, OutputReleaseCapability]:
        self.auth.verify(rao, session)
        if candidate.rao_digest != self.auth.digest(rao) or candidate.view_id != view.view_id:
            raise OutputDenied("candidate/RAO/view mismatch")
        if candidate.provenance_digest != view.provenance_digest:
            raise OutputDenied("provenance continuity failure")
        if not set(candidate.used_fields).issubset(view.fields):
            raise OutputDenied("candidate field scope mismatch")
        if not set(candidate.used_associations).issubset(set(rao.permitted_associations)):
            raise OutputDenied("candidate association scope mismatch")
        if current_destination != rao.destination or current_recipient != rao.recipient:
            raise OutputDenied("destination or recipient changed")
        if current_policy_epoch != session.policy_epoch or candidate.policy_epoch != current_policy_epoch:
            raise OutputDenied("policy epoch mismatch")
        if current_session_epoch != session.session_epoch or candidate.session_epoch != current_session_epoch:
            raise OutputDenied("session epoch mismatch")

        receipt_unsigned = ProtectedOutputValidationReceipt(
            receipt_id=str(uuid.uuid4()),
            candidate_output_id=candidate.candidate_output_id,
            candidate_output_digest=self.candidate_digest(candidate),
            rao_digest=candidate.rao_digest,
            provenance_digest=candidate.provenance_digest,
            session_id=session.session_id,
            session_epoch=session.session_epoch,
            policy_epoch=session.policy_epoch,
            destination=current_destination,
            recipient=current_recipient,
            output_boundary_id=candidate.output_boundary_id,
            committed_at=time.time(),
            signature="",
        )
        receipt = replace(receipt_unsigned, signature=hmac_sign(self._authority_secret, receipt_unsigned))

        # Constitutive ordering: commit must succeed before capability can exist.
        receipt_digest = self.receipts.commit(receipt)

        now = time.time()
        cap_unsigned = OutputReleaseCapability(
            capability_id=str(uuid.uuid4()),
            candidate_output_digest=self.candidate_digest(candidate),
            receipt_digest=receipt_digest,
            session_id=session.session_id,
            session_epoch=session.session_epoch,
            policy_epoch=session.policy_epoch,
            destination=current_destination,
            recipient=current_recipient,
            output_boundary_id=candidate.output_boundary_id,
            nonce=secrets.token_hex(16),
            issued_at=now,
            expires_at=now + ttl_seconds,
            signature="",
        )
        cap = replace(cap_unsigned, signature=hmac_sign(self._authority_secret, cap_unsigned))
        return receipt, cap

    def verify_receipt(self, receipt: ProtectedOutputValidationReceipt) -> bool:
        return hmac_verify(self._authority_secret, without_signature(receipt), receipt.signature)

    def verify_capability(self, capability: OutputReleaseCapability) -> bool:
        return hmac_verify(self._authority_secret, without_signature(capability), capability.signature)

    def decrypt_candidate(self, candidate: CandidateOutput) -> str:
        stub = {
            "candidate_output_id": candidate.candidate_output_id,
            "rao_digest": candidate.rao_digest,
            "view_id": candidate.view_id,
            "session_id": candidate.session_id,
            "session_epoch": candidate.session_epoch,
            "policy_epoch": candidate.policy_epoch,
            "destination": candidate.destination,
            "recipient": candidate.recipient,
            "output_boundary_id": candidate.output_boundary_id,
            "used_fields": candidate.used_fields,
            "used_associations": candidate.used_associations,
            "provenance_digest": candidate.provenance_digest,
            "plaintext_digest": candidate.plaintext_digest,
        }
        plain = self._box.open(candidate.nonce_b64, candidate.ciphertext_b64, self._aad(stub))
        if hashlib.sha256(plain).hexdigest() != candidate.plaintext_digest:
            raise OutputDenied("sealed output integrity mismatch")
        return plain.decode("utf-8")
