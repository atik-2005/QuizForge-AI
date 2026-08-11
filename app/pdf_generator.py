from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(mcqs, file_path):

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>Generated MCQs</b>", styles["Title"]))

    for i, mcq in enumerate(mcqs, 1):

        story.append(Paragraph(f"<b>Question {i}</b>", styles["Heading2"]))
        story.append(Paragraph(mcq["question"], styles["BodyText"]))

        for option in mcq["options"]:
            story.append(Paragraph(option, styles["BodyText"]))

        story.append(
            Paragraph(
                f"<b>Answer:</b> {mcq['answer']}",
                styles["BodyText"]
            )
        )

    doc.build(story)
