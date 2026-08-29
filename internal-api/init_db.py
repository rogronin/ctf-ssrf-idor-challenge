import sqlite3

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
        (3004, "steve",    "Expense Report",         "Flight + hotel for conference, submitted for approval."),
        (3005, "dave",   "Onboarding Checklist",   "Set up laptop, read wiki."),
        (3006, "admin",  "Service Credentials Backup", "LUN4R{SSRF_le4ds_t0_id0r_1nternal_p1v0t}"),
    ]
)

conn.commit()
conn.close()
print("Database initialized with sample documents.")