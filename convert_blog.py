import markdown
import io

md_path = "BLOG_POST.md"
html_path = "BLOG_POST.html"

with io.open(md_path, "r", encoding="utf-8") as f:
    md_text = f.read()

body = markdown.markdown(md_text, extensions=["fenced_code", "tables", "codehilite"])

html_full = (
    """<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<title>Blog Post - Rekomendasi Kuliner Indonesia</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{font:16px/1.7 system-ui,Segoe UI,Roboto,sans-serif;margin:0;padding:40px;background:#f8fafc;color:#111827}
main{max-width:800px;margin:auto;background:#fff;padding:40px;border-radius:12px;box-shadow:0 10px 30px rgba(2,6,23,.06)}
h1{font-size:32px;line-height:1.25;margin-top:0}
h2{font-size:24px;line-height:1.3;margin-top:32px;padding-bottom:6px;border-bottom:1px solid #e5e7eb}
h3{font-size:20px;line-height:1.35;margin-top:24px}
pre,code{font-family:ui-monospace,Consolas,monospace}
pre{background:#0f172a;color:#e2e8f0;padding:16px;border-radius:8px;overflow:auto;font-size:14px;line-height:1.5}
code{background:#eef2f7;color:#be123c;padding:2px 5px;border-radius:4px;font-size:.92em}
pre code{background:transparent;color:inherit;padding:0;border-radius:0}
table{border-collapse:collapse;width:100%;margin:16px 0}
th,td{border:1px solid #e5e7eb;padding:8px 12px;text-align:left}
th{background:#f9fafb}
ul,ol{padding-left:24px}
li{margin:6px 0}
a{color:#2563eb}
</style>
</head>
<body>
<main>
"""
    + body
    + """
</main>
</body>
</html>"""
)

with io.open(html_path, "w", encoding="utf-8") as f:
    f.write(html_full)

print("OK", html_path, len(html_full))
