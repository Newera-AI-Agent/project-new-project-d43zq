import urllib.request, json

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

for url in [
    "http://2130706433/",
    "http://0x7f000001/",
    "http://0177.0.0.1/",
    "http://metadata.google.internal/",
    "http://127.0.0.1/",
    "http://10.0.0.1/",
    "http://1.1.1.1/",
]:
    test(url)
