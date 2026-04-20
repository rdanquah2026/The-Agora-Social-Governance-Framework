import sqlite3

def create_database():
    # This creates a file named 'agora_registry.db' in your folder
    conn = sqlite3.connect('agora_registry.db')
    cursor = conn.cursor()

    # Create the POSTS table to store the initial AI scores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS POSTS (
            post_id TEXT PRIMARY KEY,
            content TEXT,
            ai_score REAL,
            category TEXT,
            routing_decision TEXT
        )
    ''')

    # Create the AUDIT_LOG table to store human decisions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS AUDIT_LOG (
            log_id TEXT PRIMARY KEY,
            post_id TEXT,
            human_label TEXT,
            reviewer_rationale TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(post_id) REFERENCES POSTS(post_id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Governance Registry Database created successfully!")

if __name__ == "__main__":
    create_database()
