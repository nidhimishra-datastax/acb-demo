# Welcome to ACB Q&A Assistant
This is the Q&A chatbot App that augments the capabilities of LLM with external sources(ACB website in this case) to facilitate Natural Language interactions.

## Features
- **Data Ingestion**
- **Query and Response**

## Components

This project demonstrates the use of the DataStax [ragstack-ai] to create a RAG application(Retrieval-Augmented Generation) with Langchain and AstraDB to efficiently handle and query large datasets using vector databases. 

* ingest_data.ipynb - Jupyter notebook for indexing data into Astra Vector database by crawling the ACB bank's website usify APify Webiste Crawler Bot.
* hello.py - Streamlit application for retrieval based on user queries.
* sample-questions.md - Sample questions for Q&A application
* ACB Dataset for debugging purposes

Streamlit is an open-source Python library that allows developers to create interactive, data-driven web applications with ease.

## Prerequisites
Before you can run this project, you need the following installed:
- Python and pip
- OpenAI API Key
- Access to DataStax AstraDB
- Apify Key (For data ingestion)

## Running the Q&A Assistant

1. First, clone the repository:

```bash
git clone <repository-url>
cd ACB-Demo
```

2. Install the dependencies as in requirements.txt

``` 
pip install requirements.txt
```

3. Populate OpenAI key, Astra DB endpoint, Astra token etc in the environment variables.

4. Run the Streamlit application.

``` 
streamlit run hello.py
 ```

Streamlit is an open-source Python library that allows developers to create interactive, data-driven web applications with ease.
ingest_data.ipynb - Run the python notebook to index and populate vector embeddings in AstraDB.

Alternatively, you can host it on Streamlit Cloud. This is available [[here](https://acb-demo.streamlit.app/)](https://acb-demo.streamlit.app/)
