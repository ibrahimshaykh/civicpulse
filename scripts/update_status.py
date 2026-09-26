#!/usr/bin/env python3
"""Render STATUS.md from docs/progress.toml.

    python scripts/update_status.py           # rewrite STATUS.md
    python scripts/update_status.py --check   # exit 1 if STATUS.md is stale (used in CI)

Python 3.11+ (uses the standard-library tomllib). No third-party packages.
Output is deterministic: it depends only on progress.toml, never on the clock,
so --check is stable across machines.
"""

from __future__ import annotations

import argparse
import math
import sys
import tomllib
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "progress.toml"
OUT = ROOT / "STATUS.md"

BONUS_CAP = 15
# The brief's rubric (§4). NOTE: these section totals add up to 175 points, while the
# brief's header says "Total Marks 150". Until the instructor clarifies, STATUS.md reports
# marks scaled to meta.total_marks (default 150) and also shows the raw rubric points.
# If the instructor says the real total is 175, set total_marks = 175 in progress.toml.
SECTIONS = {
    "A": ("Collaboration and version control", 15),
    "B": ("Frontend", 18),
    "C": ("Backend", 25),
    "D": ("Data layer", 12),
    "E": ("Cache layer", 10),
    "F": ("AI layer", 25),
    "G": ("Docker and Compose", 15),
    "H": ("Kubernetes", 20),
    "I": ("CI/CD", 20),
    "J": ("Documentation", 15),
}
PHASES = [
    ("C0", "Setup and contract"), ("FE", "Frontend"), ("DB", "Data layer"), ("BE", "Backend"),
    ("CA", "Cache"), ("AI", "AI layer"), ("DK", "Docker and Compose"), ("K8", "Kubernetes"),
    ("CI", "CI/CD"), ("DOC", "Documentation"), ("EV", "Evidence"), ("SUB", "Submission"),
    ("OB", "Observability"),
]
RUBRIC_POINTS = sum(total for _, total in SECTIONS.values())
STATUSES = ("todo", "in_progress", "done", "blocked")
OWNERS = ("A", "B", "Both")
WHO = {
    "claude": "Claude",
    "claude+you": "Claude builds, you run it",
    "you": "you, step by step",
    "partner": "your partner",
}
ICON = {"done": "✅", "in_progress": "🔄", "todo": "⬜", "blocked": "⛔"}
BAR_WIDTH = 30


class ProgressError(Exception):
    pass


def bar(frac: float, width: int = BAR_WIDTH) -> str:
    frac = min(max(frac, 0.0), 1.0)
    filled = math.floor(frac * width)
    return "█" * filled + "░" * (width - filled)


def pct(num: int, den: int) -> int:
    # floor, so the bar never shows 100% before the last item is really done
    return math.floor(100 * num / den) if den else 0


def fmt(x: float) -> str:
    s = f"{x:.1f}"
    return s[:-2] if s.endswith(".0") else s


def phase_of(task_id: str) -> str:
    return task_id.split("-", 1)[0]


def load() -> dict:
    try:
        with SRC.open("rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        raise ProgressError(f"missing {SRC.relative_to(ROOT)}") from None
    except tomllib.TOMLDecodeError as e:
        raise ProgressError(f"{SRC.relative_to(ROOT)} is not valid TOML: {e}") from None


def validate(data: dict) -> None:
    errors: list[str] = []
    tasks = data.get("tasks", [])
    for key in ("tasks", "rubric"):
        if not data.get(key):
            errors.append(f"no '{key}' found at the top level (in TOML, keys placed after a [table] header belong to that table)")
    ids = [t.get("id") for t in tasks]
    dupes = [i for i, n in Counter(ids).items() if n > 1]
    if dupes:
        errors.append(f"duplicate task ids: {', '.join(dupes)}")
    known = set(ids)
    known_phases = {p for p, _ in PHASES}
    for t in tasks:
        tid = t.get("id", "?")
        for key in ("id", "title", "owner", "status", "week", "who"):
            if key not in t:
                errors.append(f"task {tid}: missing '{key}'")
        if t.get("status") not in STATUSES:
            errors.append(f"task {tid}: status must be one of {STATUSES}, got {t.get('status')!r}")
        if t.get("owner") not in OWNERS:
            errors.append(f"task {tid}: owner must be one of {OWNERS}, got {t.get('owner')!r}")
        if t.get("who") not in WHO:
            errors.append(f"task {tid}: who must be one of {tuple(WHO)}, got {t.get('who')!r}")
        if t.get("status") == "done" and not t.get("done"):
            errors.append(f"task {tid}: done tasks need done = \"YYYY-MM-DD\"")
        if phase_of(tid) not in known_phases:
            errors.append(f"task {tid}: unknown id prefix {phase_of(tid)!r}")
    for kind in ("rubric", "bonus", "submission"):
        for r in data.get(kind, []):
            for req in r.get("requires", []):
                if req not in known:
                    errors.append(f"{kind} {r.get('id')}: requires unknown task {req}")
            if not r.get("requires"):
                errors.append(f"{kind} {r.get('id')}: requires at least one task")
    by_section: Counter[str] = Counter()
    for r in data.get("rubric", []):
        if r.get("section") not in SECTIONS:
            errors.append(f"rubric {r.get('id')}: unknown section {r.get('section')!r}")
        by_section[r.get("section")] += r.get("marks", 0)
    for sec, (name, total) in SECTIONS.items():
        if by_section[sec] != total:
            errors.append(f"rubric section {sec} ({name}) sums to {by_section[sec]}, brief says {total}")
    if sum(by_section.values()) != RUBRIC_POINTS:
        errors.append(f"rubric lines total {sum(by_section.values())} points, the brief's sections total {RUBRIC_POINTS}")
    for n in data.get("needs_you", []):
        if n.get("task") and n["task"] not in known:
            errors.append(f"needs_you '{n.get('text', '')[:40]}': unknown task {n['task']}")
    if errors:
        raise ProgressError("progress.toml has problems:\n  - " + "\n  - ".join(errors))


def render(data: dict) -> str:
    meta = data.get("meta", {})
    tasks = data["tasks"]
    by_id = {t["id"]: t for t in tasks}
    core = [t for t in tasks if not t.get("bonus")]
    extra = [t for t in tasks if t.get("bonus")]
    done_core = [t for t in core if t["status"] == "done"]

    def is_done(tid: str) -> bool:
        return by_id[tid]["status"] == "done"

    def line_state(r: dict) -> str:
        n = sum(is_done(x) for x in r["requires"])
        if n == len(r["requires"]):
            return "done"
        if n or any(by_id[x]["status"] == "in_progress" for x in r["requires"]):
            return "in_progress"
        return "todo"

    rubric = data["rubric"]
    points = sum(r["marks"] for r in rubric if line_state(r) == "done")
    stated_total = int(meta.get("total_marks", 150))
    marks = points * stated_total / RUBRIC_POINTS
    bonus_marks = min(BONUS_CAP, sum(b["marks"] for b in data.get("bonus", []) if line_state(b) == "done"))

    out: list[str] = []
    w = out.append
    w(f"# {meta.get('project', 'Project')} — status")
    w("")
    w("> Generated from `docs/progress.toml` by `python scripts/update_status.py`. Edit the TOML, then regenerate. Don't edit this file by hand.")
    w(f"> Last updated: {meta.get('updated', 'unknown')}")
    w("")
    w("```text")
    w(f"Project progress  [{bar(len(done_core) / len(core))}]  {pct(len(done_core), len(core)):>3}%   "
      f"{len(done_core)} of {len(core)} core tasks done")
    scaled_note = "" if stated_total == RUBRIC_POINTS else f"  ({points} of {RUBRIC_POINTS} rubric points)"
    w(f"Marks secured     [{bar(points / RUBRIC_POINTS)}]  {pct(points, RUBRIC_POINTS):>3}%   "
      f"{fmt(marks)} of {stated_total} marks{scaled_note}")
    w("```")
    w("")
    if stated_total != RUBRIC_POINTS:
        w(f"> ⚠️ The brief's rubric sections add up to **{RUBRIC_POINTS}** points but its header says **{stated_total}** marks. "
          f"Marks above are scaled ×{stated_total}/{RUBRIC_POINTS} until the instructor confirms. "
          "If the real total is 175, set `total_marks = 175` in `docs/progress.toml`.")
        w("")
    w(f"Bonus secured: **{bonus_marks} of {BONUS_CAP}**. "
      "Marks are self-assessed and count a rubric line only when every task it needs is done. "
      "The final grade also applies the viva multiplier and the brief's automatic deductions.")
    w("")

    # per-partner
    w("| Partner | Core tasks done | Share of core tasks |")
    w("|---|---|---|")
    for owner, label in (("A", meta.get("partner_a", "Partner A")), ("B", meta.get("partner_b", "Partner B")),
                         ("Both", "Shared tasks")):
        mine = [t for t in core if t["owner"] == owner]
        d = sum(t["status"] == "done" for t in mine)
        w(f"| {label} | {d} of {len(mine)} | `{bar(d / len(mine) if mine else 0, 10)}` {pct(d, len(mine))}% |")
    w("")

    # marks by section
    w("## Marks by rubric section")
    w("")
    w("Raw rubric points, as printed in the brief.")
    w("")
    w("| Section | Secured | Out of | |")
    w("|---|---:|---:|---|")
    for sec, (name, total) in SECTIONS.items():
        got = sum(r["marks"] for r in rubric if r["section"] == sec and line_state(r) == "done")
        w(f"| {sec} · {name} | {got} | {total} | `{bar(got / total, 10)}` |")
    w(f"| **Total** | **{points}** | **{RUBRIC_POINTS}** | `{bar(points / RUBRIC_POINTS, 10)}` |")
    w("")

    # working on now
    w("## Working on now")
    w("")
    active = [t for t in tasks if t["status"] == "in_progress"]
    if active:
        for t in active:
            note = f" — {t['note']}" if t.get("note") else ""
            w(f"- 🔄 **{t['id']}** {t['title']} ({t['owner']}){note}")
    else:
        w("Nothing in progress right now.")
    w("")

    # needs you
    w("## Needs you")
    w("")
    needs = data.get("needs_you", [])
    blocked = [t for t in tasks if t["status"] == "blocked"]
    if not needs and not blocked:
        w("Nothing is waiting on you.")
    for n in needs:
        tag = f" _(needed for {n['task']})_" if n.get("task") else ""
        w(f"- [ ] {n['text']}{tag}")
    for t in blocked:
        why = t.get("note", "reason not recorded")
        w(f"- [ ] ⛔ **{t['id']}** {t['title']} is blocked: {why}")
    w("")

    # up next
    w("## Up next")
    w("")
    order = {t["id"]: i for i, t in enumerate(tasks)}
    todo = sorted((t for t in core if t["status"] == "todo"), key=lambda t: (t["week"], order[t["id"]]))
    for owner in ("A", "B"):
        nxt = [t for t in todo if t["owner"] in (owner, "Both")][:4]
        label = meta.get("partner_a" if owner == "A" else "partner_b", owner)
        w(f"**{label}**")
        w("")
        if nxt:
            for t in nxt:
                w(f"- ⬜ **{t['id']}** {t['title']} — {WHO[t['who']]} (week {t['week']})")
        else:
            w("- All planned tasks done.")
        w("")

    # hands-on work for humans
    w("## Hands-on work for you and your partner")
    w("")
    w("Claude does every task marked \"Claude\". These are the ones that need a person. "
      "Claude gives step-by-step instructions for each one when it comes up.")
    w("")
    human = [t for t in sorted(tasks, key=lambda t: (t["week"], order[t["id"]]))
             if t["who"] != "claude" and t["status"] != "done"]
    if human:
        w("| Week | Task | Who | What you do |")
        w("|---:|---|---|---|")
        for t in human:
            what = t.get("human") or {"you": "All of it, following Claude's steps",
                                      "partner": "Your partner does it from his own account",
                                      "claude+you": "Run the commands Claude gives, paste the output back"}[t["who"]]
            star = " ⭐" if t.get("bonus") else ""
            w(f"| {t['week']} | {ICON[t['status']]} **{t['id']}** {t['title']}{star} | {WHO[t['who']]} | {what} |")
    else:
        w("Nothing left that needs a person.")
    w("")

    # submission portal
    w("## Submission portal checklist")
    w("")
    w("The portal takes these items (brief §5.8), not files. Every file lives in the GitHub repo.")
    w("")
    sub = data.get("submission", [])
    ready = sum(line_state(x) == "done" for x in sub)
    w(f"**{ready} of {len(sub)} ready.**")
    w("")
    for x in sub:
        st = line_state(x)
        missing = [r for r in x["requires"] if not is_done(r)]
        tail = "" if not missing else f" — waiting on {', '.join(missing)}"
        w(f"- {ICON[st]} {x['title']}{tail}")
    w("")

    # built
    w("## Built")
    w("")
    done_all = sorted((t for t in tasks if t["status"] == "done"), key=lambda t: (t["done"], order[t["id"]]), reverse=True)
    if done_all:
        w("| Done on | Task | Owner |")
        w("|---|---|---|")
        for t in done_all:
            star = " ⭐ bonus" if t.get("bonus") else ""
            w(f"| {t['done']} | **{t['id']}** {t['title']}{star} | {t['owner']} |")
    else:
        w("Nothing finished yet.")
    w("")

    # rubric detail
    w("<details>")
    w("<summary><strong>Every rubric line and what it still needs</strong></summary>")
    w("")
    w("| Line | Marks | State | Still needed |")
    w("|---|---:|---|---|")
    for r in rubric:
        st = line_state(r)
        missing = [x for x in r["requires"] if not is_done(x)]
        w(f"| {r['id']} {r['title']} | {r['marks']} | {ICON[st]} | {', '.join(missing) if missing else '—'} |")
    for b in data.get("bonus", []):
        st = line_state(b)
        missing = [x for x in b["requires"] if not is_done(x)]
        w(f"| {b['id']} ⭐ {b['title']} | +{b['marks']} | {ICON[st]} | {', '.join(missing) if missing else '—'} |")
    w("")
    w("</details>")
    w("")

    # all tasks by phase
    w("<details>")
    w("<summary><strong>All tasks by phase</strong></summary>")
    w("")
    for prefix, name in PHASES:
        group = [t for t in tasks if phase_of(t["id"]) == prefix]
        if not group:
            continue
        d = sum(t["status"] == "done" for t in group)
        w(f"**{name}** — {d} of {len(group)} done")
        w("")
        for t in group:
            star = " ⭐" if t.get("bonus") else ""
            w(f"- {ICON[t['status']]} {t['id']} {t['title']} ({t['owner']}, {WHO[t['who']]}, week {t['week']}){star}")
        w("")
    w("</details>")
    w("")

    # log
    w("## Change log")
    w("")
    for entry in list(reversed(data.get("log", [])))[:15]:
        w(f"- {entry['date']}: {entry['text']}")
    w("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="fail if STATUS.md is out of date")
    args = ap.parse_args()
    try:
        data = load()
        validate(data)
    except ProgressError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    text = render(data)
    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != text:
            print("STATUS.md is stale. Run: python scripts/update_status.py", file=sys.stderr)
            return 1
        print("STATUS.md is up to date.")
        return 0
    OUT.write_text(text, encoding="utf-8")
    core = [t for t in data["tasks"] if not t.get("bonus")]
    done = sum(t["status"] == "done" for t in core)
    print(f"STATUS.md written: {done}/{len(core)} core tasks ({pct(done, len(core))}%).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
