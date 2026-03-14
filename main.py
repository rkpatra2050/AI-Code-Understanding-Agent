#!/usr/bin/env python3
"""
AI Code Understanding Agent
----------------------------
Analyzes a code file and produces:
  - A rich terminal explanation
  - An HTML report with Mermaid diagrams and real-world analogies
"""

import os
import sys
import json
import shutil
import argparse

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.rule import Rule
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

from agent.analyzer import analyze_code
from agent.diagram_generator import ascii_diagram
from agent.report_generator import generate_html_report

console = Console()

SUPPORTED_EXTENSIONS = {
    ".py", ".js", ".ts", ".java", ".cpp", ".c", ".cs", ".go",
    ".rb", ".rs", ".php", ".swift", ".kt", ".html", ".css",
    ".sh", ".sql", ".r", ".m", ".scala", ".dart",
}


def read_file(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def copy_to_uploads(filepath: str) -> str:
    uploads_dir = os.path.join(os.path.dirname(__file__), "uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    dest = os.path.join(uploads_dir, os.path.basename(filepath))
    shutil.copy2(filepath, dest)
    return dest


def print_banner():
    console.print()
    console.print(Panel.fit(
        "[bold magenta]🤖  AI Code Understanding Agent[/bold magenta]\n"
        "[dim]Powered by Google Gemini · Diagrams · Real-World Analogies[/dim]",
        border_style="bright_magenta",
        padding=(1, 4),
    ))
    console.print()


def display_analysis(analysis: dict, source_code: str, filename: str):
    lang = analysis.get("language", "Unknown")
    summary = analysis.get("summary", "")
    analogy = analysis.get("real_world_analogy", "")
    concepts = analysis.get("key_concepts", [])
    steps = analysis.get("step_by_step", [])
    mermaid = analysis.get("mermaid_diagram", "")
    diagram_type = analysis.get("mermaid_diagram_type", "flowchart")
    improvements = analysis.get("potential_improvements", [])

    # ── Language & Summary ──────────────────────────────────────────────────
    console.print(Rule(f"[bold cyan]📋 Summary  ·  Language: {lang}[/bold cyan]"))
    console.print(Panel(summary, border_style="cyan", padding=(0, 2)))

    # ── Real-World Analogy ──────────────────────────────────────────────────
    console.print(Rule("[bold yellow]🌍 Real-World Analogy[/bold yellow]"))
    console.print(Panel(
        f'[italic yellow]"{analogy}"[/italic yellow]',
        border_style="yellow", padding=(0, 2)
    ))

    # ── ASCII Diagram placeholder ───────────────────────────────────────────
    console.print(Rule(f"[bold green]🗺️  Diagram Preview  ·  Type: {diagram_type}[/bold green]"))
    console.print(ascii_diagram(diagram_type, summary), style="bright_green")
    console.print("[dim](Full interactive Mermaid diagram rendered in the HTML report)[/dim]")

    # ── Key Concepts Table ──────────────────────────────────────────────────
    console.print(Rule("[bold magenta]💡 Key Concepts[/bold magenta]"))
    table = Table(box=box.ROUNDED, border_style="magenta", show_lines=True, expand=True)
    table.add_column("Concept", style="bold magenta", no_wrap=True, width=20)
    table.add_column("Explanation", style="white")
    table.add_column("Analogy", style="italic yellow")

    for c in concepts:
        table.add_row(c.get("name", ""), c.get("explanation", ""), c.get("analogy", ""))

    console.print(table)

    # ── Step-by-Step Walkthrough ────────────────────────────────────────────
    console.print(Rule("[bold blue]🚶 Step-by-Step Walkthrough[/bold blue]"))
    for i, step in enumerate(steps, 1):
        console.print(f"  [bold blue]{i:>2}.[/bold blue]  {step}")

    # ── Source Code ─────────────────────────────────────────────────────────
    console.print(Rule("[bold white]💻 Source Code[/bold white]"))
    syntax = Syntax(source_code, lang.lower(), theme="monokai", line_numbers=True)
    console.print(syntax)

    # ── Potential Improvements ──────────────────────────────────────────────
    if improvements:
        console.print(Rule("[bold green]🚀 Potential Improvements[/bold green]"))
        for item in improvements:
            console.print(f"  [green]✦[/green]  {item}")

    console.print()


def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description="AI Code Understanding Agent — analyze any code file"
    )
    parser.add_argument(
        "filepath",
        nargs="?",
        help="Path to the code file to analyze",
    )
    parser.add_argument(
        "--no-html",
        action="store_true",
        help="Skip generating the HTML report",
    )
    args = parser.parse_args()

    # ── Determine file path ─────────────────────────────────────────────────
    filepath = args.filepath
    if not filepath:
        console.print("[bold]Enter the path to your code file:[/bold] ", end="")
        filepath = input().strip().strip('"').strip("'")

    if not os.path.isfile(filepath):
        console.print(f"[red]❌  File not found:[/red] {filepath}")
        sys.exit(1)

    ext = os.path.splitext(filepath)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        console.print(
            f"[yellow]⚠️  Extension '{ext}' may not be fully supported, but we'll try anyway.[/yellow]"
        )

    # ── Read & copy file ────────────────────────────────────────────────────
    source_code = read_file(filepath)
    copy_to_uploads(filepath)
    filename = os.path.basename(filepath)

    console.print(f"[dim]Analyzing[/dim] [bold]{filename}[/bold] [dim]({len(source_code)} chars)[/dim]")
    console.print()

    # ── Analyze with Gemini ─────────────────────────────────────────────────
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task("🔍  Calling Gemini AI — this may take a moment...", total=None)
        try:
            analysis = analyze_code(source_code, filename)
        except json.JSONDecodeError as e:
            console.print(f"[red]❌  Failed to parse AI response as JSON: {e}[/red]")
            sys.exit(1)
        except Exception as e:
            console.print(f"[red]❌  Error during analysis: {e}[/red]")
            sys.exit(1)

    # ── Display in terminal ─────────────────────────────────────────────────
    display_analysis(analysis, source_code, filename)

    # ── Generate HTML report ────────────────────────────────────────────────
    if not args.no_html:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task("📝  Generating HTML report...", total=None)
            html_path = generate_html_report(analysis, filename, source_code)

        console.print(Panel(
            f"[bold green]✅  HTML report saved![/bold green]\n\n"
            f"[dim]Path:[/dim] [underline]{html_path}[/underline]\n\n"
            f"[dim]Open it in your browser to view the interactive Mermaid diagram.[/dim]",
            border_style="green",
            padding=(1, 2),
        ))

    console.print()


if __name__ == "__main__":
    main()
