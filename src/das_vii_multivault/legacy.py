from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .models import AssociationRule, ReconstructionRequest


@dataclass(frozen=True)
class MigratedRecordIds:
    identity_id: str
    content_id: str
    relationship_id: str


class LegacyRecordAdapter:
    """Demonstrates incremental decomposition of a joined legacy record.

    It is intentionally explicit: production migration must remove/mediate the old
    unrestricted join path. Copying fields into vaults while leaving a bypassable joined
    database exposed does not establish Technical Non-Joinability.
    """

    def split_record(
        self,
        record_id: str,
        record: dict[str, Any],
        identity_fields: tuple[str, ...],
        content_fields: tuple[str, ...],
        relation: str = "belongs_to",
    ) -> tuple[MigratedRecordIds, dict, dict, dict]:
        identity_id = f"id:{record_id}"
        content_id = f"content:{record_id}"
        relationship_id = f"rel:{record_id}"
        identity = {k: record[k] for k in identity_fields if k in record}
        content = {k: record[k] for k in content_fields if k in record}
        relationship = {"identity_id": identity_id, "content_id": content_id, "relation": relation}
        return MigratedRecordIds(identity_id, content_id, relationship_id), identity, content, relationship


class LegacyGateway:
    """Converts a legacy application request into a bounded reconstruction request."""

    def make_request(
        self,
        ids: MigratedRecordIds,
        purpose: str,
        destination: str,
        recipient: str,
        permitted_fields: tuple[str, ...],
        boundary_id: str,
        relation: str = "belongs_to",
    ) -> ReconstructionRequest:
        return ReconstructionRequest(
            identity_id=ids.identity_id,
            content_id=ids.content_id,
            relationship_id=ids.relationship_id,
            purpose=purpose,
            destination=destination,
            recipient=recipient,
            permitted_fields=permitted_fields,
            permitted_associations=(AssociationRule(ids.identity_id, ids.content_id, relation),),
            output_boundary_id=boundary_id,
        )
