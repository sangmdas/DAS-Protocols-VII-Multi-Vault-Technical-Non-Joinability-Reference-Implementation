from __future__ import annotations

import base64
import hashlib
import hmac
import os
from dataclasses import replace
from typing import Any

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from .canonical import canonical_bytes


def hmac_sign(secret: bytes, value: Any) -> str:
    return hmac.new(secret, canonical_bytes(value), hashlib.sha256).hexdigest()


def hmac_verify(secret: bytes, value: Any, signature: str) -> bool:
    expected = hmac_sign(secret, value)
    return hmac.compare_digest(expected, signature)


def without_signature(obj: Any) -> Any:
    if hasattr(obj, "signature"):
        return replace(obj, signature="")
    return obj


class AeadBox:
    """Small AES-GCM wrapper used only to make Candidate Output opaque to callers.

    Production deployments should use a real protected key boundary (TEE/HSM/KMS,
    destination-held key, etc.) and formal key lifecycle management.
    """

    def __init__(self, secret: bytes):
        self._key = hashlib.sha256(b"das-vii-output-seal:" + secret).digest()
        self._aes = AESGCM(self._key)

    def seal(self, plaintext: bytes, aad: bytes) -> tuple[str, str]:
        nonce = os.urandom(12)
        ct = self._aes.encrypt(nonce, plaintext, aad)
        return base64.b64encode(nonce).decode(), base64.b64encode(ct).decode()

    def open(self, nonce_b64: str, ciphertext_b64: str, aad: bytes) -> bytes:
        nonce = base64.b64decode(nonce_b64)
        ct = base64.b64decode(ciphertext_b64)
        return self._aes.decrypt(nonce, ct, aad)
