import fitz  # PyMuPDF

pdf_path = "InputOutputReference.pdf"
txt_path = "input_output_reference.txt"

with fitz.open(pdf_path) as doc:
    text = "\n".join([page.get_text("text") for page in doc])

with open(txt_path, "w", encoding="utf-8") as f:
    f.write(text)
