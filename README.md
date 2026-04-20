# The Agora Social Governance Framework

## Problem Context: The Governance Deficit
Social media platforms face regulatory risks (like the EU DSA) when relying on opaque, fully automated moderation. This project operationalizes a Human-in-the-Loop (HITL) Governance Framework to ensure content moderation is transparent, documented, and defensible. 

## System Architecture
Our system uses a "Defense-in-Depth" flow:
1. **Ingestion:** Synthetic posts are evaluated.
2. **AI Risk Evaluator (Commercial Tool):** Posts are scored using the **OpenAI Moderation API**.
3. **The Routing Gate (`gate.py`):** Posts scoring between 0.45 and 0.85 (or encountering API errors) trigger a "Governance Lock" and are sent to human review.
4. **Human Adjudication Portal (`portal.py`):** A **Streamlit** UI where reviewers must provide a "Forced Rationale" for their decisions.
5. **Governance Registry:** An **SQLite** database storing the immutable audit trail.
6. **Admin Oversight Dashboard (`dashboard.py`):** A real-time monitor for compliance officers.

## Setup Instructions (For the Evaluator)
1. Install dependencies: `pip install openai streamlit pandas`
2. Add your OpenAI API key to your environment: `export OPENAI_API_KEY='your_key_here'`
3. Run the Routing Gate to populate the database: `python3 gate.py`
4. Run the Adjudication Portal to review posts: `python3 -m streamlit run portal.py`
5. Run the Admin Dashboard to view metrics: `python3 -m streamlit run dashboard.py`

## Evidence Pack
Please see the `/Evidence_Pack` folder for exported SQL Audit Logs, processed posts data, system mock notifications, and the Threshold Sensitivity Analysis. The Master Architecture Diagram and Risk & Control Matrix can be found in `ARCHITECTURE_AND_RCM.md`.
