# Threshold Sensitivity Analysis

**Objective:** Determine the optimal routing gate thresholds to balance AI automation with human reviewer capacity.

**Current Configuration (Balanced):**
* Auto-Approve: < 0.45
* Human Review (Uncertainty Zone): 0.45 to 0.85
* Auto-Reject: > 0.85

**Analysis of Alternatives:**
1. **Conservative (0.30 - 0.90):** 
   * *Impact:* Captures almost all borderline content.
   * *Risk:* Overwhelms the Human Adjudication Portal, leading to reviewer burnout and massive backlogs. Not scalable.
2. **Aggressive (0.70 - 0.80):** 
   * *Impact:* Highly efficient, minimal human review required.
   * *Risk:* High probability of "Policy Misalignment." The AI will auto-approve moderately toxic content and auto-reject nuanced sarcasm, leading to user complaints and regulatory risk.

**Conclusion:** The 0.45 - 0.85 threshold remains the most defensible standard. As demonstrated in our `mock_notifications.log` and database, it correctly trapped nuanced sarcasm and subtle threats that the OpenAI API flagged with a medium confidence score during our API error simulation.
