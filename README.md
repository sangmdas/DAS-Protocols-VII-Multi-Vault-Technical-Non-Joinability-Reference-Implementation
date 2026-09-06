# DAS Protocols VII — Multi-Vault Technical Non-Joinability Reference Implementation

**Runnable reference implementation — v0.1.0**

This repository demonstrates the distinct DAS Protocols VII architecture for **Technical Non-Joinability and Technical Non-Completability in enterprise AI**.

It is deliberately **not** the ordinary agent-tool invocation / MCP wrapper architecture. The load-bearing problem here is earlier and broader:

> Access to identity is not authority to associate identity with content. Access to content is not relationship authority. Successful reconstruction is not output authority. Successful computation is not release authority.

## Implemented chain

```text
legacy joined record / protected sources
        ↓
independent semantic domains
  Identity Vault
  Content Vault
  Relationship-Mapping Vault
        ↓
Reconstruction Authorization Object (RAO)
        ↓
independent Vault-Local Release Conditions
        ↓
Session-Bound Components
        ↓
Protected Reconstruction Domain
        ↓
Ephemeral Minimum-Necessary Data View
        ↓
provenance / association continuity
        ↓
AI computation (synthetic in this repo)
        ↓
Sealed Candidate Output
        ↓
live output verification
        ↓
Protected Output Validation Receipt (POVR) committed
        ↓
Output Release Capability formed
        ↓
Output Release Boundary verifies and consumes once
        ↓
external release
```

## What the code demonstrates

- **Independent semantic authority.** Identity, content, and the mapping needed to join them are held by different vault objects with separate signing secrets.
- **Permitted Association Scope.** Possession of identity and content components does not authorize a relationship. The relationship vault must independently release the association permitted by the RAO.
- **Non-bearer reconstruction authorization.** A valid RAO is not enough by possession: current session, workload measurement, session epoch, policy epoch, record identity, and vault-local conditions must still correspond.
- **Vault-local release.** Each vault independently projects only fields it is authorized to release.
- **Session-bound components.** Released values carry RAO, session, epoch, workload, expiry, and vault-local integrity bindings.
- **Scope-limited reconstruction.** The Protected Reconstruction Domain requires all three semantic domains, validates component correspondence, applies the field set and association scope, and creates an ephemeral view rather than a durable unrestricted joined record.
- **Provenance continuity.** The reconstructed view retains field-to-vault/source provenance and a protected association provenance digest.
- **Sealed Candidate Output.** Candidate output is AES-GCM sealed before release authority exists.
- **Constitutive POVR.** The output validation receipt is committed to the local receipt store before an Output Release Capability can be created.
- **Boundary-specific, one-time release.** Output Release Capability is bound to candidate digest, receipt, session, epochs, destination, recipient, and Output Release Boundary, then atomically consumed on release.
- **Fail closed.** Missing relationship authority, missing vault release, stale session, changed workload, changed destination, changed epoch, uncommitted receipt, wrong boundary, mutation, or replay denies the operation.
- **Parallel vault fan-out.** Required vault-local releases can be issued concurrently for network-bound deployments.
- **Legacy migration adapter.** A joined legacy record can be split into identity, content, and relationship domains and reached through a legacy gateway that generates bounded reconstruction requests.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e .
python -m unittest discover -s tests -v
python -m das_vii_multivault.demo
python bench/benchmark.py
```

Expected test result for v0.1.0:

```text
Ran 16 tests
OK
```

## Test coverage

The suite covers:

1. authorized multi-vault reconstruction and output release;
2. relationship vault required even where identity/content are available;
3. unauthorized semantic association denied;
4. vault-local field projection;
5. cross-session component reuse denied;
6. changed workload measurement denied;
7. Candidate Output cannot claim unreconstructed fields;
8. no Output Release Capability if POVR commitment fails;
9. destination substitution denied;
10. single-use replay denied;
11. Candidate Output mutation denied;
12. policy-epoch change denied;
13. wrong Output Release Boundary denied;
14. poisoned session fails closed;
15. legacy joined-record decomposition; and
16. parallel vs sequential vault release preserves the same scope.

## Latency and legacy integration

See [`LATENCY_AND_LEGACY.md`](LATENCY_AND_LEGACY.md).

The local benchmark intentionally does **not** claim that a distributed multi-vault production deployment will have the same latency. In the included reference run, the complete local protected path had a median of approximately **2.38 ms**, but that excludes network RPC, remote attestation, HSM/KMS, distributed commit, AI inference, and production observability. The architectural response to multi-vault latency is cold-path preparation, concurrent vault-local release, minimum-necessary reconstruction, compact hot-path verification, and incremental legacy mediation—not pretending that independent protection domains are free.

## Legacy migration invariant

The adapter is a migration demonstration, not bypass closure. A production deployment must make the mediation path mandatory. If the original joined database, raw vault credential, debug endpoint, alternate API, or ungoverned output channel remains reachable by the workload, Technical Non-Joinability / Technical Non-Completability is not established for that path.

## Red-mode limitations

This repository is an executable architectural reference, **not proof of production security**.

- The three vaults are Python objects in one process. Separate secrets demonstrate independent release decisions, but they do not provide process, machine, administrator, or hardware isolation. If the Python process is fully compromised, the reference boundary can be bypassed.
- HMAC is used for compact local integrity. Production multi-authority deployments should use appropriate asymmetric signatures, attestation, PKI, HSM/TEE/KMS, threshold mechanisms, or other protected-domain primitives.
- AES-GCM sealing makes the Candidate Output opaque in the reference API, but the sealing key still exists in the same process. This is not equivalent to a non-exportable destination key or hardware output boundary.
- SQLite demonstrates commit-before-capability and atomic consume-once state locally. It is not a rollback-resistant hardware journal, distributed transaction protocol, or atomic commit with an arbitrary remote side effect.
- The provenance model is structured. The implementation does not solve general semantic provenance, model-internal information flow, covert channels, paraphrased leakage, embeddings leakage, or inferred association detection.
- Permitted Association Scope is implemented with exact structured association rules. Graph policies, inference-channel budgets, quantitative disclosure budgets, k-anonymity, multi-authority quorum, and semantic similarity controls are not implemented in v0.1.0.
- Remote attestation and live revocation infrastructure are represented by workload measurement and epoch bindings, not by a production attestation verifier.
- Parallel vault fan-out uses local threads. It demonstrates the orchestration shape, not distributed-RPC performance or fault tolerance.
- The legacy adapter does not delete the original joined record. A real migration must prevent direct access to the old join path.
- The reference does not prove universal alternate-path closure. Production assurance depends on controlling every path capable of reconstructing protected relationships or externalizing protected output.
- The reference makes no determination of GDPR, EU AI Act, sectoral, contractual, or other legal compliance.

## Design distinction from DAS Protocols IX / tool-call finality

The separate agentic-tool reference implementation focuses on **whether a concrete tool call may be invoked**. This repository focuses on **whether independently protected identity, content, and relationship information may be joined into a semantically usable representation at all, and whether an AI-derived result from that reconstruction may leave the protected path**.

The two architectures can be combined, but they are not the same reference profile.

## Synthetic data

All records, identities, destinations, measurements, secrets, and outputs in this repository are synthetic. No live enterprise data or production credentials are included.
