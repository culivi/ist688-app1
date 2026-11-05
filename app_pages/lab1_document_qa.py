import streamlit as st
from openai import OpenAI

# 1. Add a title to the web page
st.title("Lab 1 - Document Q&A")
st.write("Upload a .txt document and ask a question about it.")

# 2. Get the user's OpenAI API key
#    type="password" hides the key on screen. We only keep it in this
#    variable while the page runs — it is never saved or printed.
api_key = st.text_input("OpenAI API key", type="password")

if not api_key:
    st.info("Enter your OpenAI API key to continue.")
    st.stop()

# 3. Let the user upload a .txt document
uploaded_file = st.file_uploader("Upload a document (.txt)", type="txt")

# 4. Let the user ask a question (disabled until a file is uploaded)
question = st.text_input(
    "Ask a question about the document",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

# 5. When we have both a document and a question, ask OpenAI
if uploaded_file and question:
    # Turn the uploaded file's bytes into text
    document = uploaded_file.read().decode("utf-8")

    client = OpenAI(api_key=api_key)

    messages = [
        {
            "role": "user",
            "content": f"Here's a document:\n\n{document}\n\n---\n\n{question}",
        }
    ]

    # 6. Send the document and question to OpenAI and show the answer
    try:
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-5-mini",
                messages=messages,
            )
    except Exception as error:
        # Show a short message instead of a long error (e.g. a wrong API key)
        st.error(f"Something went wrong talking to OpenAI: {error}")
        st.stop()

    st.subheader("Answer")
    st.write(response.choices[0].message.content)
