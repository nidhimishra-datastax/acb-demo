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

    # Create containers for messages
    container = st.container()
    all_messages = []

    # Manage user input through session state for better control
    if 'input' not in st.session_state:
        st.session_state['input'] = ""

    user_input = st.text_input("Type your question here:", key="input")

    # Function to handle the response display
    def display_message(user_query, bot_response):
        col1, col2 = st.columns([1, 5])
        with col1:
            st.image("https://via.placeholder.com/50", width=50)  # Placeholder for user image
        with col2:
            st.text_area("", value=user_query, height=75, disabled=True, key=f"user_{len(all_messages)}")
        
        col1, col2 = st.columns([1, 5])
        with col1:
            st.image("https://via.placeholder.com/50", width=50)  # Placeholder for bot image
        with col2:
            st.text_area("", value=bot_response, height=100, disabled=True, key=f"bot_{len(all_messages)}")

    if st.button('Send'):
        if user_input:
            bot_response = get_response(user_input)
            all_messages.append((user_input, bot_response))
            with container:
                for user_query, bot_reply in all_messages:
                    display_message(user_query, bot_reply)
            # Clear input field after sending
            # st.session_state.input = ""  # Reset input field safely

    # Check if we need to reset the input field
    # if 'reset_input' in st.session_state and st.session_state.reset_input:
    #     st.session_state.input = ""  # Reset input field safely
    #     st.session_state.reset_input = False  # Clear the reset flag        

if __name__ == '__main__':
    main()