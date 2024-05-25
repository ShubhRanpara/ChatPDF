# Chat with PDF

This is a fun Python project that allows you to chat with a chatbot about the PDF you uploaded. and generate a PDF transcript of the conversation. The project is built using Python and Streamlit framework.

## Installation

To run this project, please follow the steps below:

1. Create and activate a virtual environment (optional but recommended):

```shell
python3 -m venv venv source venv/bin/activate
```

2. Install the dependencies from the `requirements.txt` file:

```shell
pip install -r requirements.txt
```

3. Add your HUGGINGFACEHUB_API_TOKEN in `.env` file and check the file name must be `.env` otherwise rename the file to `.env`. If you don't have a huggingface api token then generate one from settings. And also remember to get access of the required nlp model which you are using.

## Running the Project

4. Once you have installed the required dependencies, you can run the project using Streamlit. Streamlit provides an easy way to create interactive web applications in Python.

To start the application, run the following command:

```shell
python -m streamlit run app.py
```

This will start the Streamlit server and open the application in your default web browser.