import re

with open('docs/progress.toml', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'status = "todo"', 'status = "done", done = "2026-09-29"', content)

with open('docs/progress.toml', 'w', encoding='utf-8') as f:
    f.write(content)
