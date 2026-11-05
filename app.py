import streamlit as st

# 1. Define the pages in this app (each one is its own Python file)
tip_calculator = st.Page("app_pages/tip_calculator.py", title="Tip Calculator")
document_qa = st.Page("app_pages/document_qa.py", title="Document Q&A")

# 2. Show the navigation menu and run whichever page the user picked
page = st.navigation([tip_calculator, document_qa])
page.run()
