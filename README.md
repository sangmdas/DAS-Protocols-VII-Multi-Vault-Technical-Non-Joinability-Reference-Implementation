# DAS Protocols VII — Multi-Vault Technical Non-Joinability and Output-Finality Reference Implementation

## Runnable reference implementation — v0.1.0

#### This repository provides an executable reference implementation of selected technical mechanisms disclosed in DAS Protocols VII — “Architecting Resilience for Enterprise AI: Preventing Data Reconstruction, Exfiltration, and Unauthorized Consequence in Compromised AI Environments.”

### Why this matters

A conventional cyber breach steals what already exists. An AI-era breach can reconstruct what does not yet exist as a document at all: an individual’s, enterprise’s, or government’s probable future.

Imagine that I am the CEO of a billion-dollar company and use an AI assistant every day. It helps me evaluate acquisition targets, compare competitors, review financial scenarios, assess suppliers, prepare board material, explore future products, analyse regulatory exposure, and develop technical ideas that may later become patent applications.

Over time, that AI assistant may know more about the direction of the company than any single document does.

If an attacker steals one file, the attacker gets that file.

If the attacker compromises the AI environment through which I work, the attacker may instead ask:

“Based on everything this person has been working on, what is this company likely to do next?”

The answer may never have existed as a stored document.

There may be no file called “Acquisitions We Will Announce Next Year.pdf.”

There may be no database row called “Future Product Roadmap.”

There may be no memorandum saying “This is the technology we intend to patent six months from now.”

But the ingredients may already exist separately across email, financial models, meeting notes, product discussions, supplier conversations, technical experiments, search history, draft patent material, market analysis, and everyday AI interactions.

A capable AI may correlate those fragments and reconstruct that the company is considering acquiring a particular business, entering a new market, replacing a supplier, abandoning a product, preparing a regulatory strategy, developing an unannounced technology, or forming an idea that may become the subject of a future patent filing.

The attacker has not merely stolen data. The attacker has reconstructed strategy.

The same problem becomes even more serious for a senior government official.

A day-to-day AI assistant may encounter fragments concerning diplomatic meetings, sanctions options, trade negotiations, alliance priorities, defence assessments, procurement concerns, draft speeches, internal disagreements, economic analysis, and policy options.

No single record may say:

“This is our next foreign-policy move toward Country X or Group Y.”

Yet the combination of those fragments may reveal whether relations are likely to harden or soften, whether sanctions are being considered, which alliance may receive closer cooperation, which diplomatic concession may be offered, or what strategic position the government is preparing to adopt.

There may be no document called “Our Next Foreign Policy Toward Country X.”

The future policy may exist only as a relationship among information distributed across many systems.

If that AI environment is compromised, the attacker may not simply learn what the government already knows.

The attacker may reconstruct what the government is preparing to do.

This is the core problem addressed by this repository.

AI is increasingly becoming a day-to-day cognitive assistant. People do not use it only to process finished documents. They use it while thinking through unfinished decisions.

That changes the security question from:

What information can this workload access?

to:

What relationships is this workload authorized to form between independently protected information?

and ultimately:

What reconstructed knowledge is actually authorized to leave the protected environment?

This repository demonstrates two related properties:

Technical Non-Joinability — access to identity information is not authority to associate identity with content; access to content is not relationship authority; possession of several individually permitted data components does not automatically authorize reconstruction of the protected semantic relationship between them.

Technical Non-Completability — even after authorized reconstruction and AI computation, the resulting output does not become externally effective merely because the model successfully produced it.

The runnable reference implementation demonstrates the following chain:

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
AI computation
        ↓
Sealed Candidate Output
        ↓
live output verification
        ↓
Protected Output Validation Receipt (POVR)
        ↓
Output Release Capability
        ↓
Output Release Boundary
        ↓
external release

That is already the architecture implemented in the repository.

The key design rule is:

Access to data is not automatically authority to form every relationship between those data.

And after reconstruction:

Successful computation is not release authority.

The repository demonstrates independent semantic authority, permitted association scope, non-bearer reconstruction authorization, vault-local release, session-bound components, scope-limited reconstruction, provenance continuity, sealed Candidate Outputs, constitutive POVR, boundary-specific one-time release, fail-closed behavior, parallel vault fan-out, and legacy migration.

A runnable test suite covers 16 cases, including unauthorized semantic association, missing relationship authority, cross-session reuse, changed workload measurement, uncommitted POVR, destination substitution, replay, output mutation, epoch change, wrong release boundary, poisoned sessions, legacy decomposition, and parallel versus sequential vault release.

The local reference benchmark measured approximately 2.38 ms median for the complete protected path, while explicitly excluding network RPC, remote attestation, HSM/KMS, distributed commit, AI inference, and production observability.

And the repository is careful not to overclaim: it is an executable architectural reference, not proof of production security, and it explicitly lists the limits of the current Python implementation, local cryptography, same-process isolation, attestation model, provenance model, inference controls, and alternate-path closure.


The architecture addresses a security problem that becomes increasingly important as enterprise AI systems gain access to databases, vector stores, source-code repositories, communications, customer information, financial systems, internal planning tools, APIs, and autonomous tool chains:

Compromise of an AI workload should not automatically become authority to reconstruct the enterprise, infer protected relationships, or externalize the resulting intelligence.

The fundamental distinction is:

Access to identity is not authority to associate identity with content. Access to content is not relationship authority. Successful reconstruction is not output authority. Successful computation is not release authority.

The repository therefore does not model an ordinary DLP filter, database-sharding exercise, MCP wrapper, or post-hoc audit system. It demonstrates a narrower runnable profile of an architecture in which semantic reconstruction authority and output authority remain independently controlled.

The broader DAS Protocols VII disclosure separates computation from authorized consequence using independently protected domains, Mandatory Mediation, Technical Non-Joinability, Technical Non-Completability, protected validation evidence, output-specific Release Authority, and verification at a protected Output Release Boundary.

The Problem: A Compromised AI Server Can Become More Than a Data Breach

Traditional enterprise security often concentrates authority in the application layer.

An application server may simultaneously possess:

database credentials;
plaintext access;
identity information;
relationship mappings;
vector-search access;
model context;
tool credentials;
network authority;
file-write permission;
messaging authority;
and external API access.

For conventional applications this concentration may already be risky. For AI workloads it creates an additional problem: the workload can infer new relationships that were never stored explicitly.

A compromised AI system may correlate individually accessible records and infer:

customer-to-product relationships;
product defects associated with specific accounts;
future product strategy;
internal organizational relationships;
unreleased research;
acquisition or negotiation activity;
sensitive operational dependencies;
financial exposure;
strategic timelines;
or other enterprise intelligence.

DAS Protocols VII therefore treats the problem as more than:

“Was this workload permitted to read these records?”

The architecture also asks:

“Was this workload authorized to form this specific semantic relationship, for this purpose, in this session, and to make this exact derived result externally effective?”

The disclosure expressly separates the powers to access protected components, join them into meaningful enterprise intelligence, and externalize the resulting intelligence.

Core Architectural Principle
COMPUTATION
    ≠
RECONSTRUCTION AUTHORITY
    ≠
ASSOCIATION AUTHORITY
    ≠
OUTPUT AUTHORITY
    ≠
EXTERNAL EFFECT

The protected workflow implemented by this repository follows the more specific chain:

Legacy joined record / protected enterprise sources
        ↓
Independent semantic domains
        ↓
Identity Vault
Content Vault
Relationship-Mapping Vault
        ↓
Reconstruction Authorization Object (RAO)
        ↓
Independent Vault-Local Release Conditions
        ↓
Session-Bound Components
        ↓
Protected Reconstruction Domain
        ↓
Ephemeral Minimum-Necessary Data View
        ↓
Provenance / association continuity
        ↓
AI computation
        ↓
Sealed Candidate Output
        ↓
Live output verification
        ↓
Protected Output Validation Receipt (POVR)
        ↓
Output Release Capability
        ↓
Output Release Boundary
        ↓
External effect

The important property is not merely that several security checks exist. The important property is ordering and dependency:

NO VALID RECONSTRUCTION AUTHORITY
        → NO AUTHORIZED JOIN

NO VALID ASSOCIATION AUTHORITY
        → NO AUTHORIZED SEMANTIC RELATIONSHIP

NO VALID OUTPUT VERIFICATION
        → NO POVR

NO COMMITTED POVR
        → NO OUTPUT RELEASE CAPABILITY

NO VALID OUTPUT RELEASE CAPABILITY
        → NO EXTERNAL EFFECT

The broader disclosure describes this as Execution–Consequence Decoupling, Mandatory Mediation, Technical Non-Joinability, and Technical Non-Completability.

1. Independent Semantic Authority

A central architectural distinction is that storing values separately is not enough.

A system can place identity data in one table and content in another, yet still remain effectively joined if one application credential can retrieve both and reconstruct the relationship.

DAS Protocols VII instead treats the relationship itself as a protected technical asset.

The architecture may use:

Identity Vault
        +
Content Vault
        +
Relationship-Mapping Vault
        +
optional Cryptographic-Material Domain

The Relationship-Mapping Vault is not just another database table.

It acts as an independent authority over which semantic associations may be reconstructed.

Therefore:

IDENTITY ACCESS + CONTENT ACCESS
            ≠
RELATIONSHIP AUTHORITY

The broader disclosure expressly distinguishes permission to access fields from permission to associate those fields.

The reference implementation demonstrates this using independently controlled vault objects.

2. Technical Non-Joinability

Technical Non-Joinability means that separately maintained identity, content, relationship, provenance, cryptographic, or other protected components cannot be converted into a semantically usable enterprise representation outside an authorized protected reconstruction operation.

It does not mean the information can never be associated.

It means association authority exists only under controlled conditions such as:

protected session;
authorized purpose;
current execution context;
Permitted Association Scope;
Protected Reconstruction Domain;
protected policy state;
Mandatory Mediation Path.

A user or workload may therefore have legitimate access to two values while still lacking authority to establish or externalize the semantic relationship between them.

This distinction is important for AI because models can infer relationships from combinations of information even where no direct database join exists.

3. Permitted Association Scope

A Permitted Association Scope is separate from an ordinary field-access list.

Consider:

Field A → permitted
Field B → permitted

That does not automatically imply:

Association(A, B) → permitted

DAS Protocols VII allows a protected authorization decision to specify which relationships may be formed during a particular reconstruction session.

The broader disclosure contemplates representations such as:

explicit relationship rules;
permitted-association graphs;
prohibited-association graphs;
entity classes;
relationship classes;
protected predicates;
purpose restrictions;
destination restrictions.

The permitted association scope therefore controls semantic combination, not merely storage access.

The current v0.1.0 implementation uses structured exact association rules rather than full graph-policy or inferred-semantic enforcement.

4. Non-Bearer Reconstruction Authorization Object

A Protected Authorization Domain can issue a Reconstruction Authorization Object (RAO).

The RAO may bind:

requester;
tenant;
workload identity;
attested execution-context measurement;
session identifier;
session nonce;
Session Epoch;
Policy Epoch;
permitted field set;
Permitted Association Scope;
authorized processing purpose;
permitted output types;
destinations;
recipients;
jurisdiction conditions;
validity conditions;
use-count conditions;
Disclosure Budget;
Inference-Channel Budget;
Protected Reconstruction Domain;
Output Release Boundary.

The essential property is that the RAO is not intended to operate as a freely transferable bearer token.

Possession of the object alone is insufficient.

Exercise must still correspond to current protected:

execution context
+
session
+
epoch
+
policy
+
workload
+
domain
+
scope

The patent explicitly describes this non-bearer correspondence model.

The reference implementation models this using session, workload, epoch, record, and vault-local bindings.

5. Independent Vault-Local Release

A valid RAO does not automatically dump all requested enterprise information into the AI process.

Each required vault separately evaluates its own Vault-Local Release Conditions.

For example:

RAO
 ├── Identity Vault verifies local conditions
 ├── Content Vault verifies local conditions
 └── Relationship Vault independently verifies association authority

A vault can therefore deny even when other vaults succeed.

Approved material is converted into Session-Bound Components rather than unrestricted reusable plaintext objects.

The disclosure allows vault-local release receipts to bind released components to the RAO, session, Session Epoch, releasing vault, and Protected Reconstruction Domain.

The current implementation demonstrates the same logical principle using separate vault-local integrity bindings.

6. Session-Bound Components

Material released by a vault should not silently become a permanently reusable enterprise object.

Released components are bound to the protected reconstruction context.

The implementation binds them to properties such as:

RAO;
session;
epoch;
workload;
expiry;
releasing vault;
protected integrity state.

This helps prevent an attacker from collecting legitimate fragments from multiple historical sessions and recombining them later into an unauthorized representation.

Cross-session component reuse is explicitly tested in v0.1.0.

7. Protected Reconstruction Domain

The Protected Reconstruction Domain is where approved components are permitted to become semantically usable together.

It does not reconstruct the full enterprise record merely because all source systems technically contain the required information.

Instead it creates an:

Ephemeral Minimum-Necessary Data View

containing only the fields and relationships authorized for the requested purpose.

The broader disclosure states that the complete semantically usable enterprise record should not be persistently exported outside the protected processing span unless separately authorized.

This is substantially different from ordinary data sharding.

The purpose is not merely:

store values separately

but:

make authorized semantic reconstruction
a protected operation in its own right
8. Provenance and Association Continuity

Once reconstruction occurs, the architecture does not simply discard where the information came from.

Protected provenance may follow:

source components;
reconstructed fields;
permitted associations;
intermediate values;
protected derivatives;
generated fragments;
tool arguments;
retrieval queries;
Candidate Output portions.

This gives the Output Verification Stage a basis for asking whether an output derives from:

an unauthorized source;
an unauthorized identity-content relationship;
an unauthorized transformation;
or data outside the permitted reconstruction.

The broader disclosure permits provenance to be represented by explicit labels, structured intermediates, deterministic schemas, protected references, information-flow state, or confined processing paths.

The current implementation demonstrates structured provenance continuity. It does not claim a general solution to arbitrary semantic information-flow analysis.

9. AI Computation Does Not Create Output Authority

Once the minimum-necessary view exists, AI computation may proceed.

The workload may:

summarize;
classify;
infer;
generate;
analyze;
transform;
retrieve;
plan;
or derive a new result.

But completion of the computation does not complete the security transaction.

The resulting artifact becomes a:

Candidate Output

not an externally releasable result.

This is the central execution-finality separation:

SUCCESSFUL AI COMPUTATION
        ≠
AUTHORIZED EXTERNAL OUTPUT
10. Sealed Candidate Output

Before the Candidate Output becomes available to an uncontrolled output path, the broader architecture requires it to remain Non-Releasable.

The patent describes possible mechanisms including:

encryption;
hardware sealing;
protected memory;
protected output buffers;
capability restriction;
destination binding;
mandatory channels;
protected intermediate representations.

The relevant invariant is that the workload itself lacks sufficient key material, release authority, protected state, interface authority, or path control to independently turn the Candidate Output into an external consequence.

The v0.1.0 implementation uses AES-GCM sealing for this purpose.

That is a runnable demonstration of the state-machine relationship, not equivalent to a production hardware-sealed output boundary.

11. Live Output-Time Re-Verification

Authorization at reconstruction time is not assumed to remain valid forever.

Immediately before output release, the architecture can re-establish:

workload measurement;
current revocation state;
Policy Epoch;
Session Epoch;
use count;
Disclosure Budget;
Inference-Channel Budget;
destination;
recipient;
output type;
Output Release Boundary;
quorum state;
jurisdiction state;
continuity with the RAO.

This addresses time-of-check-to-time-of-use risk.

If the model, runtime, agent code, tools, policy, destination, tenant, revocation state, or session has changed, previously obtained authorization does not automatically remain sufficient.

The reference implementation tests policy-epoch changes and changed workload measurements.

12. Output-Scope and Association Evaluation

The Output Verification Stage can evaluate whether the Candidate Output:

contains unauthorized protected fields;
creates an Unauthorized Cross-Vault Correlation;
exceeds the Permitted Association Scope;
violates the processing purpose;
exceeds output scope;
targets the wrong destination;
targets the wrong recipient;
violates jurisdiction restrictions;
exceeds a Disclosure Budget;
exceeds an Inference-Channel Budget;
contains unverifiable provenance;
contains unauthorized tool operations;
creates unauthorized persistent memory.

The wider disclosure contemplates methods including:

structured parsing;
entity extraction;
graph comparison;
protected identity indices;
provenance analysis;
embedding similarity;
information-flow analysis;
classifier-assisted analysis;
cumulative output analysis.

The v0.1.0 repository intentionally implements only a subset of this broader evaluation model.

13. Protected Output Validation Receipt — POVR

A successful verification result alone does not necessarily produce Release Authority.

Instead, the architecture can first generate a Protected Output Validation Receipt (POVR).

The POVR may bind:

RAO digest
Candidate Output digest
verified output digest
provenance digest
execution-context measurement
Session Epoch
Policy Epoch
destination
recipient
output type
Permitted Association Scope
Output Release Boundary
verification result

The critical property is:

The receipt is committed before Release Authority exists.

This makes the receipt constitutive, rather than merely evidentiary.

A conventional audit record says:

the event happened
and then evidence was recorded

The constitutive model says:

if protected receipt commitment does not succeed,
the authority required to complete the event does not exist

The patent expressly describes this distinction.

The current repository implements commit-before-capability behavior.

14. Atomic Output Finality Transaction

The broader architecture defines an Atomic Output Finality Transaction (AOFT).

It can group two or more operations such as:

final Candidate Output verification;
protected transformation;
POVR generation;
POVR commitment;
Release Authority formation;
Output Release Capability issuance;
key derivation;
protected state advancement;
boundary-specific release preparation.

The required property is:

Failure must not leave usable partial Release Authority.

For example:

verification succeeded
BUT receipt commit failed
        →
NO RELEASE

receipt prepared
BUT not durably committed
        →
NO RELEASE

provisional capability exists
BUT protected transaction failed
        →
NO RELEASE

This all-or-nothing finality relationship is explicitly described in DAS Protocols VII.

The current SQLite implementation demonstrates a local subset of these atomic semantics.

15. Output-Specific Release Capability

Only after the required validation and receipt state succeeds is an Output Release Capability formed.

It can be bound to:

Candidate Output digest;
POVR digest;
session;
Session Epoch;
Policy Epoch;
destination;
recipient;
output type;
Output Release Boundary.

It is therefore not:

permission to export enterprise information

It is closer to:

permission for this exact verified output,
under this protected state,
to become effective through this exact boundary

The capability is consumed or transitioned to a non-reusable state after effectuation.

16. Output Release Boundary

The Output Release Boundary is the point where a non-effective Candidate Output first becomes externally usable or authoritative.

Depending on deployment, that may be the boundary controlling:

decryption;
network transmission;
display;
rendering;
file writing;
database commit;
message publication;
tool invocation;
persistent memory;
payment initiation;
workflow transition;
actuator operation.

The broader disclosure explicitly treats these as examples of consequence-bearing boundaries.

This is why DAS Protocols VII is not limited to “data leakage.”

The same finality concept can potentially govern:

DATA RELEASE
TOOL EXECUTION
DATABASE CHANGE
MESSAGE SEND
PAYMENT
WORKFLOW TRANSITION
CYBER-PHYSICAL ACTION
17. Technical Non-Completability

Technical Non-Completability means that successful computation, action selection, or Candidate Output generation is insufficient to complete the external consequence.

At least one technically enforced operation remains unavailable until protected conditions are satisfied.

These may include:

current-state verification;
execution-context correspondence;
provenance verification;
association-scope verification;
protected receipt commitment;
quorum approval;
Release Authority formation;
key application;
state-machine advancement;
Output Release Boundary verification.

The disclosure expressly distinguishes this from policy statements, contracts, organizational procedures, advisory warnings, retrospective logging, and post-release detection.

The key invariant is:

THE WORKLOAD MAY COMPLETE COMPUTATION

BUT

THE WORKLOAD CANNOT INDEPENDENTLY COMPLETE CONSEQUENCE
18. Fail-Closed Semantics

The architecture is deliberately fail closed.

A release can be denied where required protected state is:

absent;
stale;
ambiguous;
unavailable;
inconsistent;
expired;
revoked;
unverifiable.

A timeout, unavailable policy service, stale cached bearer token, or legacy fallback is not supposed to create a default-allow path.

The current implementation demonstrates denial for conditions including:

missing relationship authority;
unauthorized semantic association;
stale session;
changed workload;
changed destination;
changed policy;
uncommitted receipt;
wrong boundary;
Candidate Output mutation;
replay.

This behavior is summarized in the existing repository.

19. Streaming and Cumulative Disclosure

AI output is often incremental.

A token, output chunk, audio segment, tool-argument fragment, or structured field may become externally useful before the full response exists.

DAS Protocols VII therefore extends finality to segmented output.

The disclosure describes chained segment capabilities and rolling disclosure state such that:

each segment can be independently verified;
cumulative disclosure can be tracked;
segment capabilities must remain in sequence;
a poisoned stream invalidates unconsumed segment capabilities.

This prevents a system from relying solely on a final check after earlier information has already escaped.

Streaming cumulative-disclosure enforcement is part of the broader disclosure but is not fully implemented in v0.1.0.

20. Disclosure Budget and Inference-Channel Budget

A sequence of individually permissible responses can collectively reveal prohibited information.

DAS Protocols VII therefore contemplates:

Disclosure Budget
Inference-Channel Budget

These can constrain direct and indirect disclosure over repeated queries, aggregate outputs, or incremental release.

This matters because a compromised AI workload may attempt to reconstruct a prohibited relationship indirectly rather than requesting it in one explicit operation.

The v0.1.0 repository does not implement a general quantitative disclosure-budget engine. That remains a broader disclosed mechanism and future implementation area.

21. Prompt Injection and Compromised-Workload Assumption

The security architecture does not depend on assuming that the AI workload remains trustworthy.

The disclosure explicitly considers:

prompt injection;
malicious retrieved content;
altered agent code;
compromised model state;
tool substitution;
adversarial instructions;
full workload compromise.

The architecture instead attempts to retain protected control over reconstruction and consequence even if the workload produces a prohibited output.

This is a significant distinction from approaches where security depends mainly on the model following instructions.

The design principle is:

The workload may fail, be manipulated, or be compromised, and the protected output path must still remain separately controlled.

22. Hardware-Backed Deployment

The architecture is mechanism-neutral.

A production deployment may use hardware-backed execution and attestation mechanisms such as:

TPM 2.0;
Intel SGX;
Intel TDX;
AMD SEV-SNP;
ARM Confidential Compute Architecture;
AWS Nitro Enclaves;
confidential virtual machines;
HSMs;
secure boot;
accelerator attestation;
NVIDIA confidential-computing GPU state;
protected firmware.

For accelerator-backed AI, the disclosed execution-context measurement may bind properties such as:

host state;
accelerator state;
model-weight digest;
runtime digest;
firmware state;
interconnect-protection state;
tenant;
protected-memory mode.

The current Python implementation does not provide such hardware assurance.

It models the protocol relationships in portable software.

23. Multi-Authority and High-Sensitivity Reconstruction

For particularly sensitive associations, DAS Protocols VII permits k-of-n authority models.

Possible independent authorities include:

tenant authority;
enterprise security;
DPO/privacy authority;
legal authority;
business-unit authority;
jurisdiction authority;
consent authority;
financial compliance;
system owner.

A relationship-mapping vault could therefore require multiple independently protected approvals before releasing a high-sensitivity association.

Multi-authority quorum enforcement is not implemented in v0.1.0.

24. Performance Architecture

The architecture does introduce additional work.

Possible costs include:

vault-local verification;
attestation;
provenance propagation;
association analysis;
receipt commitment;
Candidate Output sealing;
capability verification;
protected state maintenance.

But DAS Protocols VII does not prescribe one universal latency.

The disclosure allows latency reduction through:

protected precomputation;
bounded-freshness artifacts;
local receipt commitment;
compiled policy evaluation;
incremental provenance;
parallel vault retrieval;
batch verification;
segmented release;
hardware acceleration.
Hot Path / Cold Path

The architecture explicitly permits separation between a cold path and a hot path.

The cold path may prepare:

compiled policy predicates;
permitted-association graphs;
protected identity indices;
registered workload measurements;
destination manifests;
attestation collateral;
revocation snapshots;
provenance schemas;
disclosure rules.

The hot path then performs the conditions that must still be current at reconstruction or output time:

session verification;
epoch verification;
bounded-freshness or live attestation;
revocation;
output-scope verification;
provenance evaluation;
association evaluation;
receipt commitment;
Release Capability issuance;
boundary verification.

Precomputation can reduce latency, but it does not replace current finality conditions.

25. Reference Benchmark

The current repository includes a local benchmark.

The included reference run reports a complete local protected path with median latency of approximately:

2.38 ms

This should not be interpreted as a production multi-vault performance claim.

The benchmark excludes important production costs such as:

network RPC;
remote attestation;
HSM/KMS access;
distributed commit;
real AI inference;
production telemetry;
cross-region operation;
hardware isolation.

The README should preserve this limitation exactly.

26. Parallel Vault Fan-Out

Independent authority does not inherently require sequential network calls.

Where the required vault decisions are independent, vault-local release operations may execute concurrently.

The repository demonstrates parallel local fan-out and verifies that parallel and sequential reconstruction preserve equivalent authorization scope.

The broader objective is:

INDEPENDENT AUTHORITY
        ≠
NECESSARILY SERIAL LATENCY
27. Legacy Enterprise Integration

DAS Protocols VII is explicitly designed for incremental deployment.

Existing systems can continue to operate behind mandatory mediation components such as:

proxy;
wrapper;
broker;
gateway;
adapter;
storage filter;
OS service;
model-serving layer;
output controller.

Legacy infrastructure can include:

ERP;
CRM;
identity systems;
document systems;
data lakes;
warehouses;
vector databases;
knowledge graphs;
AI models;
application servers;
cloud infrastructure;
existing enterprise APIs.

The disclosure does not require wholesale replacement of these systems.

Critical Legacy Invariant

A wrapper alone does not establish Technical Non-Joinability.

If the AI workload can still directly access:

old joined database
raw vault credential
debug endpoint
alternate API
unmediated file path
uncontrolled network route

then the protected architecture can simply be bypassed.

The existing README correctly states that the legacy adapter is a migration demonstration, not bypass closure.

The broader disclosure is even stricter: observe-only monitoring does not satisfy Technical Non-Completability; the protected mediation path must become mandatory.

28. Threat Model

This architecture is designed around compromise of one or more ordinary AI execution components.

Representative compromise targets include:

AI model server;
autonomous agent;
orchestration layer;
retrieval pipeline;
vector-store interface;
application server;
tool-use framework;
model memory;
enterprise credential;
plugin;
API integration.

The desired containment property is:

COMPROMISE OF COMPUTATION

does not automatically imply

COMPROMISE OF SEMANTIC ASSOCIATION

and does not automatically imply

COMPROMISE OF EXTERNAL CONSEQUENCE

The architecture uses multiple independent controls rather than assuming one perfect security boundary.

29. Example Threat Scenario

Consider an AI assistant connected to:

Customer Support
Product Development
Engineering Communications
Financial Systems
Internal Planning

An attacker compromises the AI workload and attempts to:

identify strategic customers
        ↓
associate complaints with unreleased defects
        ↓
correlate defects with engineering activity
        ↓
infer future product roadmap
        ↓
determine intended markets
        ↓
generate competitive intelligence
        ↓
transmit it externally

Under the DAS Protocols VII architecture:

identity authority remains separate
content authority remains separate
relationship authority remains separate
        ↓
reconstruction remains session scoped
        ↓
unauthorized associations fail
        ↓
Candidate Output remains non-releasable
        ↓
output-time state is re-verified
        ↓
POVR must commit
        ↓
output-specific Release Capability required
        ↓
Output Release Boundary controls effectuation

The workload may potentially be manipulated into computing the prohibited report while still being unable to make the report externally effective.

That is the intended consequence of Execution–Consequence Decoupling.

30. What the v0.1.0 Code Actually Demonstrates

The current runnable implementation demonstrates:

independent Identity, Content, and Relationship-Mapping Vault objects;
distinct semantic release authority;
structured Permitted Association Scope;
non-bearer session/workload-bound RAO behavior;
independent vault-local field projection;
Session-Bound Components;
protected minimum-necessary reconstruction;
structured provenance continuity;
AES-GCM Sealed Candidate Outputs;
local constitutive POVR commitment;
output-specific Release Capability;
destination and recipient binding;
session and policy-epoch binding;
Output Release Boundary binding;
one-time release consumption;
fail-closed state transitions;
session poisoning;
legacy joined-record decomposition;
parallel local vault release.

These properties are directly reflected in the existing repository description.

31. Executable Tests

The v0.1.0 test suite currently contains 16 tests covering:

authorized multi-vault reconstruction and output release;
relationship authority required even when identity and content are available;
unauthorized semantic association denial;
vault-local field projection;
cross-session component reuse denial;
changed workload measurement denial;
Candidate Output cannot claim unreconstructed fields;
no Output Release Capability where POVR commitment fails;
destination substitution denial;
single-use replay denial;
Candidate Output mutation denial;
Policy Epoch change denial;
wrong Output Release Boundary denial;
poisoned-session fail-closed behavior;
legacy joined-record decomposition;
equivalent scope under parallel and sequential vault release.

The repository reports:

Ran 16 tests
OK

32. Quick Start
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m unittest discover -s tests -v
python -m das_vii_multivault.demo
python bench/benchmark.py

On Windows:

python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
python -m unittest discover -s tests -v
python -m das_vii_multivault.demo
python bench\benchmark.py
33. Current v0.1.0 Limitations

This repository must not be described as proof that the full DAS Protocols VII architecture has been implemented.

The current reference has important limitations:

all three vaults are Python objects within one process;
separate secrets demonstrate independent logical decisions, not independent hardware trust domains;
a fully compromised Python process can bypass the software reference boundary;
HMAC is used for local integrity rather than production multi-authority PKI;
AES-GCM sealing is performed inside the same process;
SQLite is not rollback-resistant hardware state;
no distributed transaction protocol is implemented;
no real TEE/HSM/GPU confidential-computing attestation is performed;
no general semantic provenance engine exists;
no general inferred-association detector is implemented;
no graph-policy engine is implemented;
no quantitative Disclosure Budget is implemented;
no quantitative Inference-Channel Budget is implemented;
no multi-authority quorum implementation exists;
parallel fan-out uses local threads, not distributed RPC;
the legacy adapter does not remove the original joined record;
universal alternate-path closure is not established;
no GDPR, EU AI Act, or sectoral legal compliance determination is made.

These limitations are already accurately acknowledged in the repository and should remain prominent.

34. What a Production Implementation Would Need

A serious production deployment should consider replacing the reference abstractions with independently protected components such as:

Identity Vault
    → independent protected data service / HSM / TEE

Content Vault
    → independently controlled protected storage

Relationship Vault
    → independently controlled mapping authority

Protected Reconstruction Domain
    → TEE / confidential VM / secure processing domain

POVR Store
    → append-only / rollback-resistant protected journal

Output Release Capability
    → protected non-bearer cryptographic authority

Output Release Boundary
    → OS / network / storage / accelerator / application effectuation boundary

Additional controls may include:

hardware attestation;
protected monotonic epochs;
key isolation;
secure boot;
IOMMU/DMA restrictions;
confidential GPU execution;
remote-attestation verification;
quorum authorities;
distributed finality;
destination-side verification;
replay-resistant protected state;
receiver idempotency;
streaming finality;
cumulative disclosure controls;
protected telemetry.
35. Mechanism Neutrality

DAS Protocols VII is intentionally not limited to one cryptographic primitive or one trusted hardware vendor.

The disclosure permits enforcement through:

cryptography;
protected state machines;
mandatory reference monitors;
capability systems;
hardware isolation;
OS isolation;
confidential computing;
trusted brokers;
protected control planes;
append-only journals;
monotonic protected state;
quorum control;
secure kernels;
independently controlled gateways.

The operative test is whether the AI workload can unilaterally bypass or fabricate the protected state necessary to make the Candidate Output externally effective.

36. Technical Enforcement, Not Policy-Only Restriction

The architecture is not satisfied merely because a policy says:

the AI must not disclose this relationship

or:

the AI should not send this output

The broader disclosure expressly distinguishes execution-finality from:

contractual restrictions;
human-readable policies;
administrative rules;
system prompts;
model-alignment instructions;
audit obligations;
organizational expectations.

The target property is technical:

the workload lacks unilateral ability to complete the controlled consequence unless the protected finality conditions are satisfied.

Human approval can still be part of the architecture, but once required it should become part of the protected completion condition rather than merely an informal expectation.

37. Design Distinction from Agentic Tool Finality

This repository is deliberately different from the separate execution-finality profile for tool invocation.

The tool-binding architecture asks primarily:

May this exact AI-generated tool call be invoked?

DAS Protocols VII asks an earlier and broader question:

May these independently controlled enterprise components be semantically joined at all, and may a result derived from that reconstruction ever leave the protected processing path?

Therefore:

DAS Protocols VII
    → reconstruction authority
    → semantic association authority
    → protected enterprise processing
    → output finality

whereas the tool-call profile focuses primarily on:

Candidate Tool Act
    → protected validation
    → act-bound authority
    → Finality Sink
    → invoke()

They can be composed, but they are not the same security layer. The current README already correctly makes this distinction.

38. Industrial Applicability

The broader architecture is applicable beyond ordinary enterprise document processing.

The disclosure identifies potential application across:

enterprise AI;
agentic AI;
multi-agent systems;
model serving;
RAG;
vector databases;
cloud infrastructure;
confidential computing;
cybersecurity;
telecommunications;
financial services;
healthcare;
government systems;
industrial automation;
critical infrastructure;
robotics;
autonomous systems;
cyber-physical systems.

The same underlying control principle applies wherever a compromise of computation should not automatically become authority to produce a consequential external effect.

39. Commercial / Deployment Forms

The disclosed architecture may be implemented as:

enterprise AI security platform;
confidential-computing service;
protected reconstruction service;
AI output-finality gateway;
operating-system security service;
hardware appliance;
telecommunications function;
SDK;
API;
model-serving control layer;
hybrid hardware/firmware/software architecture.

It may integrate with existing environments using proxies, adapters, gateways, brokers, storage filters, OS services, and model-serving layers.

40. Synthetic Data

All identities, records, destinations, measurements, secrets, and outputs in the reference implementation are synthetic.

No live enterprise data or production credentials are included.

41. Security Position in One Sentence

Compromise of an AI workload should not automatically confer authority to reconstruct protected enterprise relationships or make the resulting intelligence externally effective.

Or technically:

COMPROMISE(COMPUTE)
        ≠
AUTHORITY(JOIN)
        ≠
AUTHORITY(RELEASE)
42. Reference Disclosure

DAS Protocols VII — Architecting Resilience for Enterprise AI: Preventing Data Reconstruction, Exfiltration, and Unauthorized Consequence in Compromised AI Environments

The full disclosure should be treated as the broader architectural reference.

This repository implements a selected executable profile for engineering inspection and testing. It does not attempt to implement every embodiment, variant, hardware realization, distributed-finality mechanism, semantic inference-control mechanism, or design-around closure described in the full disclosure.

43. Final Scope Statement

This repository demonstrates a concrete proposition:

An AI workload can be allowed to compute over protected enterprise information without automatically giving that workload persistent authority to reconstruct every semantic relationship or independently release every result it can derive.

The design achieves this by separating:

data access
        ↓
semantic association
        ↓
protected reconstruction
        ↓
AI computation
        ↓
output validation
        ↓
receipt commitment
        ↓
release authority
        ↓
external consequence

Each stage can remain independently bounded.

That is the core engineering objective of Technical Non-Joinability + Technical Non-Completability + Output Finality.
