# tools/llm_correct.py
import argparse
import os
import sys
from pathlib import Path

# Reuse the shared OpenAI client from your app
try:
    from core.llm import client  # our centralized client (recommended)
except Exception:
    # Fallback if running standalone without project imports
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY (or oai_key).")
    client = OpenAI(api_key=api_key)

MODES = {"light", "medium", "strict"}

def build_system_prompt(mode: str) -> str:
    if mode == "light":
        return (
            "You are an expert copy editor. Correct grammar, spelling, punctuation, and minor clarity issues. "
            "Keep original tone, voice, length, structure, and formatting. Do not add or remove content. "
            "Return only corrected Markdown, no extra commentary."
        )
    if mode == "strict":
        return (
            "You are an expert editor. Heavily improve clarity, flow, structure, and concision while preserving meaning. "
            "Fix grammar and style; reorganize sections; add headings and bullets where beneficial; remove redundancy. "
            "Do not invent facts. Keep all technical details. Return only corrected Markdown, no extra commentary."
        )
    # medium (default)
    return (
        "You are an expert editor. Improve clarity and style while preserving meaning and structure. "
        "Fix grammar, wording, and formatting. Avoid hallucinations. "
        "Return only corrected Markdown, no extra commentary."
    )

def correct_chunk(text: str, model: str, mode: str) -> str:
    system = build_system_prompt(mode)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": text},
        ],
        max_tokens=2000,  # adjust if needed
    )
    return resp.choices[0].message.content

def chunk_markdown(text: str, target_size: int = 6000) -> list[str]:
    """
    Naive chunker: split at paragraph boundaries near target_size chars.
    Keeps Markdown formatting reasonably intact.
    """
    if len(text) <= target_size:
        return [text]
    chunks, buf = [], []
    size = 0
    for para in text.split("\n\n"):
        p = para + "\n\n"
        if size + len(p) > target_size and buf:
            chunks.append("".join(buf))
            buf, size = [p], len(p)
        else:
            buf.append(p); size += len(p)
    if buf:
        chunks.append("".join(buf))
    return chunks

def correct_markdown(full_text: str, model: str, mode: str) -> str:
    chunks = chunk_markdown(full_text)
    corrected = []
    for i, ch in enumerate(chunks, 1):
        corrected.append(correct_chunk(ch, model, mode))
    return "".join(corrected)

def main():
    parser = argparse.ArgumentParser(
        prog="llm-correct",
        description="Correct a Markdown file using OpenAI."
    )
    parser.add_argument("path", help="Path to the Markdown file.")
    parser.add_argument("--model", default="gpt-4o-mini",
                        help="OpenAI model (e.g., gpt-4o, gpt-4o-mini).")
    parser.add_argument("--mode", default="medium", choices=list(MODES),
                        help="Correction strength: light | medium | strict.")
    parser.add_argument("--write", action="store_true",
                        help="Overwrite the source file with corrected output.")
    parser.add_argument("--out", type=str, default=None,
                        help="Write to this output path instead of stdout.")
    args = parser.parse_args()

    src = Path(args.path)
    if not src.exists():
        print(f"❌ File not found: {src}", file=sys.stderr)
        sys.exit(1)

    text = src.read_text(encoding="utf-8")
    corrected = correct_markdown(text, model=args.model, mode=args.mode)

    if args.write and args.out:
        print("❌ Use either --write or --out, not both.", file=sys.stderr)
        sys.exit(2)

    if args.write:
        backup = src.with_suffix(src.suffix + ".bak")
        backup.write_text(text, encoding="utf-8")
        src.write_text(corrected, encoding="utf-8")
        print(f"✅ Corrected in place. Backup saved to {backup}")
    elif args.out:
        out_path = Path(args.out)
        out_path.write_text(corrected, encoding="utf-8")
        print(f"✅ Wrote corrected file to {out_path}")
    else:
        # stdout (pipe to a file if you want)
        sys.stdout.write(corrected)

if __name__ == "__main__":
    main()
