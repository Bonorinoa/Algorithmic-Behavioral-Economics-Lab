import streamlit as st
import pandas as pd
from utils import chat_with_author, summarize_book
import time
from io import StringIO

if "summarized" not in st.session_state:
    st.session_state["summarized"] = []

if "summaries" not in st.session_state:
    st.session_state["summaries"] = []
    
st.title("EconGPT")

st.sidebar.title("Inputs")

st.sidebar.subheader("OpenAI API Key")
api_key = st.sidebar.text_input(" ", "Insert API Key")
model = st.sidebar.selectbox(" ", ["davinci", "gpt-4"])
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.5, step=0.05)
max_tokens = st.sidebar.slider("Max tokens", 0, 800, 350, step=50)


# getting the correct files for given author and work should be done automatically. Look into file processing and regex to match with file names.

# get author
st.sidebar.subheader("Author")
author = st.sidebar.selectbox(" ", ["Adam Smith"])

if author == "Adam Smith":
    with open ("AdamSmith_MoralSentiments\\AdamSmith_Bio.txt", encoding='utf8') as f:
        adam_bio = f.read()


# get written work
st.sidebar.subheader("Written work")
work = st.sidebar.selectbox(" ", ["The Theory of Moral Sentiments"])

if work == "The Theory of Moral Sentiments":    
    with open("AdamSmith_MoralSentiments\\TheoryMoralSentiments.txt", encoding='utf8') as f:
        tms = f.read()

# get question
st.sidebar.subheader("Ask author a question about their work")
query = st.sidebar.text_input(" ", "Insert question")

# summarize and reply
if api_key and author and work and query:
    if st.button("Ask author"):
        # summarize the book
        with st.spinner("Give me a minute to read the book... (It may take a few minutes for new books)"):

            work_summary = summarize_book(tms, api_key)

            st.write("Author's response:")
            completion = chat_with_author(api_key, model, adam_bio, work, work_summary, query)
            if work not in st.session_state['summarized']:
                work_summary = summarize_book(tms, api_key)
                st.session_state['summarized'].append(work)
                st.session_state['summaries'].append({work: work_summary})
                time.sleep(1)
                st.success("Document summarized!")
                st.balloons()
            else:
                work_summary = st.session_state['summaries'][st.session_state['summarized'].index(work)][work]

            st.write(f"{author}'s response:")
            completion = chat_with_author(api_key, model, 
                                          adam_bio, work, work_summary, 
                                          query, max_tokens, temperature)

            response = completion[0]
            st.write(response)