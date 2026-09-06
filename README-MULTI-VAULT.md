# Multi-Vault AI Non-Joinability
## Runnable Reference Implementation for Enterprise-AI Technical Non-Joinability and Output Finality

**Version:** v0.1.0  
**Status:** Research / evaluation / standards-review reference implementation  
**License:** Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)  
**Production status:** Not production security software

---

## 1. Overview

This repository contains a runnable reference implementation of a **multi-vault security architecture for enterprise artificial intelligence**.

The implementation demonstrates a technical separation between:

- authority to access identity information;
- authority to access substantive content;
- authority to establish the relationship between identity and content;
- authority to reconstruct a purpose-limited semantic view;
- authority to compute over that reconstructed view; and
- authority to make an AI-generated result externally usable or externally effective.

The central security principle is:

> **Access is not association authority. Association is not unrestricted reconstruction authority. Reconstruction and computation are not output authority.**

The architecture is intended to reduce the risk that compromise of one AI workload, application server, agent runtime, or ordinary credential automatically gives an attacker the ability to reconstruct a complete semantic model of an enterprise and then externalize the resulting intelligence.

This repository is a **reference implementation of architectural relationships and state transitions**. It is not a claim that the included Python process provides production-grade isolation between independent trust domains.

---

## 2. Why This Problem Is Different in the AI Era

A conventional server breach may expose a defined collection of stored data such as:

- names;
- email addresses;
- telephone numbers;
- documents;
- transactions;
- account records; or
- previously stored communications.

A sufficiently connected AI workload creates a broader threat.

An enterprise AI system may simultaneously interact with:

- customer systems;
- internal communications;
- product-development repositories;
- engineering records;
- source-code systems;
- vector stores;
- financial platforms;
- supplier information;
- research repositories;
- operational databases;
- retrieval systems;
- agent memory; and
- external tools or services.

If that AI workload is compromised, the attacker may attempt not merely to copy stored records, but to **correlate otherwise separate information and infer relationships or future organizational direction**.

For example:

```text
customer complaints
        +
engineering discussions
        +
source-code changes
        +
supplier information
        +
financial allocations
        +
research activity
        ↓
AI correlation / inference
        ↓
reconstructed strategic intelligence
```

The sensitive output may never have existed as one stored document.

A file called `future_strategy.pdf` may not exist anywhere. Yet an AI system with broad access could potentially reconstruct information concerning future products, research priorities, important customer relationships, supplier dependencies, pricing intentions, investment direction, operational weaknesses, or other commercially sensitive relationships.

The security question therefore changes from:

> **Can the attacker read this database?**

to:

> **Can compromise of one AI workload give the attacker authority to join independently protected information, reconstruct relationships that were never stored together, infer protected intelligence, and externalize the result?**

This reference implementation focuses on that second problem.

---

## 3. What Makes This More Than “Several Databases”

Simply dividing a database into multiple tables, services, shards, or storage locations does not create Technical Non-Joinability.

If one administrator, application credential, query engine, application server, or common control plane can freely recombine all of the separated values, the architecture remains practically joinable.

This reference model therefore treats the **relationship required to associate identity with content as independently controlled authority**.

Conceptually:

```text
Identity Vault
      +
Content Vault
      +
Relationship-Mapping Vault
      ↓
protected reconstruction authorization
      ↓
session-bound component release
      ↓
Protected Reconstruction Domain
      ↓
ephemeral minimum-necessary view
```

Possession of identity data and content data does not automatically provide permission to establish the semantic relationship between them.

---

## 4. Core Architecture

The reference workflow is:

```text
Identity Vault
        +
Content Vault
        +
Independent Relationship-Mapping Vault
        ↓
Reconstruction Authorization Object (RAO)
        ↓
Independent Vault-Local Release Decisions
        ↓
Session-Bound Components
        ↓
Protected Reconstruction Domain
        ↓
Ephemeral Minimum-Necessary Data View
        ↓
Protected Provenance / Association Continuity
        ↓
AI Processing
        ↓
Candidate Output
        ↓
Sealed Candidate Output
        ↓
Live Output Verification
        ↓
Protected Output Validation Receipt (POVR)
        ↓
Output Release Capability
        ↓
Output Release Boundary
        ↓
Externally Usable Result
```

The implementation is deliberately different from a normal tool-invocation authorization wrapper.

Its core question is not only:

> “May this tool call execute?”

It first asks:

> **“May these independently protected pieces of information be associated and reconstructed in this way, for this purpose, in this session, by this workload?”**

Only after that does the architecture separately determine whether an AI-derived output may be released.

---

## 5. Independent Vault Roles

### 5.1 Identity Vault

The Identity Vault maintains or resolves protected identity components.

Examples may include:

- person references;
- organization references;
- account references;
- device references;
- customer references;
- employee references; or
- other protected identity attributes.

Identity access does not by itself authorize association with substantive content.

### 5.2 Content Vault

The Content Vault maintains substantive protected information.

Examples may include:

- support records;
- technical documents;
- research data;
- engineering information;
- commercial information;
- operational records;
- transaction data; or
- other enterprise content.

Content access does not by itself reveal or authorize the identity relationship.

### 5.3 Relationship-Mapping Vault

The Relationship-Mapping Vault independently controls the information or authority required to associate selected identity components with selected content components.

This is a load-bearing distinction.

The Relationship-Mapping Vault is **not merely another database table**. It represents independent control over the semantic relationship that makes separately held components meaningful when combined.

---

## 6. Reconstruction Authorization Object (RAO)

A Reconstruction Authorization Object represents protected reconstruction authority for a specific context.

A reference RAO may bind one or more of:

- session identifier;
- Session Epoch;
- Policy Epoch;
- workload identity or measurement;
- permitted field set;
- **Permitted Association Scope**;
- authorized processing purpose;
- destination;
- recipient;
- validity period;
- use count;
- disclosure limits;
- output conditions;
- reconstruction-domain identity; and
- other protected state.

The RAO is intended to be **non-bearer in effect**: possession of a serialized object alone should not be sufficient to exercise reconstruction authority outside its bound protected context.

---

## 7. Permitted Association Scope

A central concept in this implementation is that **field permission and association permission are different**.

For example:

```text
Customer identity                 permitted
Product defect record             permitted
Customer ↔ defect association     not permitted
```

An application may be permitted to access both underlying values while still being prohibited from creating, persisting, or externalizing the relationship between them.

The Permitted Association Scope therefore governs which semantic relationships may be formed during reconstruction.

---

## 8. Independent Vault-Local Release

Each required vault evaluates release independently.

Release by one vault does not force release by another.

Conceptually:

```text
                         ┌─ Identity Vault ──────────┐
                         │                           │
RAO + protected session ├─ Content Vault ───────────┼─> Reconstruction
                         │                           │
                         └─ Relationship Vault ──────┘
```

Where any required vault:

- denies;
- returns stale state;
- produces unverifiable state;
- detects a session mismatch;
- detects a policy mismatch; or
- cannot satisfy a required condition,

reconstruction fails closed.

---

## 9. Session-Bound Components

Approved vault outputs do not become unrestricted reusable bearer data merely because a vault released them once.

Released components are bound to the authorized reconstruction session.

The implementation rejects misuse such as:

- replay in another session;
- mixing components from different sessions;
- reusing stale components after an epoch change;
- using components with a different workload context; or
- reassociating components outside the authorized mediation path.

---

## 10. Protected Reconstruction Domain

The Protected Reconstruction Domain receives only authorized Session-Bound Components and required protected release state.

It then:

1. verifies component/session correspondence;
2. applies the permitted field set;
3. applies the Permitted Association Scope;
4. excludes unauthorized fields;
5. excludes unauthorized associations;
6. maintains provenance;
7. reconstructs only the minimum necessary semantic view; and
8. prevents the reconstructed view from becoming an unrestricted permanent joined record.

The result is an:

**Ephemeral Minimum-Necessary Data View**

rather than a universal enterprise profile.

---

## 11. Ephemeral Minimum-Necessary Reconstruction

The reconstructed representation may contain only what is needed for the authorized purpose.

Examples include:

- selected fields;
- a redacted record;
- a structured query result;
- a protected graph;
- an embedding;
- an aggregate;
- a feature representation;
- a model-readable derivative; or
- another purpose-limited representation.

Successful reconstruction does **not** create authority to export the reconstructed view or any derived output.

---

## 12. Provenance and Association Continuity

The architecture maintains provenance across protected processing.

Provenance may associate AI-derived information with:

- source components;
- source vaults;
- permitted fields;
- permitted associations;
- transformation steps;
- intermediate values;
- generated fragments;
- output portions; and
- authorization state.

This allows output verification to evaluate not only whether a field appears in a Candidate Output, but whether the output reconstructs, reveals, transforms, or indirectly exposes an association that the session was not authorized to externalize.

---

## 13. Candidate Output and Technical Non-Completability

AI computation does not itself create release authority.

The workload may generate:

- text;
- structured data;
- an API request;
- a database update;
- a message;
- a report;
- an embedding;
- a financial instruction;
- a tool request; or
- another consequence-bearing artifact.

That artifact is treated as a **Candidate Output**.

Before the output becomes available through an unprotected path, it is converted into a **Sealed Candidate Output** or otherwise kept Non-Releasable.

The central invariant is:

> **Generation may complete while the external output path remains technically incomplete.**

This is the reference implementation's demonstration of **Technical Non-Completability**.

---

## 14. Live Output Verification

Authorization obtained during reconstruction is not treated as permanent authority for later output release.

Before release, the system can re-establish current state including:

- session validity;
- Session Epoch;
- Policy Epoch;
- workload correspondence;
- destination;
- recipient;
- provenance;
- output digest;
- association scope;
- output scope;
- revocation state; and
- Output Release Boundary identity.

A change in a load-bearing condition causes denial or requires fresh authorization.

---

## 15. Protected Output Validation Receipt (POVR)

After successful output verification, the implementation creates a protected validation receipt.

The POVR may bind:

- verified output digest;
- RAO digest;
- session;
- epoch;
- provenance state;
- destination;
- recipient;
- output scope;
- boundary identity; and
- current protected state.

The reference flow demonstrates a **commit-before-capability** relationship.

A release capability is not created merely because output verification code returned `True`.

Required protected receipt state must first be committed.

---

## 16. Output Release Capability

The Output Release Capability represents narrow authority for a specific verified output.

It is not intended to act as a general-purpose bearer credential.

It may be bound to:

- exact output digest;
- POVR digest;
- session;
- Session Epoch;
- destination;
- recipient;
- Output Release Boundary;
- expiration;
- one-time state; and
- current protected conditions.

Changing the output, destination, boundary, session, or other load-bearing state invalidates the authority.

---

## 17. Output Release Boundary

The Output Release Boundary controls the first point at which the verified result becomes externally usable or externally effective.

The boundary independently checks the required correspondence before release.

A Candidate Output therefore cannot become externally usable merely because:

- the AI generated it;
- the application possesses it;
- an upstream verifier approved something earlier; or
- an ordinary application credential is valid.

The exact protected output path must complete.

---

## 18. Two Complementary Security Properties

### Technical Non-Joinability

Prevents unauthorized creation of a complete semantic enterprise representation from independently protected components.

### Technical Non-Completability

Prevents an AI-generated result from automatically becoming an externally effective consequence.

Together:

```text
unauthorized joining
        ↓ prevented

authorized minimum reconstruction
        ↓
AI computation
        ↓
Candidate Output
        ↓
unauthorized externalization
        ↓ prevented
```

---

## 19. Threat Model Demonstrated by the Reference

The automated tests include scenarios intended to demonstrate failure of release or reconstruction when conditions such as the following occur:

- relationship authority is missing;
- an association is outside permitted scope;
- components belong to another session;
- workload measurement changes;
- policy epoch changes;
- candidate output is modified after verification;
- destination is substituted;
- Output Release Boundary is changed;
- required POVR commitment is missing;
- an Output Release Capability is replayed;
- a session is poisoned;
- stale authority is reused; or
- required protected state is inconsistent.

The implementation is intended to show that **no single ordinary application decision is sufficient to complete the entire chain**.

---

## 20. Latency Design

A multi-vault architecture can be implemented badly.

A naive design could perform every vault lookup, policy evaluation, attestation operation, cryptographic transformation, provenance operation, and output check serially on every inference step.

That is not the intended architecture.

### Cold Path

The cold path may prepare:

- compiled policy predicates;
- permitted-association graphs;
- protected identity indices;
- registered workload measurements;
- destination manifests;
- attestation collateral;
- protected revocation snapshots;
- disclosure rules;
- provenance schemas; and
- other bounded protected precomputation.

### Hot Path

The hot path retains only current load-bearing checks such as:

- current session;
- current epoch;
- bounded-freshness or live attestation;
- current revocation;
- association scope;
- current provenance;
- destination;
- recipient;
- receipt commitment;
- output capability; and
- boundary verification.

### Parallel Vault Fan-Out

Independent vault-local decisions do not inherently need to execute serially.

Production architectures may request required vault decisions concurrently.

The security requirement is **independent decision authority**, not artificial serialization.

---

## 21. Benchmarking

The repository includes a local benchmark intended to characterize the reference implementation.

Reference benchmark numbers must **not** be interpreted as production latency guarantees.

The local benchmark excludes, among other things:

- real network RPC;
- geographic separation;
- external KMS/HSM calls;
- hardware attestation;
- distributed consensus;
- production database latency;
- AI-model inference;
- human approval;
- cloud-service scheduling;
- remote logging; and
- real external effectuation.

Performance depends on deployment topology and trust-boundary placement.

---

## 22. Legacy-System Integration

The architecture does not require every enterprise to replace all existing:

- databases;
- AI models;
- applications;
- API frameworks;
- identity infrastructure; or
- network services.

A mandatory mediation layer may be introduced through:

- database proxies;
- data-access gateways;
- service-mesh sidecars;
- API gateways;
- storage filters;
- retrieval proxies;
- operating-system brokers;
- message brokers;
- model-serving wrappers;
- tool-execution brokers;
- secure output adapters;
- database commit interceptors;
- file-system filters; or
- network-egress controllers.

The legacy application can continue using familiar interfaces while the surrounding protected control plane performs reconstruction authorization, vault mediation, provenance, sealing, and output finality.

---

## 23. Incremental Migration of Existing Databases

A legacy database containing complete joined records does not necessarily need to be decomposed in one migration event.

A staged approach may include:

1. place newly created records into separated protected domains;
2. decompose old records when first accessed;
3. separate high-sensitivity relationship mappings first;
4. tokenize identity fields while substantive content temporarily remains in the legacy store;
5. introduce a protected Relationship-Mapping Vault for opaque reference resolution;
6. place a mandatory gateway in front of unrestricted joins; and
7. progressively reduce the legacy system to opaque references or permitted derivatives.

Incomplete migration must not increase authority.

Ambiguous or partially migrated state should be handled conservatively.

---

## 24. Non-Bypassability Requirement

Legacy compatibility does not mean leaving an unrestricted old path open.

If a compromised workload can still:

- query the original joined database directly;
- use a cached credential;
- call an unmediated API;
- use a debugging endpoint;
- bypass the Relationship-Mapping Vault;
- write the Candidate Output directly to a file;
- send it through another messaging path; or
- exfiltrate it through an uncontrolled network interface,

the protected architecture has been bypassed.

A production deployment must therefore close alternate paths to protected reconstruction and external release.

---

## 25. What This Reference Implementation Does Not Prove

This repository is intentionally a **reference implementation**, not a production security certification.

The current implementation does **not** prove:

- isolation against a fully compromised host process;
- independent hardware trust domains;
- TEE/HSM security;
- resistance to arbitrary side channels;
- formal non-interference;
- elimination of covert channels;
- complete semantic leakage detection;
- secure distributed consensus;
- production-grade remote attestation;
- production-grade key lifecycle management;
- regulatory compliance;
- legal compliance;
- security against collusion of all relevant authorities; or
- universal prevention of AI inference attacks.

The example vaults are logically separated software components. If they are hosted inside one ordinary Python process, full compromise of that process can defeat those logical boundaries.

Production deployment would require trust boundaries appropriate to the threat model.

---

## 26. Production Hardening Considerations

A production-grade implementation may require:

- independent protected services or machines for vault roles;
- mutually authenticated service-to-service communication;
- asymmetric cryptographic signatures;
- HSM-backed or hardware-protected keys;
- confidential-computing environments;
- remote attestation;
- protected monotonic state;
- rollback-resistant receipt stores;
- high-availability fail-closed design;
- distributed authorization quorums;
- bounded-freshness policy and revocation state;
- strong audit and monitoring;
- formal state-machine analysis;
- information-flow analysis;
- destination-side verification;
- alternate-path closure; and
- deployment-specific incident recovery.

None of these should be assumed merely because the local reference implementation runs successfully.

---

## 27. Repository Layout

A typical repository layout may include:

```text
.
├── README.md
├── LICENSE.md
├── NOTICE.md
├── LATENCY_AND_LEGACY.md
├── pyproject.toml
├── src/
│   └── das_vii_multivault/
├── tests/
├── bench/
└── examples/
```

See the actual repository tree for the authoritative current layout.

---

## 28. Installation

Python 3.11+ is recommended for the reference implementation.

Example:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
```

---

## 29. Running the Test Suite

```bash
python -m unittest discover -s tests -v
```

The test suite is intended to cover both the permitted path and important fail-closed cases.

A successful reference run should complete without test failures.

---

## 30. Running the Demonstration

Where the package includes the module entry point:

```bash
python -m das_vii_multivault.demo
```

The demo is intended to show the protected sequence from reconstruction authorization through vault-local release, protected reconstruction, Candidate Output formation, protected receipt commitment, capability creation, and final release.

---

## 31. Running the Benchmark

```bash
python bench/benchmark.py
```

Benchmark output is for local engineering characterization only.

Do not present local benchmark results as claims about:

- production deployment;
- remote multi-vault systems;
- HSMs;
- confidential-computing infrastructure;
- distributed systems;
- cloud latency;
- model inference; or
- regulatory performance requirements.

---

## 32. Relationship to Agentic Tool-Call Execution Finality

This repository addresses a different problem from a conventional agentic tool-call execution gate.

A tool-call finality implementation primarily asks:

> **May this exact proposed action become externally effective?**

This multi-vault architecture asks an earlier question:

> **May these independently controlled data components be semantically associated and reconstructed in the first place?**

It then adds a second finality question:

> **May the AI-derived output from that reconstruction become externally usable?**

The architectures can be complementary, but they should not be collapsed into one concept.

---

## 33. Research and Standards Use

This repository is intended to support:

- technical evaluation;
- academic research;
- architecture discussion;
- interoperability analysis;
- standards review;
- benchmarking;
- security analysis;
- proof-of-concept development; and
- non-commercial experimentation,

subject to the license terms below.

---

# License

## 34. Creative Commons Attribution-NonCommercial 4.0 International

Except where otherwise expressly stated, the copyrightable material in this repository is licensed under:

**Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**

Official license information:

https://creativecommons.org/licenses/by-nc/4.0/

Legal code:

https://creativecommons.org/licenses/by-nc/4.0/legalcode

### You are free to

Subject to the license terms, users may:

- **Share** — copy and redistribute the material in any medium or format; and
- **Adapt** — remix, transform, and build upon the material.

### Under the following terms

#### Attribution

Appropriate credit must be given, a link to the license must be provided, and changes must be indicated.

Attribution should not suggest endorsement by the inventor or author.

A suggested attribution is:

> **Multi-Vault AI Non-Joinability Reference Implementation, Sangam Kumar Das, licensed under CC BY-NC 4.0 International.**

Where practical, attribution should also identify the relevant repository or release version.

#### NonCommercial

The material may not be used for **commercial purposes** as that term is defined by the CC BY-NC 4.0 license.

Users evaluating whether a particular activity is commercial or non-commercial should rely on the actual license text and obtain appropriate legal advice where necessary.

#### No additional restrictions

Users may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

---

## 35. Important Patent-Rights Notice

**CC BY-NC 4.0 is a copyright license. It does not grant patent rights.**

Patent rights, patent applications, inventions, implementations, claims, methods, systems, architectures, and other patent-related rights associated with the disclosed technology are **not licensed merely because source code, documentation, test vectors, diagrams, examples, or other materials are made available under CC BY-NC 4.0**.

No patent license is granted by this repository unless a separate written patent license expressly states otherwise.

Nothing in this repository should be interpreted as:

- a patent licence;
- a covenant not to sue;
- a waiver of patent rights;
- an exhaustion of patent rights beyond what applicable law independently requires;
- permission for commercial implementation of patented subject matter; or
- an assurance of freedom to operate.

Persons or organizations considering commercial implementation should separately evaluate applicable patent rights and obtain any required patent licence.

---

## 36. Trademarks

No trademark rights are granted.

Names of third-party products, protocols, companies, standards, or technologies may be used solely for identification, interoperability discussion, technical explanation, or comparative reference.

Such references do not imply sponsorship, affiliation, endorsement, or approval.

---

## 37. No Endorsement

Publication of this implementation does not imply endorsement by:

- any standards organization;
- any governmental authority;
- any regulator;
- any AI provider;
- any cloud provider;
- any telecommunications provider;
- any financial institution;
- any hardware manufacturer; or
- any other third party.

---

## 38. No Warranty

The material is provided for research, evaluation, and technical discussion.

To the extent permitted by applicable law, it is provided **“AS IS” and “AS AVAILABLE,” without warranties or conditions of any kind**, whether express, implied, statutory, or otherwise.

The authors and contributors do not warrant that the implementation is:

- secure;
- error free;
- suitable for production deployment;
- compliant with any law or regulation;
- fit for a particular purpose;
- interoperable with every system;
- resistant to every attack; or
- free of third-party rights.

Users are responsible for independent security review, legal review, testing, and deployment decisions.

---

## 39. Security Notice

Do not deploy this reference implementation as the sole protection for:

- production secrets;
- critical infrastructure;
- defence systems;
- financial settlement;
- medical systems;
- safety-critical control;
- personal data;
- regulated workloads; or
- other high-impact environments

without appropriate production engineering, independent security review, hardware/software trust design, cryptographic key management, monitoring, incident response, and fail-safe/fail-closed controls.

---

## 40. Contributions

Contributions, issues, technical critiques, test cases, interoperability experiments, and security analysis may be welcomed subject to the repository's contribution process.

Submission of a contribution does not automatically alter:

- the repository's copyright licence;
- patent ownership;
- patent-licensing obligations;
- inventorship;
- standards-body IPR obligations; or
- third-party rights.

Contributors should ensure that they have the right to submit their contribution.

Where contributions may be relevant to a standards process, applicable standards-body intellectual-property policies should be reviewed independently.

---

## 41. Citation

Suggested citation:

**Sangam Kumar Das. “Multi-Vault AI Non-Joinability: Runnable Reference Implementation for Technical Non-Joinability, Protected Semantic Reconstruction, and Output Finality.” v0.1.0.**

Where a DOI or archival record is available, use that record in formal citations.

---

## 42. Final Architectural Summary

The implementation demonstrates the following proposition:

```text
Access
  ≠
Association Authority

Association Authority
  ≠
Unrestricted Reconstruction

Reconstruction
  ≠
Externalization Authority

AI Computation
  ≠
Release Authority
```

The objective is not to assume that an AI workload can never be compromised.

The objective is to prevent compromise of one workload from automatically becoming complete authority to:

1. obtain all protected components;
2. join identity and content without independent relationship authority;
3. reconstruct an unrestricted semantic enterprise profile;
4. persist or reuse that reconstruction outside its authorized session;
5. convert AI inference into an automatically releasable output; and
6. make that result externally usable without independent final verification.

**Computation may produce information. It does not, by itself, create authority to reconstruct or release it.**
