# AI Code Understanding Agent - Copilot Instructions

## Project Overview
This is an AI-powered agent that analyzes code files and provides:
- Diagrammatic explanations (flowcharts, class diagrams, sequence diagrams)
- Real-world analogies for each code concept
- Step-by-step code walkthroughs
- Visual ASCII/Mermaid diagrams rendered in terminal and HTML

## Tech Stack
- Python 3.10+
- Google Gemini API (LLM backbone)
- Mermaid.js (diagram rendering in HTML)
- Rich (terminal UI)
- Jinja2 (HTML report templating)

## Project Structure
- `agent/` - Core agent logic
- `agent/analyzer.py` - Code analysis and LLM interaction
- `agent/diagram_generator.py` - Mermaid diagram generation
- `agent/report_generator.py` - HTML report generation
- `templates/` - HTML templates for reports
- `uploads/` - User-uploaded code files
- `outputs/` - Generated HTML reports
- `main.py` - CLI entrypoint
- `.env` - API keys (not committed)

## Development Rules
- Use Gemini API for all LLM calls
- Always generate Mermaid diagrams alongside explanations
- Keep real-world analogies simple and relatable
- Output both terminal (Rich) and HTML reports
