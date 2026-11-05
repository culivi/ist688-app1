import streamlit as st

# 1. Define the pages in this app (each one is its own Python file)
tip_calculator = st.Page("app_pages/tip_calculator.py", title="Tip Calculator")
lab1 = st.Page("app_pages/lab1_document_qa.py", title="Lab 1 - Document Q&A")
lab2 = st.Page(
    "app_pages/lab2_pdf_summarizer.py",
    title="Lab 2 - PDF Summarizer",
    default=True,  # the page that opens first
)

# 2. Show the navigation menu and run whichever page the user picked
page = st.navigation([tip_calculator, lab1, lab2])
page.run()
