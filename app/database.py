import mysql.connector
import os
from datetime import datetime

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "resume_screener")
    )

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS screening_results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            filename VARCHAR(255),
            score INT,
            matched_skills TEXT,
            missing_skills TEXT,
            improvements TEXT,
            strengths TEXT,
            summary TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def save_result(filename: str, result: dict):
    import json
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO screening_results 
        (filename, score, matched_skills, missing_skills, improvements, strengths, summary)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        filename,
        result.get("score"),
        json.dumps(result.get("matched_skills", [])),
        json.dumps(result.get("missing_skills", [])),
        json.dumps(result.get("improvements", [])),
        json.dumps(result.get("strengths", [])),
        result.get("summary", "")
    ))
    conn.commit()
    cursor.close()
    conn.close()

def get_history(limit: int = 10):
    import json
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM screening_results ORDER BY created_at DESC LIMIT %s", (limit,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    for row in rows:
        for field in ["matched_skills", "missing_skills", "improvements", "strengths"]:
            if row.get(field):
                row[field] = json.loads(row[field])
        if row.get("created_at"):
            row["created_at"] = str(row["created_at"])
    return rows
