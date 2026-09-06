from __future__ import annotations

import secrets
import time
import uuid
from dataclasses import replace

from .canonical import sha256_hex
from .crypto import hmac_sign, hmac_verify, without_signature
from .models import (
    MutableSessionState,
    ReconstructionAuthorizationObject,
    ReconstructionRequest,
    SessionContext,
)


class AuthorizationError(RuntimeError):
    pass


class SessionRegistry:
    def __init__(self):
        self._sessions: dict[str, MutableSessionState] = {}

    def register(self, context: SessionContext) -> None:
        self._sessions[context.session_id] = MutableSessionState(context=context)

    def get(self, session_id: str) -> MutableSessionState:
        state = self._sessions.get(session_id)
        if state is None:
            raise AuthorizationError("unknown session")
        return state

    def require_active(self, context: SessionContext) -> None:
        state = self.get(context.session_id)
        if not state.active or state.poisoned:
            raise AuthorizationError("session is inactive or poisoned")
        if state.context != context:
            raise AuthorizationError("session context mismatch")

    def poison(self, session_id: str, reason: str) -> None:
        state = self.get(session_id)
        state.poisoned = True
        state.active = False
        state.poison_reason = reason


class ProtectedAuthorizationDomain:
    def __init__(self, secret: bytes, sessions: SessionRegistry):
        self._secret = secret
        self.sessions = sessions

    def issue(self, request: ReconstructionRequest, session: SessionContext) -> ReconstructionAuthorizationObject:
        self.sessions.require_active(session)
        now = time.time()
        unsigned = ReconstructionAuthorizationObject(
            rao_id=str(uuid.uuid4()),
            tenant_id=session.tenant_id,
            workload_id=session.workload_id,
            workload_measurement=session.workload_measurement,
            session_id=session.session_id,
            session_epoch=session.session_epoch,
            policy_epoch=session.policy_epoch,
            nonce=secrets.token_hex(16),
            identity_id=request.identity_id,
            content_id=request.content_id,
            relationship_id=request.relationship_id,
            permitted_fields=tuple(sorted(set(request.permitted_fields))),
            permitted_associations=request.permitted_associations,
            purpose=request.purpose,
            destination=request.destination,
            recipient=request.recipient,
            output_boundary_id=request.output_boundary_id,
            issued_at=now,
            expires_at=now + request.ttl_seconds,
        )
        sig = hmac_sign(self._secret, unsigned)
        return replace(unsigned, signature=sig)

    def verify(self, rao: ReconstructionAuthorizationObject, session: SessionContext) -> None:
        self.sessions.require_active(session)
        if not hmac_verify(self._secret, without_signature(rao), rao.signature):
            raise AuthorizationError("invalid RAO signature")
        if time.time() > rao.expires_at:
            raise AuthorizationError("expired RAO")
        expected = (
            rao.tenant_id,
            rao.workload_id,
            rao.workload_measurement,
            rao.session_id,
            rao.session_epoch,
            rao.policy_epoch,
        )
        actual = (
            session.tenant_id,
            session.workload_id,
            session.workload_measurement,
            session.session_id,
            session.session_epoch,
            session.policy_epoch,
        )
        if expected != actual:
            raise AuthorizationError("RAO/session protected-state mismatch")

    @staticmethod
    def digest(rao: ReconstructionAuthorizationObject) -> str:
        return sha256_hex(rao)
