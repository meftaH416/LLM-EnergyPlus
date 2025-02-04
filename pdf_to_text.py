import fitz  # PyMuPDF
print(fitz.__file__)

pdf_path = "InputOutputReference.pdf"
txt_path = "input_output_reference.txt"

try:
    # Open the PDF file
    doc = fitz.open(pdf_path)

    # Extract text from all pages
    text = "\n".join([page.get_text("text") for page in doc])

    # Close the PDF document
    doc.close()

    # Write the extracted text to a text file
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Text has been successfully written to {txt_path}")

except Exception as e:
    print(f"Error: {e}")
