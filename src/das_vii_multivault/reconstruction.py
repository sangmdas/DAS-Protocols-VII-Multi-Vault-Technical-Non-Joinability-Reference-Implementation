from __future__ import annotations

import uuid

from .authorization import ProtectedAuthorizationDomain
from .canonical import sha256_hex
from .models import EphemeralDataView, ReconstructionAuthorizationObject, SessionBoundComponent, SessionContext
from .vaults import VaultCoordinator, VaultDenied


class ReconstructionDenied(RuntimeError):
    pass


class ProtectedReconstructionDomain:
    def __init__(self, coordinator: VaultCoordinator, auth: ProtectedAuthorizationDomain):
        self.coordinator = coordinator
        self.auth = auth

    def reconstruct(
        self,
        rao: ReconstructionAuthorizationObject,
        session: SessionContext,
        components: tuple[SessionBoundComponent, ...],
    ) -> EphemeralDataView:
        self.auth.verify(rao, session)
        if len(components) != 3:
            raise ReconstructionDenied("all required semantic domains are required")

        by_kind = {}
        for component in components:
            try:
                self.coordinator.verify(component)
            except VaultDenied as exc:
                raise ReconstructionDenied(str(exc)) from exc
            if component.session_id != session.session_id or component.session_epoch != session.session_epoch:
                raise ReconstructionDenied("cross-session component reuse")
            if component.workload_measurement != session.workload_measurement:
                raise ReconstructionDenied("workload context mismatch")
            if component.rao_digest != self.auth.digest(rao):
                raise ReconstructionDenied("component belongs to another RAO")
            if component.vault_kind in by_kind:
                raise ReconstructionDenied("duplicate semantic domain")
            by_kind[component.vault_kind] = component

        required = {"identity", "content", "relationship"}
        if set(by_kind) != required:
            raise ReconstructionDenied("missing required vault-local release")

        rel = by_kind["relationship"].data
        if rel.get("identity_id") != rao.identity_id or rel.get("content_id") != rao.content_id:
            raise ReconstructionDenied("relationship/component mismatch")

        rule = next(
            (
                a for a in rao.permitted_associations
                if a.identity_id == rel["identity_id"]
                and a.content_id == rel["content_id"]
                and a.relation == rel["relation"]
            ),
            None,
        )
        if rule is None:
            raise ReconstructionDenied("association not authorized")

        fields: dict[str, object] = {}
        provenance: dict[str, str] = {}
        for kind in ("identity", "content"):
            comp = by_kind[kind]
            for key, value in comp.data.items():
                fq = f"{kind}.{key}"
                if fq not in rao.permitted_fields:
                    raise ReconstructionDenied("vault released field outside RAO")
                fields[fq] = value
                provenance[fq] = f"{comp.vault_id}:{comp.component_id}"

        provenance[f"association:{rule.identity_id}:{rule.content_id}:{rule.relation}"] = by_kind["relationship"].vault_id
        p_digest = sha256_hex({"fields": provenance, "association": rule})
        return EphemeralDataView(
            view_id=str(uuid.uuid4()),
            rao_digest=self.auth.digest(rao),
            session_id=session.session_id,
            session_epoch=session.session_epoch,
            fields=fields,
            associations=(rule,),
            provenance=provenance,
            provenance_digest=p_digest,
        )
