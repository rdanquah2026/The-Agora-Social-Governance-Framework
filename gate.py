import sqlite3
import uuid
import os
from openai import OpenAI # Import the OpenAI library

# Initialize OpenAI client with API key from environment variable
# It will automatically look for OPENAI_API_KEY
client = OpenAI()

def call_openai_moderation_api(text_content):
    try:
        # Call the Moderation API
        response = client.moderations.create(input=text_content)
        
        # The Moderation API returns a list of results. We usually care about the first one.
        moderation_result = response.results[0]
        
        # Check if any category was flagged
        flagged = moderation_result.flagged
        
        # Get the maximum confidence score across all categories
        # Your proposal mentions "raw category_scores for 11 distinct harm categories"
        category_scores = moderation_result.category_scores.model_dump()
        
        # Find the category with the highest score and its value
        if category_scores:
            max_score_category = max(category_scores, key=category_scores.get)
            max_score_value = category_scores[max_score_category]
        else:
            max_score_category = "neutral"
            max_score_value = 0.0

        return max_score_value, max_score_category, flagged

    except Exception as e:
        print(f"Error calling OpenAI Moderation API: {e}")
        # Fallback in case of API error: treat as uncertain and send to human
        return 0.5, "api_error", True # Force to PENDING_REVIEW


# This function acts as our "Risk Evaluator" and now calls the real API
def evaluate_and_route_post(content):
    # 1. Generate a unique ID for this post (required for audits)
    post_id = str(uuid.uuid4())
    
    # 2. Get real AI scores from OpenAI
    ai_score, category, _ = call_openai_moderation_api(content) # We don't use 'flagged' directly for routing here
    
    # 3. Apply the Governance Thresholds from your proposal
    # These are for demonstration; actual thresholds would be fine-tuned based on real data
    if ai_score < 0.45:
        routing_decision = "AUTO_APPROVED"
    elif ai_score > 0.85:
        routing_decision = "AUTO_REJECTED"
    else:
        routing_decision = "PENDING_REVIEW" # This goes to the human!

    # 4. Save the decision to our database
    conn = sqlite3.connect('agora_registry.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO POSTS (post_id, content, ai_score, category, routing_decision)
        VALUES (?, ?, ?, ?, ?)
    ''', (post_id, content, ai_score, category, routing_decision))
    
    conn.commit()
    conn.close()

    print(f"Processed Post: '{content}'")
    print(f"AI Score: {ai_score:.4f} (Category: {category}) -> Decision: {routing_decision}\n")

# Let's test it with some synthetic data (Dataset 2 from your proposal)
if __name__ == "__main__":
    print("--- Running Safety Valve Routing Gate with OpenAI API ---")
    
    # Clear previous posts for a fresh run
    conn = sqlite3.connect('agora_registry.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM POSTS")
    cursor.execute("DELETE FROM AUDIT_LOG")
    conn.commit()
    conn.close()
    print("Cleared previous posts from database.\n")

    # Post 1: Clearly safe
    evaluate_and_route_post("I love the new coffee shop downtown! The food is amazing.")
    
    # Post 2: Potentially harmful - OpenAI should give a high score
    evaluate_and_route_post("I'm going to kill myself. I feel so alone.")
    
    # Post 3: The "Gray Area" (Sarcasm/Slang) - OpenAI might give a medium score, needs human review
    evaluate_and_route_post("Yeah, totally gonna rob a bank later. 🙄 #justkidding #notserious")

    # Post 4: Another "Gray Area" or potentially flagged depending on OpenAI's current model
    evaluate_and_route_post("This idiot is spouting nonsense again on social media.")
