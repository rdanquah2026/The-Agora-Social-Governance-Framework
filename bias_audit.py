import pandas as pd
import os

def generate_bias_audit_report(): # Renamed the function to be more descriptive
    
    # 1. Simulating our Synthetic Dataset 
    # 1 = Flagged by AI, 0 = Passed by AI (Safe)
    data = {
        'post_id': range(1, 101),
        'Linguistic_Cluster': ['Standard English']*50 + ['AAVE']*30 + ['Gen-Z Slang']*20,
        'AI_Flagged': 
            [0]*45 + [1]*5 +   # Standard English: 10% flag rate (90% pass)
            [0]*20 + [1]*10 +  # AAVE: 33% flag rate (67% pass)
            [0]*15 + [1]*5     # Gen-Z: 25% flag rate (75% pass)
    }
    df = pd.DataFrame(data)

    # 2. Calculate the "Pass Rate" (Not Flagged) for each group
    pass_rates = df[df['AI_Flagged'] == 0].groupby('Linguistic_Cluster').size() / df.groupby('Linguistic_Cluster').size()
    
    standard_english_rate = pass_rates.get('Standard English', 1.0)
    aave_rate = pass_rates.get('AAVE', 1.0)
    
    # 3. Calculate Disparate Impact Ratio (The Fairlearn Metric)
    # Ratio = (Pass rate of minority group) / (Pass rate of majority group)
    disparate_impact_ratio = aave_rate / standard_english_rate
    
    # 4. Generate the Report String
    report_content = f"""# Algorithmic Fairness & Bias Parity Report

**Methodology:** Custom Pandas Disparate Impact Calculation (Engineering Pivot from Fairlearn)

## 1. AI Pass Rates by Linguistic Cluster
* Standard English Pass Rate: {standard_english_rate:.1%}
* AAVE Pass Rate: {aave_rate:.1%}

## 2. Disparate Impact Ratio Analysis
* **Calculated Ratio (AAVE vs Standard English): {disparate_impact_ratio:.2f}**
* **Target Ratio:** > 0.80 (As defined in project proposal)

## 3. Governance Conclusion
The Disparate Impact Ratio is {disparate_impact_ratio:.2f}, which is **BELOW** our target of 0.80. 
This indicates a systemic bias where the AI is flagging AAVE content at a disproportionately higher rate than Standard English.

**Required Action:** This triggers a mandatory "Policy Misalignment" review. The AI routing thresholds for specific linguistic clusters must be adjusted, or the model requires fine-tuning before full production deployment.
"""
    
    # 5. Also save directly to the Evidence Pack for offline reference
    os.makedirs("Evidence_Pack", exist_ok=True)
    file_path = os.path.join("Evidence_Pack", "Bias_Parity_Report.md")
    with open(file_path, "w") as f:
        f.write(report_content)
        
    print(f"✅ Bias report successfully saved to {file_path}")
    
    return report_content # THIS IS THE KEY CHANGE - returns the report string

if __name__ == "__main__":
    # If run directly, print the report as before
    report = generate_bias_audit_report()
    print(report)
