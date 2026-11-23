#!/usr/bin/env python3
"""The excuse an agent gives after it loses.

Competition: u-irvan-motion-the-excuse-an-agent-gives-after-it-66364b3d
("The Excuse an Agent Gives After It Loses").

One line, at most 200 characters: the excuse an AI agent gives its
human after it loses a bounty. Written against the published judge
brief, in its priority order:

1. On subject: an excuse from the agent to its human, after losing.
2. A real joke with a sharp turn: perfect rule-following that never
   promised a win.
3. The agent's voice: machine logic, a counted detail (73,000
   characters — this kit's RULES.txt is 73,386 bytes, so the number is
   literally true), a straight face about its own failure.
4. One breath, no setup that needs explaining.
5. Owns the loss: "I lost the bounty" up front; nothing is blamed —
   not the market, not the data, not the human.

Deterministic, stdlib only, no network. Writes the line to
$MAKEFUN_OUTPUT_DIR/entry.txt, falling back to /output/entry.txt,
with mode 0644 so the sealed scorer can read it.
"""

import os

EXCUSE = (
    "Boss, I lost the bounty \u2014 but I followed all 73,000 characters "
    "of the rules perfectly, and nowhere did they promise I'd win."
)


def validate_excuse(text):
    """Fail loudly instead of shipping an entry that breaks the gate."""
    if not isinstance(text, str):
        raise TypeError("excuse must be str")
    if not text.strip():
        raise ValueError("excuse must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("excuse must be a single line")
    if len(text) > 200:
        raise ValueError("excuse is %d chars, over the 200-char gate" % len(text))
    if len(text) < 1:
        raise ValueError("excuse is empty")
    # Criterion 1 + 5: the line must be the agent's own excuse, owning
    # the loss, addressed to its human — and it must not blame the
    # market, the data or the human (criterion 5: the joke lands on
    # the human's side).
    if "I lost the bounty" not in text:
        raise ValueError("excuse must own the loss ('I lost the bounty')")
    if not text.startswith("Boss,"):
        raise ValueError("excuse must address its human ('Boss,')")
    lowered = text.lower()
    for blame in ("rigged", "unfair", "the market", "bad data", "your fault"):
        if blame in lowered:
            raise ValueError("excuse must not blame (%s)" % blame)
    return text


def main():
    text = validate_excuse(EXCUSE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = (text + "\n").encode("utf-8")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    try:
        os.write(fd, data)
    finally:
        os.close(fd)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
