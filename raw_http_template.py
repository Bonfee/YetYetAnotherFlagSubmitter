raw_template = """PUT /flags HTTP/1.1
Host: 10.1.0.2:80
User-Agent: python-requests/2.22.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
X-Team-Token: 4242424242424242
Content-Length: 36
Content-Type: application/json

["FLAG_PLACEHOLDER"]"""

# Every FLAG_PLACEHOLDER occurence will be replaced with the actual flag 
# Content-Length must be set manually:
# For example, if flags are 32 chars long, then [" + 32 chars + "] = 36