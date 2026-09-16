from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import fitz
import logging

from app.ai_engine.preprocess import (
    clean_text,
    sentence_split,
    word_split,
    remove_stopwords,
    lemmatize,
)


def home(request):
    mcqs = []
    error = None

    if request.method == "POST":
        previous_mcqs = request.session.get("mcqs", [])
        previous_questions = {
            mcq.get("question")
            for mcq in previous_mcqs
            if isinstance(mcq, dict) and mcq.get("question")
        }

        request.session["mcqs"] = []   # clear old MCQs before new generation
        request.session.modified = True

        try:
            from app.ai_engine.keyword_extractor import extract_keywords
            from app.ai_engine.mcq_generator import generate_mcqs

            pdf = request.FILES.get("pdf_file")
            difficulty = request.POST.get("difficulty", "Medium")
            mcq_count = request.POST.get("mcq_count", "10")

            if not pdf:
                error = "Please upload a PDF file."
            elif not pdf.name.lower().endswith(".pdf"):
                error = "Only PDF files are allowed."
            else:
                fs = FileSystemStorage()
                filename = fs.save(pdf.name, pdf)
                file_path = fs.path(filename)

                with fitz.open(file_path) as pdf_document:
                    extracted_text = "".join(page.get_text() for page in pdf_document)

                cleaned_text = clean_text(extracted_text)
                sentences = sentence_split(cleaned_text)
                words = word_split(cleaned_text)
                filtered_words = remove_stopwords(words)
                lemmatize(filtered_words)

                requested_count = int(mcq_count)
                keywords = extract_keywords(
                    cleaned_text,
                    top_n=max(10, requested_count * 2),
                )
                generated = generate_mcqs(
                    sentences,
                    keywords,
                    requested_count,
                    difficulty,
                    excluded_questions=previous_questions,
                )

                mcqs = generated or []
                if not mcqs:
                    error = "No selectable text was found in this PDF. Please upload a text-based PDF."
                elif len(mcqs) < requested_count:
                    error = (
                        f"This PDF only contains enough text for {len(mcqs)} unique MCQs "
                        f"out of the {requested_count} requested."
                    )
                request.session["mcqs"] = mcqs
                request.session.modified = True

        except Exception:
            logging.exception("MCQ generation failed")
            error = "Something went wrong while generating MCQs."
            mcqs = []
            request.session["mcqs"] = []
            request.session.modified = True

    return render(request, "home.html", {"mcqs": mcqs, "error": error})
def download(request):
    mcqs = request.session.get("mcqs")

    if not mcqs:
        return HttpResponse("No MCQs Generated Yet!")

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Generated_MCQs.pdf"'

    pdf = canvas.Canvas(response)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(170, 800, "AI Generated MCQs")

    y = 760
    pdf.setFont("Helvetica", 12)

    for i, mcq in enumerate(mcqs, start=1):
        if y < 120:
            pdf.showPage()
            pdf.setFont("Helvetica", 12)
            y = 800

        options = mcq.get("options", [])
        while len(options) < 4:
            options.append("")

        pdf.drawString(40, y, f"{i}. {mcq['question']}")
        y -= 20

        pdf.drawString(60, y, f"A. {options[0]}")
        y -= 20
        pdf.drawString(60, y, f"B. {options[1]}")
        y -= 20
        pdf.drawString(60, y, f"C. {options[2]}")
        y -= 20
        pdf.drawString(60, y, f"D. {options[3]}")
        y -= 40

        answer_letter = mcq.get("answer_letter", "")
        answer = mcq.get("answer", "")
        pdf.drawString(60, y, f"Answer: {answer_letter}. {answer}")
        y -= 40

    pdf.save()
    return response
