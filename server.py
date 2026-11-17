#!/usr/bin/env python3
"""
Lightweight HTTP Server & REST API for DLIMS Punjab Driving License Renewal Calculator
"""

import http.server
import socketserver
import urllib.parse
import json
import os
import sys

from calculator import calculate_renewal, RATES, COURIER_FEE, FACILITATOR_FEE, PLATFORM_FEE

PORT = int(os.environ.get("PORT", 8080))
WEB_DIR = os.path.dirname(os.path.abspath(__file__))

class DLIMSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # API: /api/calculate
        if path == "/api/calculate":
            self.handle_api_calculate(query)
            return

        # API: /api/rates
        if path == "/api/rates":
            self.handle_api_rates()
            return

        super().do_GET()

    def handle_api_calculate(self, query):
        try:
            service = query.get("service", ["regular"])[0].lower()
            cat = query.get("cat", ["Car/Jeep"])[0]
            issue = query.get("issue", [None])[0]
            expiry = query.get("expiry", [None])[0]
            years = int(query.get("years", [5])[0])
            fac = query.get("facilitator", ["true"])[0].lower() in ["true", "1", "yes"]
            cour = query.get("courier", ["true"])[0].lower() in ["true", "1", "yes"]

            result = calculate_renewal(
                service=service,
                category=cat,
                issue_date=issue,
                expiry_date=expiry,
                years=years,
                include_facilitator=fac,
                include_courier=cour
            )

            response_bytes = json.dumps({"status": "success", "data": result}, indent=2).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(response_bytes)))
            self.end_headers()
            self.wfile.write(response_bytes)

        except Exception as e:
            err_bytes = json.dumps({"status": "error", "message": str(e)}).encode("utf-8")
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(err_bytes)))
            self.end_headers()
            self.wfile.write(err_bytes)

    def handle_api_rates(self):
        data = {
            "rates": RATES,
            "courier_fee": COURIER_FEE,
            "facilitator_fee": FACILITATOR_FEE,
            "platform_fee": PLATFORM_FEE,
            "source": "https://dlims.punjab.gov.pk/fee_structure & Dastak Punjab"
        }
        data_bytes = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(data_bytes)))
        self.end_headers()
        self.wfile.write(data_bytes)

def run_server(port=PORT):
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), DLIMSRequestHandler) as httpd:
        print(f"Server listening on http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    run_server(port)
