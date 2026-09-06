from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SessionContext:
    session_id: str
    tenant_id: str
    workload_id: str
    workload_measurement: str
    session_epoch: int
    policy_epoch: int


@dataclass(frozen=True)
class AssociationRule:
    identity_id: str
    content_id: str
    relation: str


@dataclass(frozen=True)
class ReconstructionRequest:
    identity_id: str
    content_id: str
    relationship_id: str
    purpose: str
    destination: str
    recipient: str
    permitted_fields: tuple[str, ...]
    permitted_associations: tuple[AssociationRule, ...]
    output_boundary_id: str
    ttl_seconds: int = 60


@dataclass(frozen=True)
class ReconstructionAuthorizationObject:
    rao_id: str
    tenant_id: str
    workload_id: str
    workload_measurement: str
    session_id: str
    session_epoch: int
    policy_epoch: int
    nonce: str
    identity_id: str
    content_id: str
    relationship_id: str
    permitted_fields: tuple[str, ...]
    permitted_associations: tuple[AssociationRule, ...]
    purpose: str
    destination: str
    recipient: str
    output_boundary_id: str
    issued_at: float
    expires_at: float
    signature: str = ""


@dataclass(frozen=True)
class SessionBoundComponent:
    vault_id: str
    vault_kind: str
    component_id: str
    data: dict[str, Any]
    rao_digest: str
    session_id: str
    session_epoch: int
    workload_measurement: str
    issued_at: float
    expires_at: float
    signature: str


@dataclass(frozen=True)
class EphemeralDataView:
    view_id: str
    rao_digest: str
    session_id: str
    session_epoch: int
    fields: dict[str, Any]
    associations: tuple[AssociationRule, ...]
    provenance: dict[str, str]
    provenance_digest: str


@dataclass(frozen=True)
class CandidateOutput:
    candidate_output_id: str
    rao_digest: str
    view_id: str
    session_id: str
    session_epoch: int
    policy_epoch: int
    destination: str
    recipient: str
    output_boundary_id: str
    used_fields: tuple[str, ...]
    used_associations: tuple[AssociationRule, ...]
    provenance_digest: str
    plaintext_digest: str
    nonce_b64: str
    ciphertext_b64: str


@dataclass(frozen=True)
class ProtectedOutputValidationReceipt:
    receipt_id: str
    candidate_output_id: str
    candidate_output_digest: str
    rao_digest: str
    provenance_digest: str
    session_id: str
    session_epoch: int
    policy_epoch: int
    destination: str
    recipient: str
    output_boundary_id: str
    committed_at: float
    signature: str = ""


@dataclass(frozen=True)
class OutputReleaseCapability:
    capability_id: str
    candidate_output_digest: str
    receipt_digest: str
    session_id: str
    session_epoch: int
    policy_epoch: int
    destination: str
    recipient: str
    output_boundary_id: str
    nonce: str
    issued_at: float
    expires_at: float
    signature: str = ""


@dataclass(frozen=True)
class ReleaseDecision:
    allow: bool
    code: str
    message: str
    released_payload: str | None = None
    receipt_id: str | None = None
    capability_id: str | None = None


@dataclass
class MutableSessionState:
    context: SessionContext
    active: bool = True
    poisoned: bool = False
    poison_reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
