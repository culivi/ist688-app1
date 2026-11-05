import streamlit as st
from openai import OpenAI
from pypdf import PdfReader

# 1. Add a title to the web page
st.title("Lab 2 - PDF Summarizer")
st.write("Upload a PDF or .txt document and choose how you'd like it summarized.")

# 2. Get the OpenAI API key from Streamlit secrets
#    Locally, Streamlit reads it from .streamlit/secrets.toml (kept out of Git).
#    On Streamlit Community Cloud, it comes from the app's Secrets settings.
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    st.error("No OpenAI API key found. Add OPENAI_API_KEY to the app's secrets.")
    st.stop()

# 3. Let the user upload a PDF or .txt document
uploaded_file = st.file_uploader("Upload a document (.pdf or .txt)", type=["pdf", "txt"])

# 4. Let the user pick a summary style.
#    Each option (left) maps to the instruction we send to OpenAI (right).
summary_options = {
    "Summarize in 100 words": "Summarize this document in about 100 words.",
    "Summarize in 2 connecting paragraphs": (
        "Summarize this document in 2 paragraphs. "
        "The second paragraph should follow on from the first."
    ),
    "Summarize in 5 bullet points": "Summarize this document in exactly 5 bullet points.",
}
summary_choice = st.radio("Summary style", list(summary_options.keys()))

# 5. Let the user pick a model (mini first, then flagship)
model = st.radio("Model", ["gpt-5.4-mini", "gpt-6.1-sol"])

# 6. Only call OpenAI when the user clicks the button
if st.button("Summarize", disabled=not uploaded_file):
    # Turn the uploaded file into text
    if uploaded_file.name.lower().endswith(".pdf"):
        # Read the text from every page of the PDF and join it together
        reader = PdfReader(uploaded_file)
        document = "\n".join(page.extract_text() for page in reader.pages)
    else:
        document = uploaded_file.read().decode("utf-8")

    # A scanned PDF (just pictures of pages) has no text we can read
    if not document.strip():
        st.error("Couldn't find any text in this document.")
        st.stop()

    instruction = summary_options[summary_choice]

    client = OpenAI(api_key=api_key)

    messages = [
        {
            "role": "user",
            "content": f"Here's a document:\n\n{document}\n\n---\n\n{instruction}",
        }
    ]

    # 7. Send the document and instruction to OpenAI and show the summary
    try:
        with st.spinner("Summarizing..."):
            response = client.chat.completions.create(
                model=model,
                messages=messages,
            )
    except Exception as error:
        # Show a short message instead of a long error (e.g. a wrong API key)
        st.error(f"Something went wrong talking to OpenAI: {error}")
        st.stop()

    st.subheader("Summary")
    st.caption(f"Model: {model}")
    st.write(response.choices[0].message.content)
