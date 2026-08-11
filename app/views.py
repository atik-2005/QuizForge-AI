from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import fitz

from app.ai_engine.preprocess import (
    clean_text,
    sentence_split,
    word_split,
    remove_stopwords,
    lemmatize,
)

from app.ai_engine.keyword_extractor import extract_keywords
from app.ai_engine.mcq_generator import generate_mcqs


def home(request):

    mcqs = []

    if request.method == "POST":

        pdf = request.FILES.get("pdf_file")
        difficulty = request.POST.get("difficulty")
        mcq_count = request.POST.get("mcq_count")

        if pdf:

            fs = FileSystemStorage()
            filename = fs.save(pdf.name, pdf)
            file_path = fs.path(filename)

            pdf_document = fitz.open(file_path)

            extracted_text = ""

            for page in pdf_document:
                extracted_text += page.get_text()

            pdf_document.close()

            cleaned_text = clean_text(extracted_text)

            sentences = sentence_split(cleaned_text)

            words = word_split(cleaned_text)

            filtered_words = remove_stopwords(words)

            lemmatized_words = lemmatize(filtered_words)

            keywords = extract_keywords(cleaned_text)

            mcqs = generate_mcqs(
                sentences,
                keywords,
                int(mcq_count),
                difficulty
            )

            # Save generated MCQs in session
            request.session["mcqs"] = mcqs

    return render(request, "home.html", {
        "mcqs": mcqs
    })


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

    pdf.save()

    return response
