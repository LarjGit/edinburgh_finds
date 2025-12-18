import ssl, socket, requests

HOST = "api.perplexity.ai"
PORT = 443

print("=== RAW SSL TEST ===")
ctx = ssl.create_default_context()
with socket.create_connection((HOST, PORT)) as sock:
    with ctx.wrap_socket(sock, server_hostname=HOST) as ssock:
        print("Connected using TLS version:", ssock.version())
        print("Cipher:", ssock.cipher())
        ssock.sendall(b"GET /chat/completions HTTP/1.1\r\nHost: api.perplexity.ai\r\n\r\n")
        data = ssock.recv(200)
        print("Response snippet:", data.decode(errors="ignore").splitlines()[0])

print("\n=== REQUESTS TEST ===")
try:
    r = requests.get("https://api.perplexity.ai/chat/completions")
    print("Requests succeeded, status code:", r.status_code)
    print("Response snippet:", r.text[:80])
except Exception as e:
    print("Requests failed:", repr(e))
