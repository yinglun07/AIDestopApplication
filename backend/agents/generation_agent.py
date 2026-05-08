from reportlab.pdfgen import canvas
from textwrap import wrap
import json

class GenerationAgent:
    
    def create_pdf(self, text):
        file_path = "output.pdf"
        c = canvas.Canvas(file_path)

        y = 800

        for line in text.split("\n"):
            wrapped_lines = wrap(line, width=90)

            for wl in wrapped_lines:
                if y < 50:
                    c.showPage()
                    y = 800

                c.drawString(50, y, wl)
                y -= 15

        c.save()
        return file_path
    
    def summarize_history(self):
        try:
            with open("history.json", "r") as f:
                history = json.load(f)
        except:
            return ""

        lines = []

        for item in history:
            if not isinstance(item, dict):
                continue

            q = item.get("query", "")
            r = item.get("result", "")

            if isinstance(r, dict):
                r = json.dumps(r, indent=2)

            lines.append(f"User asked: {q}")
            lines.append(f"System answered: {r}")
            lines.append("")

        return "\n".join(lines)
    
    def create_report(self, query=None):
        summary = self.summarize_history()

        file_path = self.create_pdf(summary)

        return {
            "message": "PDF generated successfully",
            "summary": summary,
            "file": file_path
    }
    

