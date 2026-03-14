import os
import re
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "gemini-2.5-flash"
MAX_RETRIES = 3


def analyze_code(code: str, filename: str) -> dict:
    """
    Sends the code to Google Gemini and returns a structured explanation
    including: summary, real-world analogy, step-by-step walkthrough,
    and Mermaid diagram code.
    """
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    prompt = f"""
You are an expert software engineer and teacher. Analyze the following code file named "{filename}" and provide a comprehensive explanation structured as follows:

---
**CODE:**
```
{code}
```
---

Return your response as a structured JSON object (no markdown wrapping, just raw JSON) with these exact keys:

{{
  "language": "<detected programming language>",
  "summary": "<2-3 sentence high-level summary of what this code does>",
  "real_world_analogy": "<a simple, creative real-world analogy that explains the overall concept>",
  "key_concepts": [
    {{
      "name": "<concept name>",
      "explanation": "<clear explanation>",
      "analogy": "<a mini real-world analogy for just this concept>"
    }}
  ],
  "step_by_step": [
    "<step 1 description>",
    "<step 2 description>",
    "..."
  ],
  "mermaid_diagram": "<valid Mermaid.js diagram code — use flowchart, sequenceDiagram, or classDiagram depending on what fits best>",
  "mermaid_diagram_type": "<flowchart | sequenceDiagram | classDiagram>",
  "potential_improvements": [
    "<improvement suggestion 1>",
    "<improvement suggestion 2>"
  ]
}}

Rules:
- The mermaid_diagram must be valid Mermaid.js syntax.
- Keep analogies simple, fun, and relatable to everyday life.
- step_by_step should trace the actual execution or data flow of the code.
- Do NOT wrap the JSON in markdown code fences. Return raw JSON only.
"""

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
            break
        except Exception as e:
            msg = str(e)
            # Extract retry delay from error message if present
            match = re.search(r"retry in (\d+)", msg, re.IGNORECASE)
            wait = int(match.group(1)) + 2 if match else 15
            if attempt < MAX_RETRIES and "429" in msg:
                print(f"\n⏳  Rate limited. Waiting {wait}s before retry {attempt}/{MAX_RETRIES}...")
                time.sleep(wait)
            else:
                raise

    raw = response.text.strip()

    # Strip accidental markdown fences if model adds them
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()
        if raw.endswith("```"):
            raw = raw[:-3].strip()

    import json
    return json.loads(raw)
