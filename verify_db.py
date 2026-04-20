import sqlite3

def verify_database():
    conn = sqlite3.connect('agora_registry.db')
    cursor = conn.cursor()

    print("--- Verifying POSTS Table ---")
    cursor.execute("SELECT * FROM POSTS")
    posts = cursor.fetchall()
    for post in posts:
        print(post)

    print("\n--- Verifying AUDIT_LOG Table ---")
    cursor.execute("SELECT * FROM AUDIT_LOG")
    audit_logs = cursor.fetchall()
    for log in audit_logs:
        print(log)

    conn.close()
    print("\nDatabase verification complete.")

if __name__ == "__main__":
    verify_database()
