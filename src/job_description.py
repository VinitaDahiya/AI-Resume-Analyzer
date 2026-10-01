


from docx import Document


def read_job_description(file_path):
    document = Document(file_path)

    text = []

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text.append(paragraph.text.strip())

    return "\n".join(text)


if __name__ == "__main__":
    jd_path = "data/sample_job_description.docx"

    job_description = read_job_description(jd_path)

    print(job_description)