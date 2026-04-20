# Agora Social Governance Framework: Architecture Diagram & Risk and Control Matrix

## 1. Master Architecture Diagram (Visible Output 1)

This diagram outlines the "Defense-in-Depth" flow of content moderation, from ingestion to final audited decision. Each component represents a layer in our Human-in-the-Loop (HITL) system.
+------------------+     +--------------------------+     +--------------------------+
|  User Submits    | --> | 1. Ingestion Layer       | --> | 2. AI Risk Evaluator     |
|    Post          |     |    (Simulated Feed)      |     |    (OpenAI Moderation API)|
+------------------+     +--------------------------+     +--------------------------+
      |                          |                                  |
      |                          |                                  | (Returns AI Score & Category)
      v                          v                                  v
+--------------------------+     +--------------------------+     +--------------------------+
| 3. The Routing Gate      | <-- | AI Score (0.0 - 1.0)     | --> | 4. Human Adjudication    |
|    ("Safety Valve" Logic)|     | Max Score Category       |     |    Portal (Streamlit UI) |
+--------------------------+     +--------------------------+     +--------------------------+
      |      |      |               (If PENDING_REVIEW)                     |
      |      |      |                                                     | (Human Decision & Rationale)
      |      |      +-----------------------------------------------------+
      |      |                                                            |
      |      +------------------------------------------------------------+
      |                                                                   |
      v                                                                   v
+--------------------------------------------------------------------------+
| 5. Governance Registry (SQLite Database)                                 |
|    - Stores all POSTS (content, AI score, routing decision)              |
|    - Stores AUDIT_LOG (human decision, rationale, timestamp)             |
+--------------------------------------------------------------------------+
      |
      | (Data for Oversight)
      v
+--------------------------------------------------------------------------+
| 6. Admin Oversight Dashboard (Streamlit UI)                              |
|    - Visualizes Control Precision, Policy Drift, Systemic Bias (future)  |
+--------------------------------------------------------------------------+

### **Flow Explanation:**

1.  **Ingestion Layer:** Simulates real-time user-generated content (posts).
2.  **AI Risk Evaluator:** The OpenAI Moderation API processes each post, providing 11 harm category scores. Our system extracts the maximum confidence score and its category.
3.  **The Routing Gate:** This Python logic applies the predefined governance thresholds (0.45 and 0.85).
    *   Posts with AI scores < 0.45 are `AUTO_APPROVED`.
    *   Posts with AI scores > 0.85 are `AUTO_REJECTED`.
    *   Posts within the "Uncertainty Zone" (0.45-0.85) are marked `PENDING_REVIEW` and routed to human adjudication.
    *   **Resilience Control:** If the OpenAI API encounters an error (e.g., "Too Many Requests"), the AI score defaults to 0.5, ensuring all such posts are sent for human review, preventing system failure.
4.  **Human Adjudication Portal:** A Streamlit web application where "Policy Adapters" review `PENDING_REVIEW` posts. It provides reviewer context (raw post, AI score, policy guidelines) and enforces a "Forced Rationale" for every decision.
5.  **Governance Registry:** An SQLite database (`agora_registry.db`) that serves as the immutable record of *every* decision (AI and human), including post content, AI scores, routing decisions, human labels, and detailed rationales with timestamps. This is the "evidentiary backbone."
6.  **Admin Oversight Dashboard (Upcoming):** A future Streamlit application for "Compliance Officers" to monitor the overall system performance, audit trails, and identify potential risks like 'Control Precision' or 'Policy Drift'.

---

## 2. Risk & Control Matrix (RCM) (Visible Output 2)

This matrix maps identified risks to the specific controls implemented within our framework, demonstrating how policy intent translates into actionable system design.

| # | Risk Name             | Lifecycle Stage | Technical & Governance Control Implemented                                                                                                                                                                                                                                                                                                   |
|---|-----------------------|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1 | **Model Drift**         | Operation       | **Registry Delta Tracking (Future Dashboard):** The Governance Registry logs every AI score and corresponding human decision. The Admin Dashboard (future) will compare these to detect discrepancies, indicating AI drift (AI-to-human agreement drops below a threshold).                                                                      |
| 2 | **Algorithmic Bias**    | Build           | **Fairlearn Audit (Future):** While `fairlearn` installation faced initial challenges, it's designated as our open-source tool for monthly parity checks across linguistic clusters (e.g., AAVE vs. Standard English) on synthetic data. This will provide quantitative evidence of fairness, addressing DSA transparency requirements.            |
| 3 | **Audit Deficit**       | Operation       | **Immutable Registry:** SQLite log of every decision, rationale, and timestamp (`AUDIT_LOG` table). Each entry is uniquely identified (`log_id`, `post_id`) and cannot be altered, ensuring full traceability.                                                                                                                                  |
| 4 | **Policy Misalignment** | Design          | **Risk & Control Matrix:** This document itself explicitly maps harm categories to custom routing thresholds, ensuring AI behavior (via `gate.py`) is directly aligned with defined policy.                                                                                                                                                 |
| 5 | **Human Burnout**       | Operation       | **Dynamic Threshold Tuning (Future Dashboard):** The Routing Gate's thresholds (0.45-0.85) can be dynamically adjusted. The Admin Dashboard will monitor "Human Intervention Rate" (reviewer load). Policy Managers can narrow the "Uncertainty Zone" to reduce queue size during peak periods, mitigating reviewer fatigue.                    |
| 6 | **Regulatory Breach**   | Evolve          | **Evidence Packs (Future):** The Governance Registry's structure allows easy export of detailed audit logs (SQL, JSON) and related artifacts (e.g., bias reports) to satisfy regulatory requirements like the DSA, demonstrating compliance and accountability to external auditors.                                                         |
| 7 | **API Instability/Failure (NEW)** | Operation | **API Fallback Control:** If the OpenAI Moderation API fails or returns a "Too Many Requests" error, the system automatically assigns a default score of 0.5 to the post, routing it to "PENDING_REVIEW" for human adjudication. This ensures continuous operation and prevents unsupervised AI decisions during external service interruptions. |
