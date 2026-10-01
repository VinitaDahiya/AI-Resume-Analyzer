import pymupdf     


def extract_text_from_pdf(pdf_path):
    document = pymupdf.open(pdf_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


if __name__ == "__main__":
    pdf_path = "./data/sample_resume.pdf"

    resume_text = extract_text_from_pdf(pdf_path)

    print(resume_text)