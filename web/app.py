from flask import Flask, render_template, request, send_file, make_response
from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
import io

app = Flask(__name__)

BLOCKED_SUBSTRINGS = ["localhost", "127.0.0.1"]
ALLOWED_SCHEMES = {"http", "https"}
INTERNAL_ROUTE_HINT = "internal-api:8000"  # leaked via debug header on failures

def is_blocked(url: str) -> bool:
    lowered = url.lower()
    return any(bad in lowered for bad in BLOCKED_SUBSTRINGS)

def has_valid_scheme(url: str) -> bool:
    try:
        parsed = urlparse(url)
    except ValueError:
        return False
    return parsed.scheme in ALLOWED_SCHEMES

def error_response(message, status):
    resp = make_response(message, status)
    resp.headers["X-Debug-Route"] = f"web -> {INTERNAL_ROUTE_HINT}"
    return resp

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    target_url = request.form.get("url")

    if not target_url:
        return error_response("Please provide a URL.", 400)

    if not has_valid_scheme(target_url):
        return error_response("Only http:// and https:// URLs are allowed.", 400)

    if is_blocked(target_url):
        return error_response("This URL cannot be processed.", 403)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(target_url, timeout=15000)
            pdf_bytes = page.pdf(format="A4")
            browser.close()
    except Exception as e:
        print(f"CONVERSION ERROR: {e}")
        return error_response("Unable to convert this URL. Please check it and try again.", 500)

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name="converted.pdf"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)