# Install dependencies
# pip install streamlit PyPDF2 groq

import streamlit as st
from PyPDF2 import PdfReader
import os
from groq import Groq

# Set the API key
os.environ["GROQ_API_KEY"] = "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"

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Streamlit App
st.title("Pakistani Constitution Q&A App")
st.write("Upload the PDF of the Pakistani Constitution and ask questions about it.")

# Upload PDF
uploaded_file = st.file_uploader("Upload PDF", type="pdf")
if uploaded_file:
    # Extract text from the PDF
    pdf_reader = PdfReader(uploaded_file)
    constitution_text = ""
    for page in pdf_reader.pages:
        constitution_text += page.extract_text()

    st.success("PDF Uploaded and Processed Successfully!")

    # Predefined sections or chapters of the Constitution
    # Assuming the Constitution is structured, you can define sections like this:
    sections = {
        "Preamble": (0, 1000),  # You may need to adjust the range manually based on text positions
        "Fundamental Rights": (1000, 5000),
        "Directive Principles of State Policy": (5000, 8000),
        "Structure of Government": (8000, 12000),
        "Emergency Provisions": (12000, 15000),
        "Amendment Procedure": (15000, 18000)
    }

    # Allow user to select a specific section
    section_choice = st.selectbox("Select a section of the Constitution:", list(sections.keys()))
    section_start, section_end = sections[section_choice]

    # Extract selected section text
    selected_section_text = constitution_text[section_start:section_end]
    
    # Show the extracted section text to the user
    st.write(f"### Selected Section: {section_choice}")
    st.text_area("Text from selected section", selected_section_text, height=200)

    # Ask a question about the selected section
    user_question = st.text_input(f"Ask a question about the '{section_choice}' section:")

    if user_question:
        st.write("Processing your question...")
        
        # Send the selected section text and question to Groq API
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "user", "content": f"Context: {selected_section_text}\nQuestion: {user_question}"}
                ],
                model="llama3-8b-8192",
            )
            # Display the answer
            answer = chat_completion.choices[0].message.content
            st.write("### Answer:")
            st.write(answer)
        except Exception as e:
            st.error(f"An error occurred: {e}")
