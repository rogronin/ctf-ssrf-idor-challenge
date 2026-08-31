import sqlite3
import os

FLAG = os.environ.get("CTF_FLAG", "FLAG{ssrf_leads_to_idor_internal_pivot}")

conn = sqlite3.connect("documents.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY,
    owner TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL
)
""")

c.execute("DELETE FROM documents")
c.executemany(
    "INSERT INTO documents (id, owner, title, content) VALUES (?, ?, ?, ?)",
    [
        (3001, "alice",  "Team Lunch Notes",       "Let's get pizza on Friday, everyone chip in ₹100."),
        (3002, "bob",    "Q3 Planning Draft",      "Draft roadmap - not finalized, don't share externally."),
        (3003, "carol",  "Standup Notes 04/12",    "Discussed sprint velocity, nothing blocking."),
        (3004, "steve",  "Expense Report",         "Flight + hotel for conference, submitted for approval."),
        (3005, "dave",   "Onboarding Checklist",   "Set up laptop, read wiki."),
        (3006, "admin",  "Service Credentials Backup", FLAG),
    ]
)

conn.commit()
conn.close()
print("Database initialized with sample documents.")