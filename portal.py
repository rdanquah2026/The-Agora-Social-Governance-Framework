import streamlit as st
import sqlite3
import pandas as pd 
import uuid

# Mock Notification Service (Visible Output 6)
def send_mock_notification(post_id, decision, rationale):
    print(f"--- MOCK NOTIFICATION SERVICE ---")
    print(f"Decision for Post ID '{post_id}' was '{decision}'.")
    print(f"Rationale: '{rationale}'")
    print(f"Triggering downstream action (e.g., remove post, publish post, flag user).\n")

    # Optionally, log to a file for a more tangible "evidence" artifact
    with open("mock_notifications.log", "a") as f:
        f.write(f"[{pd.Timestamp.now()}] Post ID: {post_id}, Decision: {decision}, Rationale: {rationale}\n")


# Set up the page
st.set_page_config(page_title="Agora Adjudication Portal", layout="wide")
st.title("🛡️ Agora Social: Human Adjudication Portal")

# Sidebar - "Policy Sidebar" mentioned in your proposal
st.sidebar.header("Current Policy Guidelines")
st.sidebar.info(
    "**Version 2.1**\n\n"
    "- **Harassment:** Direct threats are immediate removals.\n"
    "- **Sarcasm/Slang:** Context matters. If not genuinely harmful, KEEP.\n"
)

# Connect to database and fetch posts pending review
conn = sqlite3.connect('agora_registry.db')
query = "SELECT * FROM POSTS WHERE routing_decision = 'PENDING_REVIEW'"
df = pd.read_sql(query, conn)

if df.empty:
    st.success("🎉 The review queue is empty! Great job.")
else:
    st.warning(f"You have {len(df)} post(s) in the review queue.")
    
    # Display the first post in the queue
    post_to_review = df.iloc[0]
    
    st.subheader("Reviewer Context")
    st.write(f"**Raw Post:** {post_to_review['content']}")
    st.write(f"**AI Confidence Score:** {post_to_review['ai_score']} (Triggered Governance Lock)")
    
    st.divider()
    
    # The "Forced Rationale" Control
    st.subheader("Make a Decision")
    justification = st.selectbox(
        "Select Policy Justification (Required):",
        ["", "Contextual Sarcasm - Non-Violating", "Direct Threat - Violating", "Slang/AAVE - Non-Violating"]
    )
    
    rationale_text = st.text_area("Type a short rationale in your own words:")
    
    col1, col2 = st.columns(2)
    
    # This is the correct block for the "Approve" button
    if st.button("✅ Approve (Keep Post)"):
        if justification == "":
            st.error("Stop! You must select a justification before deciding.")
        else:
            cursor = conn.cursor()
            # 1. Add to Audit Log
            cursor.execute('''
                INSERT INTO AUDIT_LOG (log_id, post_id, human_label, reviewer_rationale)
                VALUES (?, ?, ?, ?)
            ''', (str(uuid.uuid4()), post_to_review['post_id'], 'APPROVED', justification + " - " + rationale_text))
            
            # 2. Update Post status so it leaves the queue
            cursor.execute("UPDATE POSTS SET routing_decision = 'REVIEWED' WHERE post_id = ?", (post_to_review['post_id'],))
            conn.commit()
            st.success("Decision logged! Refresh the page for the next post.")
            
            # --- THIS IS WHERE THE send_mock_notification CALL SHOULD BE ---
            send_mock_notification(post_to_review['post_id'], 'APPROVED', justification + " - " + rationale_text)

conn.close()
