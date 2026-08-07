import os

from dotenv import load_dotenv
from google import genai

# Load variables from .env
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client lazily, so the backend can start without a key.
client = genai.Client(api_key=api_key) if api_key else None


def _get_client():
    if not client:
        raise ValueError("GEMINI_API_KEY is not set in the .env file")
    return client


def analyze_contract(contract_text):

    prompt = f"""
You are ClauseIQ AI, an AI-powered contract analysis assistant.

Analyze the following contract.

Return your response in exactly this format:

SUMMARY:
Give a short summary of the contract.

RISKS:
List the important legal or business risks.
For each risk, explain why it is risky.

OBLIGATIONS:
List important obligations, deadlines, notice periods, payments,
or responsibilities mentioned in the contract.

RECOMMENDATIONS:
Give practical recommendations based only on the contract.

Do not invent information that is not present in the contract.

CONTRACT:
{contract_text}
"""

    response = _get_client().models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


def answer_question(contract_text, question):
    prompt = f"""
You are ClauseIQ AI, an intelligent contract assistant.
Answer the user's question using only the contract text below.
If the contract does not contain the answer, respond with:
"The contract does not provide that information."

CONTRACT:
{contract_text}

QUESTION:
{question}
"""

    response = _get_client().models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":

    sample_contract = """
    This Agreement is between ABC Company and XYZ Customer.

    The customer must pay all invoices within 30 days.

    Either party may terminate this agreement by providing
    60 days written notice.

    Confidential information must not be disclosed to third parties.
    """

    result = analyze_contract(sample_contract)

    print(result)

