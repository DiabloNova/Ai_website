import os
import subprocess
import time
import http.server
import socketserver
import threading
from playwright.sync_api import sync_playwright

PORT = 8000

class QuietSimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress logging server requests
        pass

def start_server():
    handler = QuietSimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving HTTP on port {PORT}")
        httpd.serve_forever()

# Start HTTP server in a separate thread
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# Give server a moment to spin up
time.Thread = None
time.sleep(2)

print("Launching Playwright browser...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_viewport_size({"width": 1440, "height": 900})

    print(f"Navigating to http://localhost:{PORT}/index.html")
    page.goto(f"http://localhost:{PORT}/index.html")

    # Wait for page elements to render and stabilize
    page.wait_for_timeout(3000)

    # Optional interaction to show dropdown state in screenshot
    print("Clicking dropdown selector...")
    page.click("#modelTrigger")
    page.wait_for_timeout(500)

    print("Capturing screenshot...")
    page.screenshot(path="verified_ui_output.png")
    print("Screenshot saved to verified_ui_output.png")

    browser.close()

print("Verification complete.")
