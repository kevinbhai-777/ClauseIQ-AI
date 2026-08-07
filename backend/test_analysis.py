from pathlib import Path

from pdf_service import extract_text_from_pdf
from gemini_service import analyze_contract


# Find the test PDF
pdf_path = Path("test_contract.pdf")

# Read the PDF
pdf_bytes = pdf_path.read_bytes()

# Extract text from PDF
contract_text = extract_text_from_pdf(pdf_bytes)

print("\n===== PDF TEXT EXTRACTED =====\n")
print(f"Characters extracted: {len(contract_text)}")

# Send extracted text to Gemini
print("\n===== SENDING CONTRACT TO GEMINI =====\n")

result = analyze_contract(contract_text)

# Display Gemini response
print("\n===== GEMINI ANALYSIS =====\n")
print(result)

print("\n===== END =====")