from pathlib import Path

from pdf_service import extract_text_from_pdf


pdf_path = Path("test_contract.pdf")

pdf_bytes = pdf_path.read_bytes()

text = extract_text_from_pdf(pdf_bytes)

print("\n===== EXTRACTED TEXT =====\n")
print(text)
print("\n===== END =====")