import os, sys
from pathlib import Path
from openai import OpenAI

MODEL = "gpt-4.1-mini"  # use "gpt-4.1" for maximum quality

SYSTEM = """You are a senior full-stack engineer.
Repo: React/Vite frontend (/frontend) + FastAPI backend (/backend).
Goals:
- Diagnose and fix build/type/test issues.
- Correct API base usage (import.meta.env.VITE_API_BASE) in frontend.
- Add minimal FastAPI CORS if missing.
- Keep changes minimal and safe.
Return ONLY unified diff patches in ```diff fences, with correct paths from repo root.
"""

PROMPT = """Context:


Produce one or more UNIFIED DIFF patches that:
- Make /frontend build with Vite (using import.meta.env.VITE_API_BASE).
- Make API calls use ${import.meta.env.VITE_API_BASE}/cars (or correct endpoints).
- Fix obvious TS/JS/Python errors and minimal config issues.
- If needed, add dependencies (package.json / requirements.txt) in separate diff hunks.
Only output ```diff blocks. No prose outside fences.
"""

def main():
    ctx_path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    ctx = ctx_path.read_text(encoding="utf-8")[:180000] if (ctx_path and ctx_path.exists()) else ""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Missing OPENAI_API_KEY in env", file=sys.stderr)
        sys.exit(1)
    client = OpenAI(api_key=api_key)
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": PROMPT.format(ctx=ctx)},
        ],
        temperature=0.2,
    )
    print(resp.choices[0].message.content.strip())

if __name__ == "__main__":
    main()
