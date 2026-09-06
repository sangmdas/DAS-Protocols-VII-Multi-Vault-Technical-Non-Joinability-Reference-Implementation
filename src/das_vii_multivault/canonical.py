from __future__ import annotations

import dataclasses
import hashlib
import json
from enum import Enum
from typing import Any


def _primitive(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {f.name: _primitive(getattr(value, f.name)) for f in dataclasses.fields(value)}
    if isinstance(value, dict):
        return {str(k): _primitive(v) for k, v in sorted(value.items(), key=lambda kv: str(kv[0]))}
    if isinstance(value, (tuple, list)):
        return [_primitive(v) for v in value]
    if isinstance(value, set):
        return sorted(_primitive(v) for v in value)
    if isinstance(value, Enum):
        return value.value
    return value


def canonical_bytes(value: Any) -> bytes:
    """Deterministic JSON for this reference implementation.

    This is NOT claimed to be RFC 8785/JCS. Production protocols should specify
    a canonicalization format explicitly and test it cross-language.
    """
    return json.dumps(
        _primitive(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def sha256_hex(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()
