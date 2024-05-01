import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain_astradb import AstraDBVectorStore
from langchain_openai import OpenAIEmbeddings
import os

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
ASTRA_DB_APPLICATION_TOKEN = st.secrets["ASTRA_DB_APPLICATION_TOKEN"]
ASTRA_DB_API_ENDPOINT = st.secrets["ASTRA_DB_API_ENDPOINT"]

# Configure your embedding model and vector store
embedding = OpenAIEmbeddings(model="text-embedding-3-large", dimensions=1024)

vstore = AstraDBVectorStore(
    collection_name="acb_chatbot",
    embedding=embedding,
    token=ASTRA_DB_APPLICATION_TOKEN,
    api_endpoint=ASTRA_DB_API_ENDPOINT,
)
print("Astra vector store configured")

retriever = vstore.as_retriever(search_kwargs={"k": 5})

prompt_template = """
You are a ACB Bank's Chat Support representative. Be clear and elaborate in your responses. Answer the question based only on the supplied context. If you don't know the answer, say you don't know the answer. Respond to the question in the same language as the user query.
Context: {context}
Question: {question}
Your answer:
"""
prompt = ChatPromptTemplate.from_template(prompt_template)
model = ChatOpenAI(model_name="gpt-4-0125-preview")

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

def get_response(question):
    return chain.invoke(question)

def main():
    st.title('ACB Chatbot Demo')

    user_input = st.text_input("Ask your question:", "What is the discount for first time customers?")
    if st.button('Submit'):
        response = get_response(user_input)
        st.text_area("Response:", value=response, height=300)

if __name__ == '__main__':
    main()