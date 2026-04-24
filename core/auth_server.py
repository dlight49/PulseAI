import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# This is a lightweight OAuth callback server.
# When a user logs in via Meta or Google, they are redirected here with a secure code.

HOST_NAME = "localhost"
SERVER_PORT = 8000

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == "/auth/callback":
            # Extract the authorization code from the URL
            query_components = parse_qs(parsed_path.query)
            auth_code = query_components.get('code', [None])[0]
            
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            if auth_code:
                print(f"\n[🔒 SECURE SYSTEM] OAuth Code Received: {auth_code[:10]}... (truncated for security)")
                # In a real app, we exchange this code for an Access Token here.
                html_response = """
                <html>
                    <head><title>Pulse AI - Auth Success</title></head>
                    <body style="font-family: Arial; text-align: center; margin-top: 50px;">
                        <h2 style="color: green;">✅ Authentication Successful!</h2>
                        <p>Pulse AI has securely received your token. You can close this window.</p>
                    </body>
                </html>
                """
                self.wfile.write(bytes(html_response, "utf-8"))
            else:
                print("\n[❌ SECURE SYSTEM] OAuth Failed: No code received.")
                self.wfile.write(bytes("<html><body><h2>❌ Authentication Failed.</h2></body></html>", "utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def start_server():
    webServer = HTTPServer((HOST_NAME, SERVER_PORT), OAuthHandler)
    print(f"🛡️  Pulse AI Secure Token Server started at http://{HOST_NAME}:{SERVER_PORT}")
    print("Waiting for OAuth callbacks on /auth/callback...")
    
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    
    webServer.server_close()
    print("Server stopped.")

if __name__ == "__main__":
    start_server()
