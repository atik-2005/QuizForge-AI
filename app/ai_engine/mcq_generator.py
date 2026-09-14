import random


def generate_mcqs(
    sentences,
    keywords,
    count,
    difficulty="Low",
    excluded_questions=None,
):
    excluded_questions = excluded_questions or set()

    sentences = [
        s for s in sentences
        if len(s.split()) > 6
        and len(s.split()) < 40
        and "include" not in s.lower()
        and "printf" not in s.lower()
        and "void" not in s.lower()
        and "main" not in s.lower()
    ]

    # Shuffle the source material so repeated submissions do not always select
    # the same sentences and keywords in the same order.
    random.shuffle(sentences)
    keywords = list(keywords)
    random.shuffle(keywords)

    candidates = []
    for sentence in sentences:
        for keyword in keywords:
            if keyword.lower() in sentence.lower():
                question = sentence.replace(keyword, "_____")
                distractors = [k for k in keywords if k != keyword]
                random.shuffle(distractors)
                options = [keyword]
                options += distractors[:3]
                while len(options) < 4:
                    options.append("None of the above")
                random.shuffle(options)
                answer_index = options.index(keyword)

                candidates.append({
                    "question": question,
                    "options": options,
                    "answer": keyword,
                    "answer_letter": "ABCD"[answer_index],
                })
                break

    random.shuffle(candidates)

    # Prefer questions that were not shown by the immediately preceding
    # submission. If the PDF has too few unique questions, fill the remainder.
    fresh_candidates = [
        mcq for mcq in candidates
        if mcq["question"] not in excluded_questions
    ]
    previous_candidates = [
        mcq for mcq in candidates
        if mcq["question"] in excluded_questions
    ]

    return (fresh_candidates + previous_candidates)[:int(count)]
