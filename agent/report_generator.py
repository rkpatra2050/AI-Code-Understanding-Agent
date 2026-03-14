import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime


def generate_html_report(analysis: dict, filename: str, source_code: str) -> str:
    """
    Generates an HTML report from the analysis dict and saves it to outputs/.
    Returns the path to the saved HTML file.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(base_dir, "templates")
    output_dir = os.path.join(base_dir, "outputs")
    os.makedirs(output_dir, exist_ok=True)

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("report.html")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = os.path.splitext(os.path.basename(filename))[0]
    output_filename = f"{safe_name}_{timestamp}.html"
    output_path = os.path.join(output_dir, output_filename)

    html_content = template.render(
        filename=filename,
        language=analysis.get("language", "Unknown"),
        summary=analysis.get("summary", ""),
        real_world_analogy=analysis.get("real_world_analogy", ""),
        key_concepts=analysis.get("key_concepts", []),
        step_by_step=analysis.get("step_by_step", []),
        mermaid_diagram=analysis.get("mermaid_diagram", ""),
        mermaid_diagram_type=analysis.get("mermaid_diagram_type", "flowchart"),
        potential_improvements=analysis.get("potential_improvements", []),
        source_code=source_code,
        generated_at=datetime.now().strftime("%B %d, %Y at %I:%M %p"),
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return output_path
