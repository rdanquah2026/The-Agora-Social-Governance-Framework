import sqlite3
import pytest

# Test 1: Check if the Database correctly stored the 'Uncertainty Zone' posts
def test_uncertainty_zone_routing():
    """
    Professor, this test verifies that posts with a score of 0.5 
    (the 'Gray Area') are correctly sitting in the REVIEWED status.
    """
    conn = sqlite3.connect('agora_registry.db')
    cursor = conn.cursor()
    
    # We look for the posts we processed earlier
    cursor.execute("SELECT routing_decision FROM POSTS WHERE ai_score = 0.5")
    results = cursor.fetchall()
    
    assert len(results) > 0, "No posts found in database. Run gate.py first!"
    
    for row in results:
        # Every post with 0.5 MUST have been sent to a human
        assert row[0] in ['PENDING_REVIEW', 'REVIEWED']
        
    conn.close()

# Test 2: Verify the Audit Log has rationales (The 'Forced Rationale' control)
def test_audit_log_completeness():
    """
    This verifies that our 'Persistence Layer' captured the rationales 
    we typed into the portal.
    """
    conn = sqlite3.connect('agora_registry.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT reviewer_rationale FROM AUDIT_LOG")
    logs = cursor.fetchall()
    
    assert len(logs) > 0, "Audit log is empty! Process posts in the portal first."
    
    for log in logs:
        # Check that the rationale isn't empty
        assert len(log[0]) > 10, "Rationale is too short to be valid governance evidence."
        
    conn.close()
