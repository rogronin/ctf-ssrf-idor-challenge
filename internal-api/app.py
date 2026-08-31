from flask import Flask, jsonify, abort, request
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("documents.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def root():
    return jsonify({
        "service": "internal-document-api",
        "message": "See /internal/health for status.",
        "endpoints": ["/internal/health"]
    })
@app.route("/internal/health", strict_slashes=False)
def health():
    return jsonify({
        "status": "ok",
        "service": "document-api",
        "see_also": "/internal/profile"
    })
@app.route("/internal/profile", strict_slashes=False)
def profile():
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) AS c FROM documents").fetchone()["c"]
    conn.close()
    return jsonify({
        "service": "internal-document-api",
        "version": "1.0",
        "description": "Internal document storage service. Not for external access.",
        "document_count": total,
        "see_also": "L2ludGVybmFsL2RvY3VtZW50cw=="
    })

@app.route("/internal/documents", strict_slashes=False)
def list_documents():
    # NOTE: this filter is meant to hide admin-owned documents from casual
    # browsing. It does NOT protect the detail endpoint below - that's the bug.
    conn = get_db()
    rows = conn.execute(
        "SELECT id, owner, title FROM documents WHERE owner != 'admin'"
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route("/internal/documents/<int:doc_id>")
def get_document(doc_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM documents WHERE id = ?", (doc_id,)).fetchone()
    conn.close()

    if row is None:
        abort(404)

    requester = request.headers.get("X-User", "internal-service")

    if requester != "internal-service" and row["owner"] != requester:
        abort(403)

    return jsonify(dict(row))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)