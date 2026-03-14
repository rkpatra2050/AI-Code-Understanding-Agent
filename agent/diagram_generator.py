def generate_mermaid_block(mermaid_code: str) -> str:
    """
    Wraps raw Mermaid diagram code in a proper Mermaid code block
    for use in HTML templates.
    """
    return mermaid_code.strip()


def ascii_diagram(diagram_type: str, summary: str) -> str:
    """
    Generates a simple ASCII art placeholder diagram for terminal display
    when a visual diagram is not renderable in terminal.
    """
    lines = [
        "┌─────────────────────────────────────────┐",
        f"│  Diagram Type : {diagram_type:<24} │",
        "├─────────────────────────────────────────┤",
    ]
    # Wrap summary into ~40 chars per line
    words = summary.split()
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= 40:
            current_line = (current_line + " " + word).strip()
        else:
            lines.append(f"│  {current_line:<39}│")
            current_line = word
    if current_line:
        lines.append(f"│  {current_line:<39}│")
    lines.append("└─────────────────────────────────────────┘")
    return "\n".join(lines)
