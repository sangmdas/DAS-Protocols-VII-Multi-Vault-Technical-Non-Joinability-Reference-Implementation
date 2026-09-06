from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from typing import Any

from .authorization import ProtectedAuthorizationDomain
from .canonical import sha256_hex
from .crypto import hmac_sign, hmac_verify
from .models import (
    AssociationRule,
    ReconstructionAuthorizationObject,
    SessionBoundComponent,
    SessionContext,
)


class VaultDenied(RuntimeError):
    pass


class ProtectedVault:
    def __init__(self, vault_id: str, vault_kind: str, secret: bytes, records: dict[str, dict[str, Any]]):
        self.vault_id = vault_id
        self.vault_kind = vault_kind
        self._secret = secret
        self._records = records

    def _allowed_record_id(self, rao: ReconstructionAuthorizationObject) -> str:
        if self.vault_kind == "identity":
            return rao.identity_id
        if self.vault_kind == "content":
            return rao.content_id
        if self.vault_kind == "relationship":
            return rao.relationship_id
        raise VaultDenied(f"unsupported vault kind: {self.vault_kind}")

    def _project(self, record_id: str, rao: ReconstructionAuthorizationObject) -> dict[str, Any]:
        if record_id not in self._records:
            raise VaultDenied(f"{self.vault_id}: unknown component")
        record = self._records[record_id]

        if self.vault_kind == "identity":
            permitted = {f.split(".", 1)[1] for f in rao.permitted_fields if f.startswith("identity.")}
            return {k: v for k, v in record.items() if k in permitted}
        if self.vault_kind == "content":
            permitted = {f.split(".", 1)[1] for f in rao.permitted_fields if f.startswith("content.")}
            return {k: v for k, v in record.items() if k in permitted}
        if self.vault_kind == "relationship":
            rule = AssociationRule(
                identity_id=record["identity_id"],
                content_id=record["content_id"],
                relation=record["relation"],
            )
            if rule not in rao.permitted_associations:
                raise VaultDenied("relationship not inside Permitted Association Scope")
            return dict(record)
        raise VaultDenied("unsupported vault kind")

    def release(
        self,
        record_id: str,
        rao: ReconstructionAuthorizationObject,
        session: SessionContext,
        auth: ProtectedAuthorizationDomain,
    ) -> SessionBoundComponent:
        auth.verify(rao, session)
        if record_id != self._allowed_record_id(rao):
            raise VaultDenied(f"{self.vault_id}: component substitution")
        data = self._project(record_id, rao)
        if self.vault_kind in {"identity", "content"} and not data:
            raise VaultDenied(f"{self.vault_id}: no authorized fields")
        unsigned = SessionBoundComponent(
            vault_id=self.vault_id,
            vault_kind=self.vault_kind,
            component_id=record_id,
            data=data,
            rao_digest=auth.digest(rao),
            session_id=session.session_id,
            session_epoch=session.session_epoch,
            workload_measurement=session.workload_measurement,
            issued_at=time.time(),
            expires_at=min(rao.expires_at, time.time() + 30),
            signature="",
        )
        return replace(unsigned, signature=hmac_sign(self._secret, unsigned))

    def verify_component(self, component: SessionBoundComponent) -> None:
        unsigned = replace(component, signature="")
        if component.vault_id != self.vault_id or component.vault_kind != self.vault_kind:
            raise VaultDenied("vault identity mismatch")
        if not hmac_verify(self._secret, unsigned, component.signature):
            raise VaultDenied("invalid vault-local component signature")
        if time.time() > component.expires_at:
            raise VaultDenied("expired session-bound component")


class VaultCoordinator:
    def __init__(self, identity: ProtectedVault, content: ProtectedVault, relationship: ProtectedVault):
        self.identity = identity
        self.content = content
        self.relationship = relationship
        self._by_id = {v.vault_id: v for v in (identity, content, relationship)}

    def verify(self, component: SessionBoundComponent) -> None:
        vault = self._by_id.get(component.vault_id)
        if vault is None:
            raise VaultDenied("unknown releasing vault")
        vault.verify_component(component)

    def release_required(
        self,
        rao: ReconstructionAuthorizationObject,
        session: SessionContext,
        auth: ProtectedAuthorizationDomain,
        parallel: bool = True,
    ) -> tuple[SessionBoundComponent, ...]:
        calls = (
            (self.identity, rao.identity_id),
            (self.content, rao.content_id),
            (self.relationship, rao.relationship_id),
        )
        if not parallel:
            return tuple(v.release(record_id, rao, session, auth) for v, record_id in calls)
        with ThreadPoolExecutor(max_workers=len(calls)) as pool:
            futures = [pool.submit(v.release, record_id, rao, session, auth) for v, record_id in calls]
            # Fail closed: any vault exception aborts the whole reconstruction.
            return tuple(f.result() for f in futures)
