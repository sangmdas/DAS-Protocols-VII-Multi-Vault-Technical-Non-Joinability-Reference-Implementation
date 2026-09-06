from __future__ import annotations

import dataclasses
import os
import sys
import tempfile
import time
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from das_vii_multivault.authorization import ProtectedAuthorizationDomain, SessionRegistry
from das_vii_multivault.boundary import OutputReleaseBoundary
from das_vii_multivault.legacy import LegacyGateway, LegacyRecordAdapter
from das_vii_multivault.models import AssociationRule, ReconstructionRequest, SessionContext
from das_vii_multivault.output_finality import OutputDenied, OutputFinalityController
from das_vii_multivault.receipt_store import ProtectedReceiptStore
from das_vii_multivault.reconstruction import ProtectedReconstructionDomain, ReconstructionDenied
from das_vii_multivault.vaults import ProtectedVault, VaultCoordinator, VaultDenied


class MultiVaultTests(unittest.TestCase):
    def setUp(self):
        joined = {
            "name": "Alice Example",
            "email": "alice@example.test",
            "case_summary": "Battery overheated during evaluation",
            "future_program": "Project Aurora",
        }
        adapter = LegacyRecordAdapter()
        self.ids, identity, content, relationship = adapter.split_record(
            "case-77", joined, ("name", "email"), ("case_summary", "future_program")
        )
        self.sessions = SessionRegistry()
        self.session = SessionContext(
            session_id="sess-1",
            tenant_id="tenant-1",
            workload_id="ai-1",
            workload_measurement="sha256:workload-a",
            session_epoch=3,
            policy_epoch=9,
        )
        self.sessions.register(self.session)
        self.auth = ProtectedAuthorizationDomain(b"auth-secret", self.sessions)
        self.iv = ProtectedVault("identity-v", "identity", b"i-secret", {self.ids.identity_id: identity})
        self.cv = ProtectedVault("content-v", "content", b"c-secret", {self.ids.content_id: content})
        self.rv = ProtectedVault("relationship-v", "relationship", b"r-secret", {self.ids.relationship_id: relationship})
        self.coordinator = VaultCoordinator(self.iv, self.cv, self.rv)
        self.prd = ProtectedReconstructionDomain(self.coordinator, self.auth)
        self.gateway = LegacyGateway()
        self.request = self.gateway.make_request(
            self.ids,
            purpose="customer-support",
            destination="internal-ui",
            recipient="analyst",
            permitted_fields=("identity.name", "content.case_summary"),
            boundary_id="boundary-1",
        )
        self.rao = self.auth.issue(self.request, self.session)
        self.components = self.coordinator.release_required(self.rao, self.session, self.auth, parallel=False)
        self.view = self.prd.reconstruct(self.rao, self.session, self.components)
        self.store = ProtectedReceiptStore()
        self.controller = OutputFinalityController(b"out-auth", b"seal-secret", self.store, self.auth)
        self.boundary = OutputReleaseBoundary("boundary-1", self.controller, self.auth)

    def make_candidate(self):
        return self.controller.form_candidate(
            f"Case for {self.view.fields['identity.name']}: {self.view.fields['content.case_summary']}",
            used_fields=("identity.name", "content.case_summary"),
            used_associations=self.view.associations,
            view=self.view,
            rao=self.rao,
            session=self.session,
        )

    def authorize(self, candidate):
        return self.controller.verify_and_authorize(
            candidate,
            self.view,
            self.rao,
            self.session,
            current_destination="internal-ui",
            current_recipient="analyst",
            current_policy_epoch=9,
            current_session_epoch=3,
        )

    def release(self, candidate, receipt, cap, **kwargs):
        return self.boundary.release(
            candidate,
            receipt,
            cap,
            self.session,
            current_destination=kwargs.get("destination", "internal-ui"),
            current_recipient=kwargs.get("recipient", "analyst"),
            current_policy_epoch=kwargs.get("policy_epoch", 9),
            current_session_epoch=kwargs.get("session_epoch", 3),
        )

    def test_01_happy_path(self):
        candidate = self.make_candidate()
        receipt, cap = self.authorize(candidate)
        decision = self.release(candidate, receipt, cap)
        self.assertTrue(decision.allow)
        self.assertIn("Alice Example", decision.released_payload)

    def test_02_relationship_authority_is_required(self):
        with self.assertRaises(ReconstructionDenied):
            self.prd.reconstruct(self.rao, self.session, self.components[:2])

    def test_03_individually_accessible_fields_do_not_authorize_new_association(self):
        bad_request = ReconstructionRequest(
            identity_id=self.ids.identity_id,
            content_id=self.ids.content_id,
            relationship_id=self.ids.relationship_id,
            purpose="customer-support",
            destination="internal-ui",
            recipient="analyst",
            permitted_fields=("identity.name", "content.case_summary"),
            permitted_associations=(),
            output_boundary_id="boundary-1",
        )
        bad_rao = self.auth.issue(bad_request, self.session)
        with self.assertRaises(VaultDenied):
            self.coordinator.release_required(bad_rao, self.session, self.auth, parallel=False)

    def test_04_field_scope_is_enforced_at_vault(self):
        identity_component = next(c for c in self.components if c.vault_kind == "identity")
        content_component = next(c for c in self.components if c.vault_kind == "content")
        self.assertEqual(set(identity_component.data), {"name"})
        self.assertEqual(set(content_component.data), {"case_summary"})
        self.assertNotIn("future_program", content_component.data)

    def test_05_cross_session_component_reuse_denied(self):
        other = SessionContext("sess-2", "tenant-1", "ai-1", "sha256:workload-a", 3, 9)
        self.sessions.register(other)
        with self.assertRaises(Exception):
            self.prd.reconstruct(self.rao, other, self.components)

    def test_06_workload_measurement_change_denied(self):
        changed = SessionContext("sess-1", "tenant-1", "ai-1", "sha256:changed", 3, 9)
        with self.assertRaises(Exception):
            self.prd.reconstruct(self.rao, changed, self.components)

    def test_07_candidate_cannot_claim_field_not_in_view(self):
        with self.assertRaises(OutputDenied):
            self.controller.form_candidate(
                "leak",
                used_fields=("content.future_program",),
                used_associations=self.view.associations,
                view=self.view,
                rao=self.rao,
                session=self.session,
            )

    def test_08_output_capability_not_created_before_receipt_commit(self):
        class BrokenStore(ProtectedReceiptStore):
            def commit(self, receipt):
                raise RuntimeError("store unavailable")
        ctl = OutputFinalityController(b"out-auth", b"seal-secret", BrokenStore(), self.auth)
        candidate = ctl.form_candidate(
            "safe",
            used_fields=("identity.name",),
            used_associations=self.view.associations,
            view=self.view,
            rao=self.rao,
            session=self.session,
        )
        with self.assertRaises(RuntimeError):
            ctl.verify_and_authorize(candidate, self.view, self.rao, self.session, "internal-ui", "analyst", 9, 3)

    def test_09_destination_change_denied(self):
        candidate = self.make_candidate()
        receipt, cap = self.authorize(candidate)
        decision = self.release(candidate, receipt, cap, destination="attacker.example")
        self.assertFalse(decision.allow)
        self.assertEqual(decision.code, "MV_DESTINATION_MISMATCH")

    def test_10_replay_denied(self):
        candidate = self.make_candidate()
        receipt, cap = self.authorize(candidate)
        first = self.release(candidate, receipt, cap)
        second = self.release(candidate, receipt, cap)
        self.assertTrue(first.allow)
        self.assertFalse(second.allow)
        self.assertEqual(second.code, "MV_REPLAY")

    def test_11_output_mutation_denied(self):
        candidate = self.make_candidate()
        receipt, cap = self.authorize(candidate)
        mutated = dataclasses.replace(candidate, destination="other")
        decision = self.release(mutated, receipt, cap)
        self.assertFalse(decision.allow)
        self.assertEqual(decision.code, "MV_OUTPUT_MISMATCH")

    def test_12_policy_epoch_change_denied(self):
        candidate = self.make_candidate()
        receipt, cap = self.authorize(candidate)
        decision = self.release(candidate, receipt, cap, policy_epoch=10)
        self.assertFalse(decision.allow)
        self.assertEqual(decision.code, "MV_EPOCH_MISMATCH")

    def test_13_wrong_boundary_denied(self):
        candidate = self.make_candidate()
        receipt, cap = self.authorize(candidate)
        other_boundary = OutputReleaseBoundary("boundary-2", self.controller, self.auth)
        decision = other_boundary.release(candidate, receipt, cap, self.session, "internal-ui", "analyst", 9, 3)
        self.assertFalse(decision.allow)
        self.assertEqual(decision.code, "MV_BOUNDARY_MISMATCH")

    def test_14_poisoned_session_fails_closed(self):
        self.sessions.poison("sess-1", "partial workflow failed")
        with self.assertRaises(Exception):
            self.coordinator.release_required(self.rao, self.session, self.auth, parallel=False)

    def test_15_legacy_adapter_decomposes_joined_record(self):
        self.assertNotEqual(self.ids.identity_id, self.ids.content_id)
        self.assertNotEqual(self.ids.relationship_id, self.ids.content_id)
        self.assertEqual(self.view.fields["identity.name"], "Alice Example")
        self.assertNotIn("content.future_program", self.view.fields)

    def test_16_parallel_and_sequential_release_are_equivalent_in_scope(self):
        parallel = self.coordinator.release_required(self.rao, self.session, self.auth, parallel=True)
        seq_kinds = {c.vault_kind: c.data for c in self.components}
        par_kinds = {c.vault_kind: c.data for c in parallel}
        self.assertEqual(seq_kinds, par_kinds)


if __name__ == "__main__":
    unittest.main()
