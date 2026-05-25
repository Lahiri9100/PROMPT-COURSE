from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter


def create_pdf(content):

    pdf_file = "roadmap.pdf"

    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    story = []

    # Clean markdown symbols

    clean_content = content.replace("#", "")
    clean_content = clean_content.replace("*", "")
    clean_content = clean_content.replace("`", "")

    lines = clean_content.split("\n")

    for line in lines:

        if line.strip() != "":

            para = Paragraph(
                str(line),
                styles["BodyText"]
            )

            story.append(para)

            story.append(
                Spacer(1, 10)
            )

    doc.build(story)

    return pdf_file