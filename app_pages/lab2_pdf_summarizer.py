import streamlit as st
from openai import OpenAI

# 1. Add a title to the web page
st.title("Lab 2 - PDF Summarizer")
st.write("Upload a .txt document and choose how you'd like it summarized.")

# 2. Get the OpenAI API key from Streamlit secrets
#    Locally, Streamlit reads it from .streamlit/secrets.toml (kept out of Git).
#    On Streamlit Community Cloud, it comes from the app's Secrets settings.
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    st.error("No OpenAI API key found. Add OPENAI_API_KEY to the app's secrets.")
    st.stop()

# 3. Let the user upload a .txt document
uploaded_file = st.file_uploader("Upload a document (.txt)", type="txt")

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

# 5. Let the user pick a model.
#    Each option (left) maps to the OpenAI model name (right).
model_options = {
    "Mini (faster, cheaper)": "gpt-5.4-mini",
    "Flagship (more capable)": "gpt-5.5",
}
model_choice = st.radio("Model", list(model_options.keys()))

# 6. Only call OpenAI when the user clicks the button
if st.button("Summarize", disabled=not uploaded_file):
    # Turn the uploaded file's bytes into text
    document = uploaded_file.read().decode("utf-8")
    instruction = summary_options[summary_choice]
    model = model_options[model_choice]

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
