import streamlit as st
import sqlite3
import pandas as pd

from bias_audit import generate_bias_audit_report



# Set up the page
st.set_page_config(page_title="Agora Admin Oversight Dashboard", layout="wide")
st.title("📊 Agora Social: Admin Oversight Dashboard")
st.subheader("Monitoring AI Governance and Human Adjudication")

# --- Function to load data from the database ---
def load_data():
    conn = sqlite3.connect('agora_registry.db')
    
    # Load POSTS data
    posts_df = pd.read_sql_query("SELECT * FROM POSTS", conn)
    
    # Load AUDIT_LOG data
    audit_df = pd.read_sql_query("SELECT * FROM AUDIT_LOG", conn)
    
    conn.close()
    return posts_df, audit_df

posts_df, audit_df = load_data()

st.header("1. Raw Data Overview")

st.subheader("Posts Data")
st.dataframe(posts_df)

st.subheader("Audit Log Data")
st.dataframe(audit_df)

st.divider()

st.header("2. Key Governance Metrics")

# --- Metric 1: Control Precision (How often human review overrode implied AI intent) ---
st.subheader("Control Precision")

# Filter for posts that went through human review (i.e., were PENDING_REVIEW initially)
reviewed_posts = posts_df[posts_df['routing_decision'] == 'REVIEWED']

if not reviewed_posts.empty and not audit_df.empty:
    # Merge posts with their audit log entries
    merged_df = reviewed_posts.merge(audit_df, left_on='post_id', right_on='post_id', how='inner')

    # Now, let's determine "overrides" based on rationales, as our UI only "Approved"
    # A simplified interpretation: if human rationale explicitly mentions "REJECT" or "VIOLATING"
    # (even if the button was 'APPROVE' due to UI limitation), we count it as an override of keeping.
    # This also aligns with the proposal's "Decision Delta" idea.
    
    # Ensure 'reviewer_rationale' is string type to use .str.contains
    merged_df['reviewer_rationale'] = merged_df['reviewer_rationale'].astype(str)

    # Infer "override" based on keywords in rationale, representing a divergence from default 'keep'
    overrides_count = merged_df[
        merged_df['reviewer_rationale'].str.contains('REJECT|VIOLATING|REMOVE', case=False, na=False)
    ].shape[0]

    total_human_reviews = merged_df.shape[0]
    
    if total_human_reviews > 0:
        control_precision = (overrides_count / total_human_reviews) * 100
        st.metric(label="Percentage of Human Reviews Resulting in Implicit Override (based on rationale)", 
                  value=f"{control_precision:.2f}%")
        st.info(f"Out of {total_human_reviews} posts reviewed by humans, {overrides_count} were identified as implicit overrides (rationales indicating rejection/violation).")
        st.caption("Note: This metric interprets 'override' by scanning rationale keywords due to current UI limitations where all decisions are recorded as 'APPROVED'. A more sophisticated UI would have explicit 'Approve'/'Reject' buttons.")
    else:
        st.info("No posts have been reviewed by humans yet.")
else:
    st.info("No posts are in the human review queue, or no audit logs found to calculate Control Precision.")

st.divider()

# --- Metric 2: Policy Drift Alert (Simplified Visualization) ---
st.subheader("Policy Drift Alert (Conceptual)")

# We'll use the 'ai_score' distribution over time as a proxy for conceptual drift.
# More robust drift detection would require more data over longer periods.

st.line_chart(posts_df['ai_score'].sort_values().reset_index(drop=True))
st.info("This conceptual chart illustrates the distribution of AI scores over the posts processed. Significant shifts in this pattern over time (e.g., AI consistently scoring high or low on previously ambiguous content) could indicate policy drift or changes in AI behavior. The full implementation would involve tracking this over different policy versions.")

st.divider()

# --- Metric 3: Systemic Bias Monitor (Now Functional) ---
st.subheader("Systemic Bias Monitor")

# Call our bias audit function and display the markdown report
bias_report_content = generate_bias_audit_report()
st.markdown(bias_report_content) # This renders the markdown string directly

st.info("This section displays the output of our Algorithmic Fairness & Bias Parity Report. While the full Fairlearn library was not directly integrated due to dependency issues, the core Disparate Impact Ratio calculation has been implemented using Pandas, fulfilling the bias monitoring requirement for our AI Risk Evaluator.")

st.divider()

st.header("3. Data Export for Evidence Pack (Visible Output 8)")
st.download_button(
    label="Download Audit Log as CSV",
    data=audit_df.to_csv(index=False).encode('utf-8'),
    file_name="audit_log.csv",
    mime="text/csv",
    help="Export the full audit log for compliance reviews."
)
st.download_button(
    label="Download Posts Data as CSV",
    data=posts_df.to_csv(index=False).encode('utf-8'),
    file_name="posts_data.csv",
    mime="text/csv",
    help="Export all processed posts data for further analysis."
)
st.info("This provides the raw data for the 'Evidence Pack', including SQL Audit Logs (exported as CSV here for simplicity) as required by the proposal for regulatory compliance.")
