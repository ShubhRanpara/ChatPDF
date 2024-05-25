import os
from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS #facebook AI similarity search
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub

# Sidebar contents
with st.sidebar:
    st.title('🤗💬 LLM Chat App powered by Gemma')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [Hugging Face Transformers](https://huggingface.co/google/gemma-2b-it) for question answering

    Made by Developers of team J.A.R.V.I.S.,
    - Shubh Ranpara,
    - J.J.,
    - R.K.Sid,
    - Backlash,
    - B.M..
    ''')

from pptxtopdf import convert
import comtypes.client
import docx

def convert_pptx_to_pdf(base_path, file, file_name):

    input_dir = os.path.join(base_path, file_name)
    output_dir = os.path.join(base_path)

    print(base_path, file_name)

    convert(input_dir, output_dir)

    output_file_name = base_path + "\\" + file_name[:-4] + "pdf"

    file = open(output_file_name, 'rb')
    return file


def convert_docx_to_pdf(base_path, file, file_name):

        word_path = base_path + "\\" + file_name
        pdf_path = base_path + "\\" + file_name[:-4] + "pdf"

        # Load the Word document
        doc = docx.Document(word_path)

        # Create a Word application object
        word = comtypes.client.CreateObject("Word.Application")

        # Get absolute paths for Word document and PDF file
        docx_path = os.path.abspath(word_path)
        pdf_path = os.path.abspath(pdf_path)

        # PDF format code
        pdf_format = 17

        # Make Word application invisible
        word.Visible = False

        try:
            # Open the Word document
            in_file = word.Documents.Open(docx_path)

            # Save the document as PDF
            in_file.SaveAs(pdf_path, FileFormat=pdf_format)

            print("Conversion successful. PDF saved at:", pdf_path)

        except Exception as e:
            print("Error:", e)

        finally:
            # Close the Word document and quit Word application
            if 'in_file' in locals():
                in_file.Close()
            word.Quit()

def main():
    load_dotenv()
    st.header("Ask Your PDF, DOCX, PPTX")
    
    file = st.file_uploader("Upload your file")

    file_name = ""

    if file:
        print(file.name)
        file_name = str(file.name)

    pdf = file

    base_path = "Path to your project directory where pdf, docx or pptx file is present."
    
    if (file_name.__contains__(".pptx")):
        pdf = convert_pptx_to_pdf(base_path, file, file_name)

    elif (file_name.__contains__(".docx")):
        convert_docx_to_pdf(base_path, file, file_name)
        output_file_name = base_path + "\\" + file_name[:-4] + "pdf"
        pdf = open(output_file_name, 'rb')

    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # spilit ito chuncks
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=512,
            chunk_overlap=20,
            length_function=len
        )
        chunks = text_splitter.split_text(text)

        # create embedding
        embeddings = HuggingFaceEmbeddings()

        knowledge_base = FAISS.from_texts(chunks, embeddings)

        user_question = st.text_input("Ask Question about your PDF:")

        if user_question:
            docs = knowledge_base.similarity_search(user_question)
            llm = HuggingFaceHub(repo_id="google/gemma-2b-it", model_kwargs={"temperature":0.1, "max_length":64}) # best for question answering.
            # llm = HuggingFaceHub(repo_id="google/flan-t5-large", model_kwargs={"temperature":5, "max_length":64}) # best for now
            # llm = HuggingFaceHub(repo_id="google/flan-t5-large", model_kwargs={"temperature":6, "max_length":1024}) # changed temperature and max_length

            chain = load_qa_chain(llm, chain_type="stuff")
            response = chain.run(input_documents=docs,question=user_question)
            st.write(response)

if __name__ == '__main__':
    main()